from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """ログインリクエストのモデル"""

    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "strongpassword123",
            }
        }


class TokenResponse(BaseModel):
    """トークンレスポンスのモデル"""

    access_token: str
    token_type: str
    expires_in: int
