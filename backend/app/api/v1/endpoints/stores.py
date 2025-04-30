from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends
from ....crud.crud_store import crud_store
from ....models.store import Store, StoreCreate, StoreUpdate
from ....core.security import SecurityService

router = APIRouter()


@router.post("/", response_model=Store)
async def create_store(
    store: StoreCreate,
    current_user: dict = Depends(SecurityService.verify_firebase_token),
):
    """
    店舗を新規作成
    """
    try:
        store_data = await crud_store.create(obj_in=store)
        return store_data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{store_id}", response_model=Store)
async def get_store(
    store_id: str,
    current_user: dict = Depends(SecurityService.verify_firebase_token),
):
    """
    店舗情報を取得
    """
    store_data = await crud_store.get(store_id=store_id)
    if not store_data:
        raise HTTPException(status_code=404, detail="Store not found")
    return store_data


@router.get("/", response_model=List[Store])
async def list_stores(
    company_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(SecurityService.verify_firebase_token),
):
    """
    店舗一覧を取得
    """
    stores = await crud_store.get_multi(company_id=company_id, skip=skip, limit=limit)
    return stores


@router.put("/{store_id}", response_model=Store)
async def update_store(
    store_id: str,
    store_in: StoreUpdate,
    current_user: dict = Depends(SecurityService.verify_firebase_token),
):
    """
    店舗情報を更新
    """
    store_data = await crud_store.get(store_id=store_id)
    if not store_data:
        raise HTTPException(status_code=404, detail="Store not found")

    store_data = await crud_store.update(store_id=store_id, obj_in=store_in)
    return store_data


@router.delete("/{store_id}")
async def delete_store(
    store_id: str,
    current_user: dict = Depends(SecurityService.verify_firebase_token),
):
    """
    店舗を削除
    """
    store_data = await crud_store.get(store_id=store_id)
    if not store_data:
        raise HTTPException(status_code=404, detail="Store not found")

    await crud_store.delete(store_id=store_id)
    return {"message": "Store successfully deleted"}
