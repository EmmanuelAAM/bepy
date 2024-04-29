from pydantic import BaseModel

class UserSchemaCreate(BaseModel):
    username: str
    email: str
    password: str

class UserSchema(UserSchemaCreate):
    id: int
    class Config:
        from_attributes = True
