# 07_Function_Calling Blueprint 🛠️

## Overview
This module serves as the central **Tools Registry** and **Agent Orchestration** layer.
It allows the AI to interact with the world (Math, Time, Databases, APIs).

## Architecture

```mermaid
graph TD
    User -->|Task| Orchestrator
    
    subgraph "07_Function_Calling"
        Orchestrator[Agent Orchestrator]
        Tools[Tools Library]
    end
    
    subgraph "05_Text_Generation"
        Client[TextClient]
    end
    
    Orchestrator -->|Uses| Client
    Client -->|Calls| Tools
    Tools -->|Return Data| Client
```

## Tools Library (`api/tools_library.py`)
-   **Basic**: `calculator`, `get_system_time`, `search_database`.
-   **Smart Home**:
    -   `set_light_values`: Control lighting.
    -   `power_disco_ball`: Parallel execution demo.
    -   `start_music`: Contextual action.

## Workflows
-   **Orchestrator**: `api/agent_orchestrator.py`
    -   General purpose agent.
-   **Smart Home Lab**: `flows/smart_home_lab.py`
    -   Demonstrates **Parallel Function Calling** (Running multiple tools at once).
