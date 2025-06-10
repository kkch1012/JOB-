from pydantic import BaseModel

class CompanyResponse(BaseModel):
    id: int
    name: str
    size: str
    address: str

    class Config:
        orm_mode = True
