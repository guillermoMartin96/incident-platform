from datetime import datetime
from pydantic import BaseModel

class InvestigationRequest(BaseModel):
    service: str
    start_time: datetime
    end_time: datetime
    question: str

class InvestigationToolContext(BaseModel):
    service: str
    start_time: datetime
    end_time: datetime