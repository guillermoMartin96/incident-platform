from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Optional

from app.exceptions import IncidentNotFoundError
from app.models import IncidentModel
from app.schemas import IncidentFilters, IncidentUpdates, Severity

def create_incident(
    db: Session,
    service: str,
    severity: Severity,
    description: str,
) -> IncidentModel:
    incident = IncidentModel(
        service=service,
        severity=severity.value,
        description=description,
        resolved=False,
    )

    db.add(incident)
    db.flush()
    db.refresh(incident)

    return incident


def get_incident(
    db: Session,
    incident_id: int,
) -> Optional[IncidentModel]:
    return db.get(IncidentModel, incident_id)
    

def list_incidents(
    db: Session,
    filters: IncidentFilters,
) -> list[IncidentModel]:

    statement = select(IncidentModel)

    if filters.service is not None:
        statement = statement.where(
            IncidentModel.service == filters.service
        )

    if filters.severity is not None:
        statement = statement.where(
            IncidentModel.severity == filters.severity.value
        )

    if filters.resolved is not None:
        statement = statement.where(
            IncidentModel.resolved == filters.resolved
        )

    result = db.scalars(statement)

    return list(result.all())
    

def update_incident(
        db: Session,
        incident_id: int,
        updates: IncidentUpdates,
        ) -> IncidentModel:
    incident = db.get(IncidentModel, incident_id)

    if incident is None:
        raise IncidentNotFoundError(
            f"Incident {incident_id} not found"
        )

    update_data = updates.model_dump(
        exclude_unset=True,
        exclude_none=True,
    )

    for field, value in update_data.items():
        if isinstance(value, Severity):
            value = value.value

        setattr(incident, field, value)

    db.flush()
    db.refresh(incident)

    return incident
    