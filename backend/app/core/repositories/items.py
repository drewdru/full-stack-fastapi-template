import uuid
from app.api.deps import CurrentUser, SessionDep
from sqlmodel import Session
from fastapi import HTTPException

from app.core.models.items import Item
from app.core.dtos.items import ItemCreate 


class ItemsRepository:
    """Encapsulates all items-related database operations."""

    @staticmethod
    def create_item(*, session: Session, item_in: ItemCreate, owner_id: uuid.UUID) -> Item:
        db_item = Item.model_validate(item_in, update={"owner_id": owner_id})
        session.add(db_item)
        session.commit()
        session.refresh(db_item)
        return db_item
    
    @staticmethod
    def get_user_item_by_id(
        session: SessionDep,
        current_user: CurrentUser,
        id: uuid.UUID,
    ) -> Item:
        item = session.get(Item, id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        if not current_user.is_superuser and (item.owner_id != current_user.id):
            raise HTTPException(status_code=400, detail="Not enough permissions")
        return item
