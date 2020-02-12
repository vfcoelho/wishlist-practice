from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(256),nullable=False)
    name = Column(String(256),nullable=False)

    list_list = relationship("List", back_populates="user")
    guest_list_list = relationship("GuestList", back_populates="user")

    # parent_tenant = relationship("Tenant", back_populates="child_configs_list",foreign_keys=[parent_tenant_id])
    # tenant = relationship('Tenant', backref="config", uselist=False,foreign_keys=[tenant_id])

class List(Base):
    __tablename__='list'

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer,ForeignKey('user.id', ondelete="RESTRICT"), nullable=False)
    list_name = Column(String(256),nullable=False)

    user = relationship("User", back_populates="list_list")
    guest_list_list = relationship("GuestList", back_populates="list")
    item_list = relationship("Item", back_populates="list")

class GuestList(Base):
    __tablename__='guest_list'

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer,ForeignKey('user.id', ondelete="RESTRICT"), nullable=False)
    list_id = Column(Integer,ForeignKey('list.id', ondelete="RESTRICT"), nullable=False)

    user = relationship("User", back_populates="guest_list_list")
    list = relationship("List", back_populates="guest_list_list")

    item_list = relationship("Item", back_populates="guest")

class Item(Base):
    __tablename__='item'

    id = Column(Integer, primary_key=True, nullable=False)
    guest_id = Column(Integer,ForeignKey('guest_list.id', ondelete="RESTRICT"), nullable=False)
    list_id = Column(Integer,ForeignKey('list.id', ondelete="RESTRICT"), nullable=False)
    item_name = Column(String(256),nullable=False)

    guest = relationship("GuestList", back_populates="item_list")
    list = relationship("List", back_populates="item_list")

def build_model():
    # use: https://stackoverflow.com/questions/24622170/using-alembic-api-from-inside-application-code
    drop_model()
    import alembic.config
    alembicArgs = [
        '-x', 'scope=test',
        'upgrade', 'head',
    ]
    alembic.config.main(argv=alembicArgs)


def drop_model():
    import alembic.config
    alembicArgs = [
        '-x', 'scope=test',
        'downgrade', 'base',
    ]
    alembic.config.main(argv=alembicArgs)