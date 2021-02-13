from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, String

from app.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)


class InventoryItem(Base):
    __tablename__ = 'inventory_items'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    manufacturer = Column(String)
    quantity = Column(Integer)
    threshold = Column(Integer, nullable=True)

    user_id = Column(Integer, ForeignKey('users.id'))

    __table_args__ = (
        CheckConstraint(quantity >= 0, name='check_quantity_non_negative'),
        CheckConstraint(threshold > 0, name='check_threshold_positive'),
    )
