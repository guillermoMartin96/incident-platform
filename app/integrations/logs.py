from datetime import datetime, time
from zoneinfo import ZoneInfo
from app.integrations.schemas import LogEntry
from app.integrations.config import MAX_LOG_RESULTS
from typing import Optional
async def search_logs(
        service: str,
        start_time: datetime,
        end_time: datetime,
        level: Optional[str] = None, 
        ) -> list[LogEntry]:

        FAKE_SERVICE = "memo"

        LOCAL_TZ = ZoneInfo("America/Los_Angeles")
        
        FAKE_TIME_1 = time(14, 4, 0) ##2026-10-02 14:04:00
        FAKE_DATETIME_1 = datetime.combine(
                datetime.now(LOCAL_TZ).date(),
                FAKE_TIME_1,
                tzinfo=LOCAL_TZ,
                )

        FAKE_TIME_2 = time(14, 5, 0) ##2026-10-02 14:05:00
        FAKE_DATETIME_2 = datetime.combine(
                datetime.now(LOCAL_TZ).date(),
                FAKE_TIME_2,
                tzinfo=LOCAL_TZ,
                )
        
        logs = [
                LogEntry(
                        timestamp=FAKE_DATETIME_1, 
                        service=FAKE_SERVICE, 
                        level="WARN", 
                        message="WARN connection pool nearing capacity"
                        ),
                LogEntry(
                        timestamp=FAKE_DATETIME_2, 
                        service=FAKE_SERVICE, 
                        level="ERROR", 
                        message="ERROR unable to acquire database connection"
                        ),

        ]
        if level is not None:
                response = [l for l in logs if l.service == service and start_time <= l.timestamp <= end_time and l.level == level][:MAX_LOG_RESULTS]
                print(response)
                return response

        response = [l for l in logs if l.service == service and start_time <= l.timestamp <= end_time][:MAX_LOG_RESULTS]
        print(response)
        return response