from pydantic import BaseModel, Field
from typing import List

class CoordinatesInput(BaseModel):
    city: str = Field(..., description="The city to search for")
    location_near: List[str] = Field(..., description="The location to search for")
    radius: str = Field(..., description="The radius to search for")
    
    @field_validator("location_near")
    def validate_location_near(cls, v):
        if not v:
            raise ValueError("location_near must be a list of strings")
        return v
