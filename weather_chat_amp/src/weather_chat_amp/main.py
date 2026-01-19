#!/usr/bin/env python
import json
import os
import sys

from weather_chat_amp.crew import WeatherChatCrew


def run(inputs=None, **kwargs):
    """Entry point for AMP Crew projects.

    AMP will provide inputs; this function is tolerant to multiple calling styles:
    - run({"query": "..."})
    - run(inputs={"query": "..."})
    - run(query="...")
    """
    if inputs is None:
        inputs = kwargs or {}

    # If AMP/runtime passes a JSON string via env var, support that too
    env_inputs = os.getenv("CREWAI_INPUTS")
    if env_inputs and (not inputs):
        try:
            inputs = json.loads(env_inputs)
        except Exception:
            pass

    return WeatherChatCrew().crew().kickoff(inputs=inputs)


if __name__ == "__main__":
    # Local interactive test
    print("Weather Chat Crew (AMP-ready). Type 'exit' to quit.\n")
    while True:
        q = input("You: ").strip()
        if q.lower() == "exit":
            break
        out = run({"query": q})
        print("\nAssistant:\n", out, "\n")
