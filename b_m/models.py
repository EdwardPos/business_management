from typing import List, Optional

from database import Base
from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    comp_id: Mapped[str] = mapped_column(String(9), unique=True, index=True)
    tax_id: Mapped[str] = mapped_column(String(14), unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    users: Mapped["Users"] = relationship(back_populates="company")
    contracts: Mapped["Contract"] = relationship(back_populates="owner")


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    hashed_password: Mapped[Optional[str]]
    company_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("companies.id"))

    company: Mapped["Company"] = relationship(back_populates="users")


class Contract(Base):
    __tablename__ = "contracts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    contr_num: Mapped[str] = mapped_column(unique=True, index=True)
    contr_type: Mapped[str]
    service_id: Mapped[int]
    status_id: Mapped[int]
    company_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("companies.id"))

    owner: Mapped["Company"] = relationship(back_populates="contracts")
