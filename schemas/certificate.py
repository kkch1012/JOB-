from pydantic import BaseModel

class CertificateBase(BaseModel):
    name: str
    issuer: str

class CertificateCreate(CertificateBase):
    pass

class CertificateResponse(CertificateBase):
    id: int

    class Config:
        orm_mode = True
