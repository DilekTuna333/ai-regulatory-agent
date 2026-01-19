# Weather Chat Crew (AMP-ready)

This is a **CrewAI Crew project** structured to deploy to **CrewAI AMP**.

## What it does
- 1 agent that chats with the user
- When asked about weather for a city, it calls a tool that uses Open-Meteo:
  - Geocoding API -> lat/lon
  - Forecast API -> current temperature + wind

## Local run
> You need an LLM key configured for CrewAI (e.g., OpenAI) in your environment.

```bash
uv venv
uv pip install -e .
python -m weather_chat_amp.main
```

## AMP deployment notes
- AMP requires a `uv.lock` file. Generate it before deploying:
```bash
uv lock
```
Commit `uv.lock` to your GitHub repo before deploying.
