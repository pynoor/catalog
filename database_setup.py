# importing all necessary modules

import sys

from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

# this class will create a table called 'user' in the database
# with columns name, email, picture and id, where the latter
# will be the primary key and be later referenced as a foreign
# key in the item table (see below)


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


# the following class will create a table called category
# with columns name and id (primary key), the latter of
# which will later be referenced in the items table (see below)


class Category(Base):

    __tablename__ = 'category'

    name = Column(
        String(20), nullable=False
    )

    id = Column(
        Integer, primary_key=True
    )

# the following function will be used in the JSON view function
# showCategoryJSON() and specifies how the information about the category
# is to be displayed in JSON format

    @property
    def serialize(self):
        return {
            'name': self.name
        }

# this class will create a table called 'item'
# with columns name, description, id (primary key),
# category_id and user_id, where:
# 1) the category_id and user_id are foreign keys
# relating this table the the previous tables category
# and user
# and 2) the category_id gives away in which category this
# item belongs and the user_id tells us which user created it


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

# the following function will be used in the JSON view function
# showItemJSON() and specifies how the information about the item
# is to be displayed in JSON format
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
