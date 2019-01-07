import sys

from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    name = Column(
        String(20), nullable=False
    )

    email = Column(
        String(50), nullable=False
    )

    picture = Column(
        String(40), nullable=True
    )

    id = Column(
        Integer, primary_key=True
    )


class Category(Base):

    __tablename__ = 'category'

    name = Column(
        String(20), nullable=False
    )

    id = Column(
        Integer, primary_key=True
    )

    @property
    def serialize(self):
        return {
            'name': self.name
        }

class Item(Base):

    __tablename__ = 'item'

    name = Column(
        String(20), nullable=False
    )

    id = Column(
        Integer, primary_key=True
    )

    description = Column(
        String(500), nullable=True
    )


    category_id = Column(
        Integer, ForeignKey('category.id')
    )

    category = relationship(Category)

    user_id = Column(
        Integer, ForeignKey('user.id')
    )

    user = relationship(User)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'category': self.category_id,
            'user': self.user_id
        }

engine = create_engine(
    'sqlite:///catalogwithusers.db'
)

Base.metadata.create_all(engine)
