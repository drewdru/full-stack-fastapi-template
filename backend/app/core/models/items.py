import uuid

from app.core.dtos.items import ItemBase
from sqlmodel import Field, Relationship
from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from app.core.models.users import User

class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    description: str | None = Field(default=None, max_length=255)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: Optional["User"] = Relationship(back_populates="items")
