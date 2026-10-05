from sqlalchemy.orm import Session

from app import repository
from app.exceptions import IncidentNotFoundError
from app.models import IncidentModel
from app.schemas import IncidentFilters, IncidentUpdates, Severity

def create_incident(
        db: Session,
        service: str,
        severity: Severity,
        description: str,
        ) -> IncidentModel:
      return repository.create_incident(
           db, 
           service,severity, 
           description,
           )

def get_incident(
        db: Session,
        incident_id: int,
        ) -> IncidentModel:
    incident = repository.get_incident(
            db, 
            incident_id,
            )
    if incident is None:
         raise IncidentNotFoundError(
               f"Incident {incident_id} not found"
               )
    return incident

def list_incidents(
          db: Session,
          filters: IncidentFilters,
          ) -> list[IncidentModel]:
       return repository.list_incidents(
             db,
             filters,
             )

def update_incident(
            db: Session,
            incident_id: int,
            updates: IncidentUpdates,
            ) -> IncidentModel:
       return repository.update_incident(
             db,
             incident_id,
             updates,
             )    

def resolve_incident(
            db: Session,
            incident_id: int,
            ) -> IncidentModel:
      updates = IncidentUpdates(resolved=True)

      return update_incident(db, incident_id, updates)


