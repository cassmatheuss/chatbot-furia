from pydantic import BaseModel

class HealthViewModel(BaseModel):
    status: str
    