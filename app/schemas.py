from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict
from typing import Optional


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class CreateIncidentRequest(BaseModel):
    service: str
    severity: Severity
    description: str


class IncidentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    incident_id: int
    service: str
    severity: Severity
    description: str
    resolved: bool
    created_at: datetime
    updated_at: datetime

class IncidentFilters(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    service: Optional[str] = None
    severity: Optional[Severity] = None
    resolved: Optional[bool] = None

class IncidentUpdates(BaseModel):
    service: Optional[str] = None
    severity: Optional[Severity] = None
    description: Optional[str] = None
    resolved: Optional[bool] = None    