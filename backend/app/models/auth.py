from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """ログインリクエストのモデル"""

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """トークンレスポンスのモデル"""

    access_token: str
    token_type: str
    expires_in: int
