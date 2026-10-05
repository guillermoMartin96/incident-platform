from datetime import datetime, time
from zoneinfo import ZoneInfo
from app.integrations.schemas import MetricPoint
from typing import Optional

async def get_metrics(
        service: str,
        start_time: datetime,
        end_time: datetime,
        metric: Optional[str] = None, 
        ) -> list[MetricPoint]:

        request_latency_ms = "request_latency_ms"
        error_rate = "error_rate"
        cpu_percent = "cpu_percent"
        db_connection_pool_usage = "db_connection_pool_usage"

        LOCAL_TZ = ZoneInfo("America/Los_Angeles")
                
        FAKE_TIME_1 = time(14, 1, 0)
        FAKE_DATETIME_1 = datetime.combine(
                datetime.now(LOCAL_TZ).date(),
                FAKE_TIME_1,
                tzinfo=LOCAL_TZ,
                )

        FAKE_TIME_2 = time(14, 3, 0)
        FAKE_DATETIME_2 = datetime.combine(
                datetime.now(LOCAL_TZ).date(),
                FAKE_TIME_2,
                tzinfo=LOCAL_TZ,
                )

        FAKE_TIME_3 = time(14, 5, 0)
        FAKE_DATETIME_3 = datetime.combine(
                datetime.now(LOCAL_TZ).date(),
                FAKE_TIME_3,
                tzinfo=LOCAL_TZ,
                )

        FAKE_TIME_4 = time(14, 6, 0)
        FAKE_DATETIME_4 = datetime.combine(
                datetime.now(LOCAL_TZ).date(),
                FAKE_TIME_4,
                tzinfo=LOCAL_TZ,
                )

        FAKE_TIME_5 = time(14, 7, 0)
        FAKE_DATETIME_5 = datetime.combine(
                datetime.now(LOCAL_TZ).date(),
                FAKE_TIME_5,
                tzinfo=LOCAL_TZ,
                )

        FAKE_TIME_6 = time(14, 20, 0)
        FAKE_DATETIME_6 = datetime.combine(
                datetime.now(LOCAL_TZ).date(),
                FAKE_TIME_6,
                tzinfo=LOCAL_TZ,
                )

        FAKE_TIME_7 = time(14, 21, 0)
        FAKE_DATETIME_7 = datetime.combine(
                datetime.now(LOCAL_TZ).date(),
                FAKE_TIME_7,
                tzinfo=LOCAL_TZ,
                )


        metrics = [
                MetricPoint(
                        timestamp=FAKE_DATETIME_1, 
                        service=service, 
                        metric=db_connection_pool_usage, 
                        value=0.72
                        ),
                MetricPoint(
                        timestamp=FAKE_DATETIME_2, 
                        service=service, 
                        metric=db_connection_pool_usage, 
                        value=0.91
                        ),
                MetricPoint(
                        timestamp=FAKE_DATETIME_3, 
                        service=service, 
                        metric=db_connection_pool_usage, 
                        value=1.0
                        ),
                MetricPoint(
                        timestamp=FAKE_DATETIME_4, 
                        service=service, 
                        metric=request_latency_ms, 
                        value=2400.0
                        ),
                MetricPoint(
                        timestamp=FAKE_DATETIME_5, 
                        service=service, 
                        metric=error_rate, 
                        value=0.18
                        ),
                MetricPoint(
                        timestamp=FAKE_DATETIME_6, 
                        service=service, 
                        metric=db_connection_pool_usage, 
                        value=0.61
                        ),
                MetricPoint(
                        timestamp=FAKE_DATETIME_7, 
                        service=service, 
                        metric=request_latency_ms, 
                        value=180.0
                        ),        
        ]
        if metric is not None:
                response = [m for m in metrics if m.service == service and m.metric == metric and start_time <= m.timestamp <= end_time]
                print(response)
                return response

        response = [m for m in metrics if m.service == service and start_time <= m.timestamp <= end_time] 
        print(response)
        return response 