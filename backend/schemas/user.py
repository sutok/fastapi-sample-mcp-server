from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    """ユーザー基本情報"""

    email: EmailStr = Field(..., description="メールアドレス")
    name: str = Field(..., description="ユーザー名")
    is_active: bool = Field(default=True, description="アクティブ状態")


class UserCreate(UserBase):
    """ユーザー作成スキーマ"""

    password: str = Field(..., description="パスワード", min_length=8)


class UserUpdate(BaseModel):
    """ユーザー更新スキーマ"""

    email: Optional[EmailStr] = Field(None, description="メールアドレス")
    name: Optional[str] = Field(None, description="ユーザー名")
    password: Optional[str] = Field(None, description="パスワード", min_length=8)


class UserInDB(UserBase):
    """データベース内のユーザースキーマ"""

    id: str = Field(..., description="ユーザーID")
    hashed_password: str = Field(..., description="ハッシュ化されたパスワード")


class User(UserBase):
    """APIレスポンス用ユーザースキーマ"""

    id: str = Field(..., description="ユーザーID")
