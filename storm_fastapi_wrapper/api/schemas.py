from pydantic import BaseModel, Field, validator
from typing import Literal, Optional

class StormRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=3,
        max_length=1000,
        description="The query to process with STORM",
        example="Explain how photosynthesis works"
    )

    stream: bool = Field(
        False,
        description="Whether to stream the response"
    )

    temperature: float = Field(
        0.7,
        ge=0.0,
        le=1.0,
        description="Controls randomness of output"
    )

    @validator('query')
    def validate_query(cls, v):
        if not v.strip():
            raise ValueError("Query cannot be empty")
        return v.strip()

class StormResponse(BaseModel):
    status: Literal["success", "error"] = Field(
        ...,
        description="Result status"
    )
    output: Optional[str] = Field(
        None,
        description="The processed output from STORM"
    )
    error: Optional[str] = Field(
        None,
        description="Error message if status is 'error'"
    )

    @validator('output')
    def validate_output(cls, v, values):
        if values.get('status') == "success" and not v:
            raise ValueError("Output must be provided for successful responses")
        return v
