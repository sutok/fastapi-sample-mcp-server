from fastapi import APIRouter, HTTPException, Depends
from typing import Any
from ....crud.crud_user import crud_user
from ....models.user import UserCreate, User
from ....core.security import SecurityService
from ....models.auth import LoginRequest, TokenResponse
import requests
import logging
from firebase_admin import auth
from ....core.config import settings

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

            # EMAIL_EXISTSエラーの場合、Firestoreをチェック
            if (
                error_message == "EMAIL_EXISTS"
                and settings.ENVIRONMENT == "development"
            ):
                try:
                    # Firebase Authからユーザー情報を取得
                    user_record = auth.get_user_by_email(user_create.email)

                    # Firestoreにユーザーが存在するか確認
                    existing_user = await crud_user.get_by_uid(user_record.uid)

                    if not existing_user:
                        try:
                            # Firestoreにデータがない場合、Auth側のユーザーを削除
                            auth.delete_user(user_record.uid)
                            # 再帰的に同じエンドポイントを呼び出し
                            return await signup(user_create)
                        except Exception as delete_error:
                            logger.error(
                                f"Error deleting existing user: {str(delete_error)}"
                            )
                            raise HTTPException(
                                status_code=400,
                                detail="既存ユーザーの削除に失敗しました",
                            )
                    else:
                        raise HTTPException(
                            status_code=400,
                            detail="このメールアドレスは既に登録されています",
                        )
                except Exception as e:
                    logger.error(f"Error handling EMAIL_EXISTS: {str(e)}")
                    raise HTTPException(
                        status_code=400,
                        detail="ユーザー登録処理中にエラーが発生しました",
                    )

            raise HTTPException(
                status_code=400, detail=f"ユーザー登録に失敗しました: {error_message}"
            )

        # Firestoreにユーザー情報を保存
        user = await crud_user.create(user_create, response_data["localId"])

        try:
            # ユーザー作成後、カスタムクレームを設定
            custom_claims = {
                "role": "user",  # デフォルトロール
            }
            # company_idとbranch_idが存在する場合のみ追加
            if user.company_id:
                custom_claims["company_id"] = user.company_id
            if user.branch_id:
                custom_claims["branch_id"] = user.branch_id

            await SecurityService.set_custom_claims(
                response_data["localId"], custom_claims
            )
        except Exception as claims_error:
            # カスタムクレームの設定に失敗しても、ユーザー作成は成功しているので
            # エラーをログに記録するだけで、ユーザーは返す
            logger.error(f"Error setting custom claims: {str(claims_error)}")
            # 開発環境ではカスタムクレームの設定はスキップされるため、
            # エラーを無視してユーザー情報を返す
            if settings.ENVIRONMENT == "development":
                return user
            raise

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


@router.delete("/auth/cleanup", include_in_schema=False)  # Swagger UIには表示しない
async def cleanup_auth():
    """開発環境用：認証情報のクリーンアップ"""
    if settings.ENVIRONMENT != "development":
        raise HTTPException(
            status_code=403, detail="This endpoint is only available in development"
        )

    try:
        # Firebase Authのユーザー一覧を取得
        users = auth.list_users()
        for user in users.users:
            # ユーザーを削除
            auth.delete_user(user.uid)
            # Firestoreのユーザーデータも削除
            await crud_user.delete(user.uid)

        return {"message": "All users cleaned up successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/dev/create-admin", include_in_schema=False)
async def create_admin_user():
    """
    開発環境用：システム管理者アカウントの作成
    """
    if settings.ENVIRONMENT != "development":
        raise HTTPException(
            status_code=403,
            detail="This endpoint is only available in development environment",
        )

    try:
        admin_email = "admin@example.com"
        admin_password = "admin123"  # 開発環境専用の簡易パスワード

        # Firebase Authでユーザー作成
        user = auth.create_user(
            email=admin_email, password=admin_password, email_verified=True
        )

        # システム管理者として設定
        await SecurityService.set_custom_claims(user.uid, {"role": "system_admin"})

        # Firestoreにユーザー情報を保存
        user_create = UserCreate(
            email=admin_email,
            username="system_admin",
            role="system_admin",
            is_active=True,
        )
        await crud_user.create(user_create, user.uid)

        return {
            "message": "System admin account created successfully",
            "email": admin_email,
            "password": admin_password,
        }
    except Exception as e:
        logger.error(f"Error creating admin user: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"管理者アカウントの作成に失敗しました: {str(e)}"
        )
