from pydantic import BaseModel, Field


class AudioFormSchema(BaseModel):
    track_name: str = Field(
        ..., min_length=1, max_length=100, description="Name of the track"
    )
    author_name: str = Field(
        ..., min_length=1, max_length=100, description="Name of the author"
    )

    class Config:
        json_schema_extra = {
            "example": {"track_name": "My Song", "author_name": "John Doe"}
        }
