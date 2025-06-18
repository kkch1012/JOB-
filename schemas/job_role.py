from pydantic import BaseModel

class JobRoleCreate(BaseModel):
    name: str

class JobRoleResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
