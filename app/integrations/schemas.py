from datetime import datetime

from pydantic import BaseModel, ConfigDict
from typing import Optional

class LogEntry(BaseModel):
    timestamp: datetime
    service: str
    level: str
    message: str

class Deployment(BaseModel):
    deployment_id: str
    service: str
    version: str
    deployed_at: datetime
    status: str

class MetricPoint(BaseModel):
    timestamp: datetime
    service: str
    metric: str
    value: float

class InvestigationContext(BaseModel):
    logs: list[LogEntry]
    deployments: list[Deployment]
    metrics: list[MetricPoint]

class LogFilters(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    service: str
    start_time: datetime
    end_time: datetime
    level: Optional[str] = None

class DeploymentFilters(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    service: str
    start_time: datetime
    end_time: datetime

class MetricFilters(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    service: str
    start_time: datetime
    end_time: datetime
    metric: Optional[str] = None
