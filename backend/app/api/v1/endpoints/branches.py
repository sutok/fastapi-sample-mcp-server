from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends
from ....crud.crud_branch import crud_branch
from ....models.branch import Branch, BranchCreate, BranchUpdate
from ....core.security import SecurityService

router = APIRouter()


@router.post("/", response_model=Branch)
async def create_branch(
    branch: BranchCreate,
    current_user: dict = Depends(SecurityService.verify_firebase_token),
):
    """
    店舗を新規作成
    """
    try:
        branch_data = await crud_branch.create(obj_in=branch)
        return branch_data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{branch_id}", response_model=Branch)
async def get_branch(
    branch_id: str,
    current_user: dict = Depends(SecurityService.verify_firebase_token),
):
    """
    店舗情報を取得
    """
    branch_data = await crud_branch.get(branch_id=branch_id)
    if not branch_data:
        raise HTTPException(status_code=404, detail="Branch not found")
    return branch_data


@router.get("/", response_model=List[Branch])
async def list_branches(
    company_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(SecurityService.verify_firebase_token),
):
    """
    店舗一覧を取得
    """
    branches = await crud_branch.get_multi(
        company_id=company_id, skip=skip, limit=limit
    )
    return branches


@router.put("/{branch_id}", response_model=Branch)
async def update_branch(
    branch_id: str,
    branch_in: BranchUpdate,
    current_user: dict = Depends(SecurityService.verify_firebase_token),
):
    """
    店舗情報を更新
    """
    branch_data = await crud_branch.get(branch_id=branch_id)
    if not branch_data:
        raise HTTPException(status_code=404, detail="Branch not found")

    branch_data = await crud_branch.update(branch_id=branch_id, obj_in=branch_in)
    return branch_data


@router.delete("/{branch_id}")
async def delete_branch(
    branch_id: str,
    current_user: dict = Depends(SecurityService.verify_firebase_token),
):
    """
    店舗を削除
    """
    branch_data = await crud_branch.get(branch_id=branch_id)
    if not branch_data:
        raise HTTPException(status_code=404, detail="Branch not found")

    await crud_branch.delete(branch_id=branch_id)
    return {"message": "Branch successfully deleted"}
