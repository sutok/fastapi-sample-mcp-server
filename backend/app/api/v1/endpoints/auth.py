from fastapi import APIRouter, HTTPException, Depends
from typing import Any
from ....crud.crud_user import crud_user
from ....models.user import UserCreate, User
from ....core.security import SecurityService
from ....models.auth import LoginRequest, TokenResponse
import requests
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/signup", response_model=User)
async def signup(user_create: UserCreate) -> Any:
    """
    新規ユーザー登録

    Args:
        user_create (UserCreate): 登録するユーザー情報

    Returns:
        User: 作成されたユーザー情報

    Raises:
        HTTPException: メールアドレスが既に使用されている場合など
    """
    try:
        # エミュレータのエンドポイント
        auth_url = f"http://localhost:9099/identitytoolkit.googleapis.com/v1/accounts:signUp?key=fake-api-key"

        payload = {
            "email": user_create.email,
            "password": user_create.password,
            "returnSecureToken": True,
        }

        headers = {"Content-Type": "application/json"}

        response = requests.post(auth_url, json=payload, headers=headers)
        response_data = response.json()

        if response.status_code != 200:
            error_message = response_data.get("error", {}).get(
                "message", "不明なエラー"
            )
            logger.error(f"Signup error: {error_message}")
            raise HTTPException(
                status_code=400, detail=f"ユーザー登録に失敗しました: {error_message}"
            )

        # Firestoreにユーザー情報を保存
        user = await crud_user.create(user_create, response_data["localId"])

        return user

    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="サーバーエラーが発生しました")


@router.post("/login", response_model=TokenResponse)
async def login(login_data: LoginRequest) -> Any:
    """
    ユーザーログイン

    Args:
        login_data (LoginRequest): ログインリクエストのモデル

    Returns:
        TokenResponse: アクセストークンとトークン情報
    """
    try:
        # エミュレータのエンドポイント
        auth_url = f"http://localhost:9099/identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=fake-api-key"

        payload = {
            "email": login_data.email,
            "password": login_data.password,
            "returnSecureToken": True,
        }

        headers = {"Content-Type": "application/json"}

        response = requests.post(auth_url, json=payload, headers=headers)
        response_data = response.json()

        if response.status_code != 200:
            error_message = response_data.get("error", {}).get("message", "")
            logger.error(f"Login error: {error_message}")
            raise HTTPException(
                status_code=401,
                detail="メールアドレスまたはパスワードが正しくありません",
            )

        return TokenResponse(
            access_token=response_data["idToken"],
            token_type="bearer",
            expires_in=int(response_data["expiresIn"]),
        )

    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}")
        raise HTTPException(
            status_code=500, detail="ログイン処理中にエラーが発生しました"
        )
