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
from sqlalchemy.orm import relationship, DeclarativeBase, MappedAsDataclass

from src.schemas import AnalysisStatusEnum, GenderEnum


class Base(MappedAsDataclass, DeclarativeBase):
    """Базовый класс для моделей алхимии"""


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    gender = Column(Enum(GenderEnum), nullable=False)
    birth_year = Column(Integer, nullable=False)
    city = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    analyses = relationship(
        "Analysis",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="joined",
        uselist=True,
    )
    tags = relationship(
        "Tag",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="joined",
        uselist=True,
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

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    s3_address = Column(String, unique=True, nullable=False)
    status = Column(
        Enum(AnalysisStatusEnum), nullable=False, default=AnalysisStatusEnum.in_progress
    )
    assigned_operator_id = Column(BigInteger, ForeignKey("operators.id"), nullable=True)
    result = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    user = relationship("User", back_populates="analyses")
    assigned_operator = relationship(
        "Operator", back_populates="analyses", lazy="joined"
    )
    tags = relationship(
        "Tag", secondary=analysis_tag_association, back_populates="analyses"
    )

    def __repr__(self):
        return f"<Analysis(id={self.id}, name='{self.name}', status='{self.status.value}')>"


class Tag(Base):
    __tablename__ = "tags"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="tags")
    analyses = relationship(
        "Analysis", secondary=analysis_tag_association, back_populates="tags"
    )

    def __repr__(self):
        return f"<Tag(id={self.id}, name='{self.name}')>"


class Operator(Base):
    __tablename__ = "operators"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    token_id = Column(BigInteger, ForeignKey("tokens.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    token = relationship(
        "Token",
        back_populates="operator",
        uselist=False,
        lazy="joined",
        foreign_keys=token_id,
    )
    analyses = relationship(
        "Analysis",
        back_populates="assigned_operator",
        uselist=True,
    )

    def __repr__(self):
        return f"<Operator(id={self.id}, telegram_id={self.telegram_id})>"


class Token(Base):
    __tablename__ = "tokens"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    value = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    operator = relationship("Operator", back_populates="token")

    def __repr__(self):
        return f"<Token(id={self.id}, operator_id={self.operator_id})>"
