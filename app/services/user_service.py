from builtins import Exception, bool, classmethod, int, str
from datetime import datetime, timezone
import secrets
from typing import Optional, Dict, List
from pydantic import ValidationError
from sqlalchemy import func, update, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_email_service, get_settings
from app.models.user_model import User
from app.schemas.user_schemas import UserCreate, UserUpdate
from app.utils.nickname_gen import generate_nickname
from app.utils.security import generate_verification_token, hash_password, verify_password
from uuid import UUID
from app.services.email_service import EmailService
from app.models.user_model import UserRole
import logging

settings = get_settings()
logger = logging.getLogger(__name__)

class UserService:
    @classmethod
    async def _execute_query(cls, session: AsyncSession, query):
        try:
            result = await session.execute(query)
            await session.commit()
            return result
        except SQLAlchemyError as e:
            logger.error(f"Database error: {e}")
            await session.rollback()
            raise e

    @classmethod
    async def _fetch_user(cls, session: AsyncSession, **filters) -> Optional[User]:
        query = select(User).filter_by(**filters)
        result = await cls._execute_query(session, query)
        return result.scalars().first() if result else None

    @classmethod
    async def get_by_id(cls, session: AsyncSession, user_id: UUID) -> Optional[User]:
        return await cls._fetch_user(session, id=user_id)

    @classmethod
    async def get_by_nickname(cls, session: AsyncSession, nickname: str) -> Optional[User]:
        return await cls._fetch_user(session, nickname=nickname)

    @classmethod
    async def get_by_email(cls, session: AsyncSession, email: str) -> Optional[User]:
        return await cls._fetch_user(session, email=email)

    @classmethod
    async def create(cls, session: AsyncSession, user_data: Dict[str, str], email_service: EmailService) -> Optional[User]:
        try:
            validated_data = UserCreate(**user_data).model_dump()
            
            # Ensure email is unique
            if await cls.get_by_email(session, validated_data['email']):
                logger.error("User with the provided email already exists.")
                return None
            
            # Hash the password
            validated_data['hashed_password'] = hash_password(validated_data.pop('password'))

            # Generate unique nickname
            new_nickname = generate_nickname()
            while await cls.get_by_nickname(session, new_nickname):
                new_nickname = generate_nickname()
            validated_data['nickname'] = new_nickname

            # Create and save the user
            new_user = User(**validated_data)
            new_user.verification_token = generate_verification_token()
            session.add(new_user)
            await session.commit()

            # Send verification email
            await email_service.send_verification_email(new_user)
            
            logger.info(f"User {new_user.id} created successfully.")
            return new_user
        except ValidationError as e:
            logger.error(f"Validation error during user creation: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during user creation: {e}")
            return None

    @classmethod
    async def update(cls, session: AsyncSession, user_id: UUID, update_data: Dict[str, str]) -> Optional[User]:
        try:
            validated_data = UserUpdate(**update_data).dict(exclude_unset=True)

            # Hash password if updated
            if 'password' in validated_data:
                validated_data['hashed_password'] = hash_password(validated_data.pop('password'))

            # Update the user
            query = update(User).where(User.id == user_id).values(**validated_data).execution_options(synchronize_session="fetch")
            await cls._execute_query(session, query)
            updated_user = await cls.get_by_id(session, user_id)
            
            if updated_user:
                session.refresh(updated_user)
                logger.info(f"User {user_id} updated successfully.")
                return updated_user
            else:
                logger.error(f"User {user_id} not found after update.")
                return None
        except ValidationError as e:
            logger.error(f"Validation error during user update: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during user update: {e}")
            return None

    @classmethod
    async def delete(cls, session: AsyncSession, user_id: UUID) -> bool:
        try:
            user = await cls.get_by_id(session, user_id)
            if not user:
                logger.info(f"User with ID {user_id} not found.")
                return False
            await session.delete(user)
            await session.commit()
            logger.info(f"User {user_id} deleted successfully.")
            return True
        except Exception as e:
            logger.error(f"Error deleting user {user_id}: {e}")
            return False

    @classmethod
    async def list_users(cls, session: AsyncSession, skip: int = 0, limit: int = 10) -> List[User]:
        query = select(User).offset(skip).limit(limit)
        result = await cls._execute_query(session, query)
        return result.scalars().all() if result else []

    @classmethod
    async def register_user(cls, session: AsyncSession, user_data: Dict[str, str], get_email_service) -> Optional[User]:
        return await cls.create(session, user_data, get_email_service)

    @classmethod
    async def login_user(cls, session: AsyncSession, email: str, password: str) -> Optional[User]:
        user = await cls.get_by_email(session, email)
        if user:
            if not user.email_verified:
                logger.warning(f"User {user.id} attempted login with unverified email.")
                return None
            if user.is_locked:
                logger.warning(f"User {user.id} is locked out.")
                return None
            if verify_password(password, user.hashed_password):
                user.failed_login_attempts = 0
                user.last_login_at = datetime.now(timezone.utc)
                session.add(user)
                await session.commit()
                return user
            else:
                user.failed_login_attempts += 1
                if user.failed_login_attempts >= settings.max_login_attempts:
                    user.is_locked = True
                session.add(user)
                await session.commit()
        return None

    @classmethod
    async def reset_password(cls, session: AsyncSession, user_id: UUID, new_password: str) -> bool:
        try:
            hashed_password = hash_password(new_password)
            user = await cls.get_by_id(session, user_id)
            if user:
                user.hashed_password = hashed_password
                user.failed_login_attempts = 0
                user.is_locked = False
                session.add(user)
                await session.commit()
                logger.info(f"Password for user {user.id} reset successfully.")
                return True
            return False
        except Exception as e:
            logger.error(f"Error resetting password for user {user_id}: {e}")
            return False
