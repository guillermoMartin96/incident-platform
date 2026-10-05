# Incident Investigation Platform

An AI-assisted incident investigation platform that correlates incidents, logs, metrics, and deployments to help engineers diagnose production issues.

The project combines a traditional backend service with an AI investigator capable of querying operational data through tools, reasoning over the collected evidence, and producing a structured incident analysis.

## Overview

When a production incident occurs, engineers often need to manually inspect several sources of information:

- Application logs
- Service metrics
- Recent deployments
- Existing incidents
- Database records

This project explores how an AI agent can perform much of that initial investigation automatically.

Given a service and investigation window, the investigator can decide which tools to call, gather relevant operational evidence, and use that evidence to identify a likely root cause.

Example investigation flow:

```text
Investigation Request
        |
        v
   AI Investigator
        |
        +----> Logs
        |
        +----> Metrics
        |
        +----> Deployments
        |
        +----> Incidents
        |
        v
 Evidence + Reasoning
        |
        v
Investigation Report
```

## Current Features

### Incident Management

REST API for managing incidents with support for:

- Creating incidents
- Retrieving individual incidents
- Listing and filtering incidents
- Updating incidents
- Tracking severity and resolution status
- Created and updated timestamps

### PostgreSQL Persistence

Incidents are persisted in PostgreSQL using:

- SQLAlchemy models
- Repository and service layers
- Database transactions
- Yoyo database migrations

PostgreSQL can be started locally using Docker Compose.

### AI Incident Investigator

The investigation layer uses an LLM with tool calling to investigate operational problems.

The investigator can query:

- Logs
- Metrics
- Deployments
- Existing incidents

Rather than providing all operational data directly to the model, the model determines which tools it needs and requests the relevant evidence.

The investigation loop:

1. Receives an investigation request.
2. Sends the problem and available tools to the model.
3. Receives tool calls from the model.
4. Executes the requested integrations.
5. Returns structured tool results to the model.
6. Repeats as necessary.
7. Produces a final investigation report.

The investigator currently works against test operational data so the complete agent workflow can be developed and tested locally.

### Investigation Reports

The investigator is instructed to return analysis containing:

- Summary
- Evidence
- Likely root cause
- Confidence
- Recommended next steps

### Agent Safety and Resource Limits

The investigation loop includes limits designed to prevent uncontrolled tool or model usage, including constraints around:

- Tool rounds
- Model calls
- Tool calls
- Investigation tokens
- Log results
- Metric points
- Deployment results

## Architecture

The project follows a layered architecture:

```text
app/
├── integrations/       # Operational data sources and tools
├── investigator/       # AI investigation agent
├── config.py           # Application configuration
├── database.py         # Database connection/session management
├── exceptions.py       # Application exceptions
├── main.py             # FastAPI routes and application setup
├── models.py           # SQLAlchemy database models
├── repository.py       # Database access
├── schemas.py          # Pydantic request/response models
└── service.py          # Application business logic

migrations/             # Database migrations
tests/                  # Automated tests
```

At a high level:

```text
                 ┌─────────────────────┐
                 │       FastAPI       │
                 │        API          │
                 └──────────┬──────────┘
                            │
             ┌──────────────┴──────────────┐
             │                             │
             v                             v
    Incident Service               AI Investigator
             │                             │
             v                  ┌──────────┼──────────┐
       Repository               │          │          │
             │                  v          v          v
             v                Logs      Metrics   Deployments
        PostgreSQL                         │
                                          v
                                      Incidents
```

## Technology Stack

**Backend**

- Python
- FastAPI
- Pydantic

**Database**

- PostgreSQL
- SQLAlchemy
- Psycopg
- Yoyo migrations

**AI**

- OpenAI API
- LLM tool/function calling
- Multi-step agent investigation loop

**Infrastructure**

- Docker
- Docker Compose

## Running Locally

### 1. Clone the repository

```bash
git clone <repository-url>
cd incident-platform
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a local `.env` based on the provided example:

```bash
cp .env.example .env
```

Configure the required database and API credentials in `.env`.

> `.env` is intentionally excluded from Git and should never contain credentials that are committed to the repository.

### 5. Start PostgreSQL

```bash
docker compose up -d
```

### 6. Run database migrations

```bash
yoyo apply
```

### 7. Start the API

```bash
uvicorn app.main:app --reload
```

The FastAPI development server will start locally.

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Example Investigation

An investigation request specifies the affected service and the time window to investigate.

Conceptually:

```json
{
  "question": "Why did the service begin returning errors?",
  "service": "example-service",
  "start_time": "2026-10-05T12:00:00-07:00",
  "end_time": "2026-10-05T13:00:00-07:00"
}
```

The investigator may determine that it needs to:

```text
get_deployments()
        |
        v
get_metrics()
        |
        v
get_logs()
        |
        v
correlate evidence
        |
        v
identify likely root cause
```

The exact tool sequence is not hard-coded. The model chooses tools based on the investigation and the evidence it receives.

## Design Goals

This project is intentionally structured around several production engineering principles:

**Separation of concerns**  
API, service, repository, database, integrations, and AI orchestration are kept separate.

**Structured tool interfaces**  
Operational systems expose structured data to the investigator rather than injecting large amounts of unstructured context.

**Bounded AI execution**  
Model and tool usage are limited to prevent runaway agent loops and unnecessary API usage.

**Evidence-based investigation**  
The investigator should base conclusions on retrieved operational evidence rather than unsupported assumptions.

**Observability**  
Agent execution should itself be measurable, including model calls, tool calls, token usage, latency, and failures.

## Roadmap

Planned improvements include:

- Investigation observability and tracing
- Structured investigation results
- Improved error handling and timeouts
- Tool-result caching
- Investigation persistence
- Real observability provider integrations
- Additional automated tests
- Evaluation datasets for investigation accuracy
- Dockerized application deployment
- Production-ready configuration and secret management

## Why This Project Exists

This project is primarily an exploration of Forward Deployed Engineering and AI-assisted production operations.

It combines traditional software engineering concerns—API design, databases, migrations, testing, reliability, and observability—with agentic AI concepts such as tool calling, bounded execution, evidence collection, and multi-step reasoning.

The goal is not simply to build a chatbot for operational data, but to build an investigator that can interact with engineering systems in a controlled and observable way.