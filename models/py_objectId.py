from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from bson import ObjectId
from models import PyObjectId

class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        """Tell Pydantic to use `validate` when processing this type."""
        yield cls.validate

    @classmethod
    def validate(cls, value):
        """Validate and convert input into an ObjectId."""
        # Check if the value can be a valid ObjectId
        if not ObjectId.is_valid(value):
            raise ValueError(f"Invalid ObjectId: {value}")
        # Convert string → ObjectId
        return ObjectId(value)

    @classmethod
    def __modify_schema__(cls, field_schema):
        """Make JSON schema show this as a string type."""
        field_schema.update(type="string")


class MongoModel(BaseModel):
    """Base model with ObjectId + JSON encoding support."""
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}