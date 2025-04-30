from typing import List
from fastapi import APIRouter, HTTPException, Depends
from ....crud.crud_company import crud_company
from ....models.company import Company, CompanyCreate, CompanyUpdate
from ....core.security import SecurityService

router = APIRouter()


@router.post("/", response_model=Company)
async def create_company(
    company: CompanyCreate,
    current_user: dict = Depends(SecurityService.verify_firebase_token),
):
    """
    企業を新規作成
    """
    company_data = await crud_company.create(obj_in=company)
    return company_data


@router.get("/{company_id}", response_model=Company)
async def get_company(
    company_id: str,
    current_user: dict = Depends(SecurityService.verify_firebase_token),
):
    """
    企業情報を取得
    """
    company_data = await crud_company.get(company_id=company_id)
    if not company_data:
        raise HTTPException(status_code=404, detail="Company not found")
    return company_data


@router.get("/", response_model=List[Company])
async def list_companies(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(SecurityService.verify_firebase_token),
):
    """
    企業一覧を取得
    """
    companies = await crud_company.get_multi(skip=skip, limit=limit)
    return companies


@router.put("/{company_id}", response_model=Company)
async def update_company(
    company_id: str,
    company_in: CompanyUpdate,
    current_user: dict = Depends(SecurityService.verify_firebase_token),
):
    """
    企業情報を更新

    Args:
        company_id: 更新対象の企業ID
        company_in: 更新する企業情報
        current_user: 現在のユーザー情報（依存性注入）

    Returns:
        Company: 更新された企業情報
    """
    company_data = await crud_company.get(company_id=company_id)
    if not company_data:
        raise HTTPException(status_code=404, detail="Company not found")

    company_data = await crud_company.update(company_id=company_id, obj_in=company_in)
    return company_data


@router.delete("/{company_id}")
async def delete_company(
    company_id: str,
    current_user: dict = Depends(SecurityService.verify_firebase_token),
):
    """
    企業を削除
    """
    company_data = await crud_company.get(company_id=company_id)
    if not company_data:
        raise HTTPException(status_code=404, detail="Company not found")
    await crud_company.delete(company_id=company_id)
    return {"message": "Company successfully deleted"}
