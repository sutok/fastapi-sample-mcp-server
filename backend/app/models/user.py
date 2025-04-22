from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    """ユーザーの基本情報モデル"""

    email: EmailStr
    username: str
    is_active: bool = True


class UserCreate(UserBase):
    """ユーザー作成時のモデル"""

    password: str


class UserUpdate(BaseModel):
    """ユーザー情報更新時のモデル"""

    username: Optional[str] = None
    email: Optional[EmailStr] = None


class UserInDB(UserBase):
    """データベースに保存されるユーザーモデル"""

    uid: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class User(UserInDB):
    """APIレスポンス用ユーザーモデル"""

    pass
