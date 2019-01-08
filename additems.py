from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Item, Base

engine = create_engine('sqlite:///catalogwithusers.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

rihanna = Item(
    name='Rihanna',
    description='',
    category_id=1,
    user_id = 1
    )
session.add(rihanna)
session.commit()

muddy_waters = Item(
    name='Muddy Waters',
    description='',
    category_id=2,
    user_id = 1
    )
session.add(muddy_waters)
session.commit()

beyonce = Item(
    name='Beyonce',
    description='',
    category_id=3,
    user_id = 1
    )
session.add(beyonce)
session.commit()

erykah_badu = Item(
    name='Erykah Badu',
    description='Blablabla',
    category_id=4,
    user_id = 1
    )
session.add(erykah_badu)
session.commit()

jill_scott = Item(
    name='Jill Scott',
    description='',
    category_id=4,
    user_id = 1
    )
session.add(jill_scott)
session.commit()

india_arie = Item(
    name='India Arie',
    description='',
    category_id=4,
    user_id = 1
    )
session.add(india_arie)
session.commit()

dangelo = Item(
    name="D'Angelo",
    description='',
    category_id=4,
    user_id = 1
    )
session.add(dangelo)
session.commit()

richard_bona = Item(
    name='Richard Bona',
    description='',
    category_id=5,
    user_id  = 1
    )
session.add(richard_bona)
session.commit()

micheal_jackson = Item(
    name='Micheal Jackson',
    description='',
    category_id=6,
    user_id = 1
    )
session.add(micheal_jackson)
session.commit()


fela_kuti = Item(
    name='Fela Kuti',
    description='',
    category_id=7,
    user_id = 1
    )
session.add(fela_kuti)
session.commit()

chronix = Item(
    name='Chronix',
    description='',
    category_id=8,
    user_id = 1
    )
session.add(chronix)
session.commit()

busy_signal = Item(
    name='Busy Signal',
    description='',
    category_id=9,
    user_id = 1
    )
session.add(busy_signal)
session.commit()

lyrikal = Item(
    name='Lyrikal',
    description='',
    category_id=10,
    user_id = 1
    )
session.add(lyrikal)
session.commit()

tony_vega = Item(
    name='Tony Vega',
    description='',
    category_id=11,
    user_id = 1
    )
session.add(tony_vega)
session.commit()

xtreme = Item(
    name='Xtreme',
    description='',
    category_id=12,
    user_id = 1
    )
session.add(xtreme)
session.commit()
