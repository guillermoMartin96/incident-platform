GET_DEPLOYMENTS_TOOL = {
    "type": "function",
    "name": "get_deployments",
    "description": (
        "Retrieve deployments for a service during a specified time range. "
        "Use this to determine whether a deployment occurred before or during "
        "an incident and to correlate software changes with changes in service behavior."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "service": {
                "type": "string",
                "description": "Service to query."
            },
            "start_time": {
                "type": "string",
                "description": "Start of the log search window."
            },
            "end_time": {
                "type": "string",
                "description": "End of the log search window."
            },
            "query": {
                "type": ["string", "null"],
                "description": (
                    "Optional text to search for in logs. "
                    "Use null for no text filtering."
                )
            }
        },
        "required": [
            "service",
            "start_time",
            "end_time",
            "query"
        ],
        "additionalProperties": False
    },
    "strict": True,
}

SEARCH_LOGS_TOOL = {
    "type": "function",
    "name": "search_logs",
    "description": (
        "Search application logs for a service during a specified time range. "
        "Use this to investigate errors, exceptions, warnings, failed requests, "
        "and other application events that may explain an incident or change "
        "in service behavior."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "service": {
                "type": "string",
                "description": "Service to query."
            },
            "start_time": {
                "type": "string",
                "description": "Start of the log search window."
            },
            "end_time": {
                "type": "string",
                "description": "End of the log search window."
            },
            "level": {
                "type": ["string", "null"],
                "enum": [
                    "DEBUG",
                    "INFO",
                    "WARNING",
                    "ERROR",
                    "CRITICAL",
                    None
                ],
                "description": (
                    "Optional log severity filter. "
                    "Use null when logs of all levels are needed."
                )
            },
            "query": {
                "type": ["string", "null"],
                "description": (
                    "Optional text to search for in logs. "
                    "Use null for no text filtering."
                )
            }
        },
        "required": [
            "service",
            "start_time",
            "end_time",
            "level",
            "query"
        ],
        "additionalProperties": False
    },
    "strict": True,
}

GET_METRICS_TOOL = {
    "type": "function",
    "name": "get_metrics",
    "description": (
        "Retrieve operational metrics for a service during a specified time range. "
        "Use this to investigate changes in service health or performance, such as "
        "latency, error rate, request volume, CPU usage, or memory usage, and to "
        "identify when abnormal behavior began or recovered."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "service": {
                "type": "string"
            },
            "start_time": {
                "type": "string"
            },
            "end_time": {
                "type": "string"
            },
            "metric": {
                "type": "string",
                "enum": [
                    "request_rate",
                    "error_rate",
                    "latency_p50",
                    "latency_p95",
                    "latency_p99",
                    "cpu_usage",
                    "memory_usage"
                ],
                "description": "Metric to retrieve."
            },
        },
        "required": [
            "service",
            "start_time",
            "end_time",
            "metric"
        ],
        "additionalProperties": False
    },
    "strict": True,
}

INCIDENT_TOOL = {
    "type": "function",
    "name": "get_deployments",
    "description": (
        "Retrieve recorded incidents for a service during a specified time range. "
        "Use this to determine whether service problems were already identified, "
        "understand their severity and status, and correlate known incidents with "
        "logs, metrics, and deployments."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "service": {
                "type": "string",
                "description": "Service name",
            },
            "start_time": {
                "type": "string",
                "description": "ISO-8601 start timestamp",
            },
            "end_time": {
                "type": "string",
                "description": "ISO-8601 end timestamp",
            },
        },
        "required": [
            "service",
            "start_time",
            "end_time",
        ],
        "additionalProperties": False,
    },
    "strict": True,
}