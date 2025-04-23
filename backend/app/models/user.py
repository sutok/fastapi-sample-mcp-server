from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserBase(BaseModel):
    """ユーザーの基本情報モデル"""

    email: EmailStr = Field(..., description="メールアドレス")
    username: str = Field(..., description="ユーザー名")
    is_active: bool = Field(default=True, description="アクティブ状態")


class UserCreate(UserBase):
    """ユーザー作成時のモデル"""

    password: str


class UserUpdate(BaseModel):
    """ユーザー情報更新時のモデル"""

    username: Optional[str] = None
    email: Optional[EmailStr] = None


class User(UserBase):
    """APIレスポンス用ユーザーモデル"""

    id: str = Field(..., description="ユーザーID")
    created_at: datetime = Field(..., description="作成日時")
    updated_at: datetime = Field(..., description="更新日時")

    class Config:
        from_attributes = True
