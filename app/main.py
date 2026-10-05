import logging
import app.service as service
import app.investigator.agent as agent
from app.database import DbSession
from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from typing import Annotated, Optional
from app.exceptions import IncidentNotFoundError
from app.schemas import CreateIncidentRequest, IncidentFilters, IncidentResponse, Severity
from app.integrations.schemas import Deployment, LogEntry, MetricPoint
from app.integrations.schemas import Deployment, DeploymentFilters, LogEntry, LogFilters, MetricPoint, MetricFilters
import app.integrations.service as tools_service
from app.investigator.schemas import InvestigationRequest


app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_incident_filters(
    service: Optional[str] = Query(default=None),
    severity: Optional[Severity] = Query(default=None),
    resolved: Optional[bool] = Query(default=None),
) -> IncidentFilters:
    return IncidentFilters(
        service=service,
        severity=severity,
        resolved=resolved,
    )

@app.exception_handler(SQLAlchemyError)
async def database_error_handler(
    request: Request,
    exc: SQLAlchemyError,
):
    logger.exception(
        "Database error while processing request"
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "A database error occurred"
        },
    )

@app.exception_handler(IncidentNotFoundError)
async def incident_not_found_handler(
    request: Request,
    exc: IncidentNotFoundError,
):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post(
        "/incidents", 
        response_model=IncidentResponse
        )
def create_incident_endpoint(
    request: CreateIncidentRequest,
    db: DbSession
    ) -> IncidentResponse:
    return service.create_incident(
        db,
        service=request.service,
        severity=request.severity,
        description=request.description,
    )

@app.get(
        "/incidents/{incident_id}",
        response_model=IncidentResponse)
def get_incident_endpoint(
    incident_id: int,
    db: DbSession
    ) -> IncidentResponse:
    return service.get_incident(
        db, 
        incident_id,
        )

@app.get(
        "/incidents",
        response_model=list[IncidentResponse]
        )
def list_incidents_endpoint(
    filters: Annotated[IncidentFilters, Query()],
    db: DbSession
    ) -> list[IncidentResponse]:
    return service.list_incidents(db, filters)

@app.patch(
        "/incidents/{incident_id}/resolve", 
        response_model=IncidentResponse
        )
def resolve_incident_endpoint(
    incident_id: int,
    db: DbSession
    ) -> IncidentResponse:
    return service.resolve_incident(db, incident_id)

@app.get(
        "/tools/logs",
        response_model=list[LogEntry]
        )
async def list_logs_endpoint(
    filters: Annotated[LogFilters, Query()],
    ) -> list[LogEntry]:
    return await tools_service.logs(
        service=filters.service,
        start_time=filters.start_time,
        end_time=filters.end_time,
        level=filters.level
        )

@app.get(
        "/tools/deployments",
        response_model=list[Deployment]
        )
async def list_deployments_endpoint(
    filters: Annotated[DeploymentFilters, Query()],
    ) -> list[Deployment]:
    return await tools_service.deployments(
        service=filters.service,
        start_time=filters.start_time,
        end_time=filters.end_time
        )

@app.get(
        "/tools/metrics",
        response_model=list[MetricPoint]
        )
async def list_metrics_endpoint(
    filters: Annotated[MetricFilters, Query()],
    ) -> list[MetricPoint]:
    return await tools_service.metrics(
        service=filters.service,
        start_time=filters.start_time,
        end_time=filters.end_time,
        metric=filters.metric
        )

@app.post(
        "/investigations", 
        response_model=str
        )
async def investigations_endpoint(
    request: InvestigationRequest
    ) -> str:
    return await agent.investigate(
        question=request.question,
        service=request.service,
        start_time=request.start_time,
        end_time=request.end_time,
    )
