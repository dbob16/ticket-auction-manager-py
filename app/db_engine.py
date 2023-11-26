from sqlalchemy import create_engine, String, SmallInteger, ForeignKey
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column

engine = create_engine('sqlite:///sqlite.db')
session = Session(engine)

class Base(DeclarativeBase):
    pass

class RegularTicket(Base):
    __tablename__ = "t_regulartickets"
    TicketID:Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    FirstName:Mapped[str] = mapped_column(String(50), nullable=True)
    LastName:Mapped[str] = mapped_column(String(50), nullable=True)
    PhoneNumber:Mapped[str] = mapped_column(String(50), nullable=True)
    PrefersText:Mapped[int] = mapped_column(SmallInteger(), default=0)
    def pref(self):
        if self.PrefersText == 0:
            return "CALL"
        elif self.PrefersText == -1:
            return "TEXT"
        else:
            return "OTHER"

class SpecialtyTicket(Base):
    __tablename__ = "t_specialtytickets"
    TicketID:Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    FirstName:Mapped[str] = mapped_column(String(50), nullable=True)
    LastName:Mapped[str] = mapped_column(String(50), nullable=True)
    PhoneNumber:Mapped[str] = mapped_column(String(50), nullable=True)
    PrefersText:Mapped[int] = mapped_column(SmallInteger(), default=0)
    def pref(self):
        if self.PrefersText == 0:
            return "CALL"
        elif self.PrefersText == -1:
            return "TEXT"
        else:
            return "OTHER"

class RegularBasket(Base):
    __tablename__ = "t_regularbaskets"
    BasketID:Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    Description:Mapped[str] = mapped_column(nullable=True)
    Donors:Mapped[str] = mapped_column(nullable=True)
    WinningTicket:Mapped[int] = mapped_column(ForeignKey("t_regulartickets.TicketID"))

class SpecialtyBasket(Base):
    __tablename__ = "t_specialtybaskets"
    BasketID:Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    Description:Mapped[str] = mapped_column(nullable=True)
    Donors:Mapped[str] = mapped_column(nullable=True)
    WinningTicket:Mapped[int] = mapped_column(ForeignKey("t_specialtytickets.TicketID"))

def create_tables():
    Base.metadata.create_all(engine)