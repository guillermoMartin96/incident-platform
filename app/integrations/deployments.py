from datetime import datetime, time
from zoneinfo import ZoneInfo
from app.integrations.schemas import Deployment

async def get_deployments(
        service: str,
        start_time: datetime,
        end_time: datetime,
        ) -> list[Deployment]:

        service = "memo"

        LOCAL_TZ = ZoneInfo("America/Los_Angeles")

        FAKE_TIME_1 = time(13, 58, 0)
        FAKE_DATETIME_1 = datetime.combine(
                datetime.now(LOCAL_TZ).date(),
                FAKE_TIME_1,
                tzinfo=LOCAL_TZ,
                )

        FAKE_TIME_2 = time(14, 17, 0) #2026-09-22 14:17:00
        FAKE_DATETIME_2 = datetime.combine(
                datetime.now(LOCAL_TZ).date(),
                FAKE_TIME_2,
                tzinfo=LOCAL_TZ,
                )

        deployments = [
                Deployment(
                        deployment_id="2", 
                        service=service, 
                        version="1.42", 
                        deployed_at=FAKE_DATETIME_1, 
                        status="SUCCESS"
                        ),
                Deployment(
                        deployment_id="3", 
                        service=service, 
                        version="1.43", 
                        deployed_at=FAKE_DATETIME_2, 
                        status="SUCCESS"
                        ),
        ]
        response = [d for d in deployments if d.service == service and start_time <= d.deployed_at <= end_time]
        print(response)

        return response