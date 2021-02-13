from pydantic import BaseModel


class InventoryItemBase(BaseModel):
    name: str
    manufacturer: str = ''
    quantity: int = 0
    threshold: int = None


class InventoryItemCreateSchema(InventoryItemBase):
    pass


class InventoryItemUpdateSchema(InventoryItemBase):
    # Make name optional for update
    name: str = ''


class InventoryItemSchema(InventoryItemBase):
    id: int

    class Config:
        orm_mode = True
