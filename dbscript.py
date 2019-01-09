# importing all necessary modules

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Item, Base

# connecting to the existing database

engine = create_engine('sqlite:///catalogwithusers.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# in the following lines we are adding a few categories
# as a first step to populate our database

r_n_b = Category(name='rnb')
session.add(r_n_b)
session.commit()


blues = Category(name='blues')
session.add(blues)
session.commit()

hip_hop = Category(name='hiphop')
session.add(hip_hop)
session.commit()

soul = Category(name='soul')
session.add(soul)
session.commit()

jazz = Category(name='jazz')
session.add(jazz)
session.commit()

pop = Category(name='pop')
session.add(pop)
session.commit()

afrobeat = Category(name='afrobeat')
session.add(afrobeat)
session.commit()

reggae = Category(name='reggae')
session.add(reggae)
session.commit()

dancehall = Category(name='dancehall')
session.add(dancehall)
session.commit()

soca = Category(name='soca')
session.add(soca)
session.commit()

salsa = Category(name='salsa')
session.add(salsa)
session.commit()

bachata = Category(name='bachata')
session.add(bachata)
session.commit()
