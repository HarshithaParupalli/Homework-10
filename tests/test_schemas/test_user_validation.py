import pytest
from app.schemas.user_schemas import UserCreate, UserUpdate
from pydantic import ValidationError

# Test for valid nickname
def test_valid_nickname():
    valid_nickname = "JohnDoe123"
    user = UserCreate(
        email="john.doe@example.com",
        password="ValidPassword123!",
        nickname=valid_nickname
    )
    assert user.nickname == valid_nickname

# Test for invalid nickname
@pytest.mark.parametrize("invalid_nickname", ["", "!!Invalid", "ab", "a" * 51])
def test_invalid_nickname(invalid_nickname):
    with pytest.raises(ValidationError):
        UserCreate(
            email="john.doe@example.com",
            password="ValidPassword123!",
            nickname=invalid_nickname
        )

# Test for valid password
def test_valid_password():
    valid_password = "Strong*Password123"
    user = UserCreate(
        email="john.doe@example.com",
        password=valid_password,
        nickname="JohnDoe"
    )
    assert user.password == valid_password

# Test for invalid password
@pytest.mark.parametrize(
    "invalid_password",
    [
        "short",             # Too short
        "alllowercase123",   # No uppercase
        "ALLUPPERCASE123",   # No lowercase
        "NoSpecial123",      # No special character
        "NoNumbers!"         # No digits
    ]
)
def test_invalid_password(invalid_password):
    with pytest.raises(ValidationError):
        UserCreate(
            email="john.doe@example.com",
            password=invalid_password,
            nickname="JohnDoe"
        )

# Test for user update with no values
def test_user_update_no_values():
    with pytest.raises(ValidationError):
        UserUpdate()

# Test for user update with valid data
def test_user_update_valid():
    update_data = {
        "email": "new.email@example.com",
        "nickname": "NewNickname",
        "bio": "Updated bio"
    }
    user_update = UserUpdate(**update_data)
    assert user_update.email == update_data["email"]
    assert user_update.nickname == update_data["nickname"]
    assert user_update.bio == update_data["bio"]

# Test for invalid URLs in UserBase
@pytest.mark.parametrize(
    "invalid_url", ["htp://example", "www.example.com", "https:/example.com"]
)
def test_invalid_urls(invalid_url):
    with pytest.raises(ValidationError):
        UserUpdate(profile_picture_url=invalid_url)
