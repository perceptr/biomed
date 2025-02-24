from datetime import datetime
from typing import List

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    Boolean,
    func,
    Table,
)
from sqlalchemy.orm import (
    relationship,
    DeclarativeBase,
    MappedAsDataclass,
    Mapped,
    mapped_column,
)

from src.schemas import AnalysisStatusEnum, GenderEnum


class Base(MappedAsDataclass, DeclarativeBase):
    """Базовый класс для моделей алхимии"""


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    gender: Mapped[GenderEnum] = mapped_column(Enum(GenderEnum), nullable=False)
    birth_year: Mapped[int] = mapped_column(Integer, nullable=False)
    city: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), default_factory=func.now
    )

    analyses: Mapped[List["Analysis"]] = relationship(
        "Analysis",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="joined",
        uselist=True,
        default_factory=list,
    )
    tags: Mapped[List["Tag"]] = relationship(
        "Tag",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="joined",
        uselist=True,
        default_factory=list,
    )

    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id})>"


analysis_tag_association = Table(
    "analysis_tag_association",
    Base.metadata,
    Column("analysis_id", ForeignKey("analyses.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    s3_address: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    assigned_operator_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("operators.id"), nullable=True
    )
    result: Mapped[str | None] = mapped_column(Text, nullable=True)
    user: Mapped["User"] = relationship(
        "User", back_populates="analyses", lazy="joined"
    )
    edit_note: Mapped[str] = mapped_column(String, unique=False, nullable=True, server_default=None, default=None)

    assigned_operator: Mapped["Operator|None"] = relationship(
        "Operator",
        back_populates="analyses",
        lazy="joined",
        default=None,
    )
    tags: Mapped[List["Tag"]] = relationship(
        "Tag",
        secondary=analysis_tag_association,
        back_populates="analyses",
        uselist=True,
        default_factory=list,
        lazy="joined",
    )
    status: Mapped[AnalysisStatusEnum] = mapped_column(
        Enum(AnalysisStatusEnum),
        nullable=False,
        default=AnalysisStatusEnum.in_progress,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default_factory=func.now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        default_factory=func.now,
    )

    def __repr__(self):
        return f"<Analysis(id={self.id}, name='{self.name}', status='{self.status.value}')>"


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    # created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship("User", back_populates="tags", lazy="joined",)
    analyses: Mapped[List["Analysis"]] = relationship(
        "Analysis", secondary=analysis_tag_association, back_populates="tags", lazy="joined",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default_factory=func.now,
    )

    def __repr__(self):
        return f"<Tag(id={self.id}, name='{self.name}')>"


class Token(Base):
    __tablename__ = "tokens"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    value: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), default_factory=func.now
    )


class Operator(Base):
    __tablename__ = "operators"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    token_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("tokens.id"), nullable=False
    )
    token: Mapped[Token] = relationship(
        "Token",
        uselist=False,
        lazy="joined",
        foreign_keys=[token_id],
    )

    is_online: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default_factory=func.now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        default_factory=func.now,
    )
    analyses: Mapped[list[Analysis]] = relationship(
        "Analysis",
        back_populates="assigned_operator",
        uselist=True,
        default_factory=list,
        lazy="joined",
    )

    def __repr__(self):
        return f"<Operator(id={self.id}, telegram_id={self.telegram_id})>"


class AnalysisHistory(Base):
    __tablename__ = "analysis_history"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    analysis_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    s3_address: Mapped[str] = mapped_column(String, nullable=False)
    assigned_operator_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    result: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[AnalysisStatusEnum] = mapped_column(
        Enum(AnalysisStatusEnum), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    operation: Mapped[str] = mapped_column(
        String, nullable=False
    )  # 'INSERT', 'UPDATE', 'DELETE'
    operation_timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
