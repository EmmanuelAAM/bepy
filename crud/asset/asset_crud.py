from fastapi import HTTPException, status
from models.asset_model import Asset
from schemas.asset_schema import AssetSchemaCreate
from sqlalchemy.orm import Session

def get_asset(db: Session, asset_id: Asset.id):
    element = db.query(Asset).filter(Asset.id == asset_id).first()
    if element == None:
        raise HTTPException(status_code=404, detail="Item not found")
    return { "asset": element }

def create_asset(db: Session, asset: AssetSchemaCreate):
    new_entry = Asset(name=asset.name)
    try:
        db.add(new_entry)
        db.commit()
        return new_entry
    except ValueError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=ValueError)
