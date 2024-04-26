from crud.asset.asset_crud import get_asset, create_asset
from dependencies.database import get_db
from fastapi import APIRouter, Depends, status
from schemas.asset_schema import AssetSchemaCreate

crudRouter = APIRouter()

@crudRouter.get("/asset/{asset_id}")
async def get_data(asset_id: int, db=Depends(get_db)):
    return get_asset(db=db, asset_id=asset_id)

@crudRouter.post("/asset/", status_code=status.HTTP_201_CREATED)
async def save_data(asset: AssetSchemaCreate, db=Depends(get_db)):
    return create_asset(db=db, asset=asset)