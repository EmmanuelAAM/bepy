from pydantic import BaseModel

class AssetSchemaCreate(BaseModel):
    name: str

class AssetSchema(AssetSchemaCreate):
    id: int
    name: str
    class Config:
        from_attributes = True
