from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ....crud.crud_user import crud_user
from ....models.user import User, UserUpdate, UserCreate
from ....core.security import SecurityService
from firebase_admin import auth

router = APIRouter()


@router.get("/me", response_model=User)
async def read_user_me(
    current_user: dict = Depends(SecurityService.verify_firebase_token),
):
    """
    現在のログインユーザーの情報を取得
    """
    try:
        user = await crud_user.get_by_uid(current_user["uid"])
        if not user:
            # ユーザーがFirestoreに存在しない場合、Firebase Authの情報から作成
            user_create = UserCreate(
                email=current_user["email"],
                username=current_user["email"].split("@")[
                    0
                ],  # メールアドレスからユーザー名を生成
                is_active=True,
            )
            user = await crud_user.create(user_create, current_user["uid"])

        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"ユーザー情報の取得に失敗しました: {str(e)}",
        )


@router.put("/me", response_model=User)
async def update_user_me(
    user_update: UserUpdate,
    current_user: dict = Depends(SecurityService.verify_firebase_token),
):
    """
    現在のログインユーザーの情報を更新

    Args:
        user_update (UserUpdate): 更新するユーザー情報
        current_user (dict): 現在のユーザー情報（依存性注入）

    Returns:
        User: 更新されたユーザー情報
    """
    updated_user = await crud_user.update(current_user["uid"], user_update)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return updated_user


@router.delete("/me")
async def delete_user_me(
    current_user: dict = Depends(SecurityService.verify_firebase_token),
):
    """
    現在のログインユーザーを削除

    Args:
        current_user (dict): 現在のユーザー情報（依存性注入）

    Returns:
        dict: 削除完了メッセージ
    """
    try:
        # Firebaseからユーザーを削除
        auth.delete_user(current_user["uid"])
        # Firestoreからユーザーデータを削除
        await crud_user.delete(current_user["uid"])
        return {"message": "ユーザーが正常に削除されました"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="ユーザーの削除に失敗しました")


@router.put("/users/{user_id}/role")
async def update_user_role(
    user_id: str,
    role_update: dict,
    current_user: dict = Depends(SecurityService.verify_firebase_token),
):
    """
    ユーザーのロールを更新（管理者のみ実行可能）
    """
    # 管理者権限チェック
    if current_user.get("role") not in ["system_admin", "company_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="この操作を実行する権限がありません",
        )

    try:
        # カスタムクレームを更新
        custom_claims = {
            "role": role_update["role"],
            "company_id": role_update.get("company_id"),
            "branch_id": role_update.get("branch_id"),
        }
        await SecurityService.set_custom_claims(user_id, custom_claims)

        return {"message": "ユーザーロールが正常に更新されました"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"ロールの更新に失敗しました: {str(e)}",
        )


"""
APIエンドポイントでの権限チェックは以下のように行う
"""

"""
@router.post("/some-protected-endpoint")
async def protected_endpoint(
    current_user: dict = Depends(SecurityService.verify_firebase_token),
):
    # ロールベースのアクセス制御
    # システム管理者、企業管理者、店舗管理者のみがアクセス可能 settings.pyで管理したほうが楽になるはず
    if current_user["role"] not in ["system_admin", "company_admin", "store_admin"]: 
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="この操作を実行する権限がありません",
        )

    # 企業・店舗レベルのアクセス制御
    if current_user["company_id"] != requested_company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="この企業のデータにアクセスする権限がありません",
        )

    # 処理の実行
    ...
"""


@router.delete("/cleanup", include_in_schema=False)
async def cleanup_auth(
    current_user: dict = Depends(SecurityService.verify_firebase_token),
) -> dict:
    """
    開発環境用：認証情報のクリーンアップ
    システム管理者のみが実行可能
    """
    if settings.ENVIRONMENT != "development":
        raise HTTPException(
            status_code=403,
            detail="This endpoint is only available in development environment",
        )

    # システム管理者権限チェック
    if current_user.get("role") != "system_admin":
        raise HTTPException(
            status_code=403,
            detail="この操作を実行する権限がありません。システム管理者のみが実行できます。",
        )

    try:
        # Firebase Authのユーザー一覧を取得
        users = auth.list_users()
        deleted_count = 0

        for user in users.users:
            # システム管理者自身は削除しない
            if user.uid != current_user["uid"]:
                # ユーザーを削除
                auth.delete_user(user.uid)
                # Firestoreのユーザーデータも削除
                await crud_user.delete(user.uid)
                deleted_count += 1

        return {
            "message": "Cleanup completed successfully",
            "deleted_users_count": deleted_count,
        }
    except Exception as e:
        logger.error(f"Error during cleanup: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"クリーンアップ処理中にエラーが発生しました: {str(e)}",
        )
