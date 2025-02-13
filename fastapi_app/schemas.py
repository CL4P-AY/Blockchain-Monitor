from pydantic import BaseModel
from datetime import datetime


class ProviderSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class BlockSchema(BaseModel):
    id: int
    currency: str
    provider: str
    block_number: str
    created_at: datetime | None
    stored_at: datetime

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, block):
        return cls(
            id=block.id,
            currency=block.currency.name,
            provider=block.provider.name,
            block_number=block.block_number,
            created_at=block.created_at,
            stored_at=block.stored_at,
        )


class UserSchema(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True
