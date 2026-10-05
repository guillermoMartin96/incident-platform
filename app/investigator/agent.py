from openai import AsyncOpenAI
import json
from datetime import datetime
import logging
from dataclasses import dataclass
from app.config import settings
from app.integrations.service import execute_tool
from app.investigator.exceptions import InvestigationLimitError
from app.investigator.prompts import INVESTIGATOR_INSTRUCTIONS
from app.investigator.schemas import InvestigationToolContext
from app.investigator.config import MAX_MODEL_CALLS, MAX_TOOL_ROUNDS, MODEL, TOOLS, MAX_INVESTIGATION_TOKENS

@dataclass
class InvestigationUsage:
    model_calls: int = 0
    tool_calls: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = AsyncOpenAI(
    api_key=settings.openai_api_key,
)

async def investigate(
        question: str,
        service: str,
        start_time: datetime,
        end_time: datetime,
        ) -> str:
        
    investigation_input = f"""
    Service: {service}
    Start time: {start_time.isoformat()}
    End time: {end_time.isoformat()}
    Investigation question:
    {question}
    """

    tool_cache: dict[str, str] = {}
    usage = InvestigationUsage()

    response = await create_investigation_response(
        usage=usage,
        model=MODEL,
        instructions=INVESTIGATOR_INSTRUCTIONS,
        input=investigation_input,
        tools=TOOLS,
        )

    for round_number in range(1, MAX_TOOL_ROUNDS + 1):

        logger.info(
            "Investigation round=%d",
            round_number,
            )
        
        tool_calls = [
            item
            for item in response.output
            if item.type == "function_call"
        ]

        if not tool_calls:
            logger.info(
                "Investigation complete: "
                "model_calls=%d tool_calls=%d "
                "input_tokens=%d output_tokens=%d "
                "total_tokens=%d",
                usage.model_calls,
                usage.tool_calls,
                usage.input_tokens,
                usage.output_tokens,
                usage.total_tokens,
                )
            return response.output_text

        tool_outputs = []

        for item in tool_calls:
            usage.tool_calls += 1

            logger.info(
                "Tool call #%d: round=%d "
                "tool=%s arguments=%s",
                usage.tool_calls,
                round_number,
                item.name,
                item.arguments,
                )
            arguments = json.loads(item.arguments)
            cache_key = json.dumps(
                {
                    "tool": item.name,
                    "arguments": arguments,
                },
                sort_keys=True,
                )

            if cache_key in tool_cache:
                logger.info(
                    "Tool cache hit: tool=%s arguments=%s",
                    item.name,
                    item.arguments,
                    )
                tool_result = tool_cache[cache_key]
            else:
                tool_result = await execute_tool(
                    item, 
                    InvestigationToolContext(
                        service=service, 
                        start_time=start_time, 
                        end_time=end_time
                        )
                    )
                tool_cache[cache_key] = tool_result

            tool_outputs.append(
                {
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": tool_result,
                }
            )

        response = await create_investigation_response(
            usage=usage,
            model=MODEL,
            instructions=INVESTIGATOR_INSTRUCTIONS,
            previous_response_id=response.id,
            input=tool_outputs,
            tools=TOOLS,
        )
    tool_calls = [
        item
        for item in response.output
        if item.type == "function_call"
        ]

    if not tool_calls:
        return response.output_text    

    logger.warning(
        "Investigation hit tool-round limit. "
        "remaining_tool_calls=%s",
        [
            {
                "tool": item.name,
                "arguments": item.arguments,
            }
            for item in tool_calls
        ],
        )
    
    raise InvestigationLimitError(
        f"Investigation exceeded maximum of "
        f"{MAX_TOOL_ROUNDS} tool rounds"
        )

async def create_investigation_response(
        usage: InvestigationUsage,
        **kwargs,
        ):
    if usage.model_calls >= MAX_MODEL_CALLS:
        raise InvestigationLimitError(
            f"Investigation exceeded maximum of "
            f"{MAX_MODEL_CALLS} model calls"
        )

    response = await client.responses.create(**kwargs)

    usage.model_calls += 1

    if response.usage:
        usage.input_tokens += response.usage.input_tokens
        usage.output_tokens += response.usage.output_tokens
        usage.total_tokens += response.usage.total_tokens

    logger.info(
        "OpenAI call #%d: response_id=%s "
        "input_tokens=%d output_tokens=%d "
        "response_tokens=%d investigation_tokens=%d",
        usage.model_calls,
        response.id,
        response.usage.input_tokens if response.usage else 0,
        response.usage.output_tokens if response.usage else 0,
        response.usage.total_tokens if response.usage else 0,
        usage.total_tokens,
    )

    if usage.total_tokens > MAX_INVESTIGATION_TOKENS:
        raise InvestigationLimitError(
            f"Investigation exceeded token budget of "
            f"{MAX_INVESTIGATION_TOKENS} tokens"
        )

    return response