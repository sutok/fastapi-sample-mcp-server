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
