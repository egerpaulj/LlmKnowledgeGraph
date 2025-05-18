from pydantic import BaseModel, Field


class CleanText(BaseModel):
    original: str = Field(
        description="Original text"

    )
    converted: str = Field(
        description="Converted text"
    )