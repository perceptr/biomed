from enum import StrEnum
import uuid

from pydantic import BaseModel, ConfigDict, Field


class GenderEnum(StrEnum):
    """Гендеры"""

    male = "male"
    female = "female"


class AnalysisStatusEnum(StrEnum):
    in_progress = "in_progress"
    completed = "completed"


class UserSchema(BaseModel):
    """Схема пользователя"""

    model_config = ConfigDict(
        str_strip_whitespace=True, frozen=True, from_attributes=True
    )

    id: int
    telegram_id: int

    birth_year: int = Field(ge=1812, le=2024)
    gender: GenderEnum
    city: str


class UserCreateSchema(UserSchema):
    """Схема создания пользователя"""

    id: int | None = None


class TagSchema(BaseModel):
    """Схема тэга"""

    model_config = ConfigDict(
        str_strip_whitespace=True, frozen=True, from_attributes=True
    )

    id: int
    name: str


class TagCreateSchema(TagSchema):
    """Схема создания тэга"""

    id: int | None = None


# class UserTagsSchema(BaseModel):
#     """Отношение юзера к тегам"""

#     user: UserSchema
#     tags: list[TagSchema]


class TokenSchema(BaseModel):
    """Схема токена"""

    id: int

    model_config = ConfigDict(
        str_strip_whitespace=True, frozen=True, from_attributes=True
    )

    is_active: bool = True
    value: str = Field(default_factory=lambda: str(uuid.uuid4()))


class TokenCreateSchema(TokenSchema):
    """Схема создания токена"""

    id: int | None = None


class OperatorSchema(BaseModel):
    """Схема оператора"""

    model_config = ConfigDict(
        str_strip_whitespace=True, frozen=True, from_attributes=True
    )

    id: int

    telegram_id: int

    is_online: bool = True
    token: TokenSchema


class OperatorCreateSchema(OperatorSchema):
    """Схема создания оператора"""

    id: int | None = None


class AnalysisSchema(BaseModel):
    """Схема анализа"""

    id: int

    model_config = ConfigDict(
        str_strip_whitespace=True, frozen=True, from_attributes=True
    )

    name: str
    s3_address: str

    status: AnalysisStatusEnum

    user: UserSchema
    assigned_operator: OperatorSchema | None = None

    tags: list[TagSchema] = []

    result: str | None = None


class AnalysisCreateSchema(AnalysisSchema):
    """Схема создания анализа"""

    id: int | None = None
