import asyncio
import json
from datetime import datetime
from app.integrations.deployments import get_deployments
from app.integrations.metrics import get_metrics
from app.integrations.logs import search_logs
from app.integrations.schemas import Deployment, InvestigationContext, LogEntry, MetricPoint
from app.investigator.exceptions import UnknownToolError
from app.investigator.schemas import InvestigationToolContext
from typing import Optional, Protocol

async def gather_incident_context(
        service: str,
        start_time: datetime,
        end_time: datetime,
        ) -> InvestigationContext:
    logs, deployments, metrics = await asyncio.gather(
        LogsProvider.logs(service, start_time, end_time),
        deployments(service, start_time, end_time),
        metrics(service, start_time, end_time),
    )
    return InvestigationContext(logs, deployments, metrics)

class LogsProvider(Protocol):
    async def logs(
            service: str,
            start_time: datetime,
            end_time: datetime,
            level: Optional[str] = None
            ) -> list[LogEntry]:
        await asyncio.sleep(0.8)
        return await search_logs(
            service, 
            start_time, 
            end_time, 
            level
            )

async def deployments(
        service: str,
        start_time: datetime,
        end_time: datetime,
        ) -> list[Deployment]:
    await asyncio.sleep(0.5)
    return await get_deployments(
        service, 
        start_time, 
        end_time
        )

async def metrics(
        service: str,
        start_time: datetime,
        end_time: datetime,
        metric: Optional[str] = None
        ) -> list[MetricPoint]:
    await asyncio.sleep(0.9)
    return await get_metrics(
        service, 
        start_time, 
        end_time,
        metric, 
        )

async def execute_tool(
        item,
        context: InvestigationToolContext
        ) -> str:

    arguments = json.loads(item.arguments)

    if item.name == "search_logs":
        result = await LogsProvider.logs(
            service=context.service,
            start_time=context.start_time,
            end_time=context.end_time,
            level=arguments["level"],
            )

    elif item.name == "get_deployments":
        result = await deployments(
            service=context.service,
            start_time=context.start_time,
            end_time=context.end_time,
            )

    elif item.name == "get_metrics":
        result = await metrics(
            service=context.service,
            start_time=context.start_time,
            end_time=context.end_time,
            metric=arguments["metric"],
            )

    else:
        raise UnknownToolError(item.name)

    return json.dumps(
        [
            result_item.model_dump(mode="json")
            for result_item in result
        ]
        )
