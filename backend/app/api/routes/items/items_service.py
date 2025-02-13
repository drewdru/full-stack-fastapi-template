import uuid
from typing import Any

from app.core.repositories.items import ItemsRepository
from fastapi import APIRouter
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.core.models.items import Item
from app.core.dtos.items import ItemCreate, ItemsPublic, ItemUpdate
from app.core.dtos.message import Message

router = APIRouter(prefix="/items", tags=["items"])
    

class ItemsService:
    """Handles items-related business logic and database operations"""

    @staticmethod
    def read_items(
        session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
    ) -> Any:
        """
        Retrieve items.
        """

        if current_user.is_superuser:
            count_statement = select(func.count()).select_from(Item)
            count = session.exec(count_statement).one()
            statement = select(Item).offset(skip).limit(limit)
            items = session.exec(statement).all()
        else:
            count_statement = (
                select(func.count())
                .select_from(Item)
                .where(Item.owner_id == current_user.id)
            )
            count = session.exec(count_statement).one()
            statement = (
                select(Item)
                .where(Item.owner_id == current_user.id)
                .offset(skip)
                .limit(limit)
            )
            items = session.exec(statement).all()
        return ItemsPublic(data=items, count=count)

    @staticmethod
    def read_item(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
        """
        Get item by ID.
        """
        return ItemsRepository.get_user_item_by_id(
            session, current_user, id,
        )

    @staticmethod
    def create_item(
        session: SessionDep, current_user: CurrentUser, item_in: ItemCreate
    ) -> Any:
        """
        Create new item.
        """
        item = Item.model_validate(item_in, update={"owner_id": current_user.id})
        session.add(item)
        session.commit()
        session.refresh(item)
        return item

    @staticmethod
    def update_item(
        session: SessionDep,
        current_user: CurrentUser,
        id: uuid.UUID,
        item_in: ItemUpdate,
    ) -> Any:
        """
        Update an item.
        """
        item = ItemsRepository.get_user_item_by_id(
            session, current_user, id,
        )
        update_dict = item_in.model_dump(exclude_unset=True)
        item.sqlmodel_update(update_dict)
        session.add(item)
        session.commit()
        session.refresh(item)
        return item


    @staticmethod
    def delete_item(
        session: SessionDep, current_user: CurrentUser, id: uuid.UUID
    ) -> Message:
        """
        Delete an item.
        """
        item = ItemsRepository.get_user_item_by_id(
            session, current_user, id,
        )
        session.delete(item)
        session.commit()
        return Message(message="Item deleted successfully")
