from __future__ import annotations

import os
from typing import List

from crewai import Agent, Crew, Process, Task, LLM
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task

from .tools.weather_tool import weather_by_city


def build_azure_llm() -> LLM:
    """Create Azure LLM instance from env vars (Azure OpenAI)."""

    api_key = os.environ.get("AZURE_OPENAI_API_KEY")
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")
    deployment = os.environ.get("AZURE_DEPLOYMENT_NAME")

    missing = []
    if not api_key:
        missing.append("AZURE_OPENAI_API_KEY")
    if not endpoint:
        missing.append("AZURE_OPENAI_ENDPOINT")
    if not deployment:
        missing.append("AZURE_DEPLOYMENT_NAME")

    if missing:
        raise RuntimeError(f"Missing env var(s): {', '.join(missing)}")

    return LLM(
        model=f"azure/{deployment}",
        api_key=api_key,
        base_url=endpoint,
        api_version=api_version,
    )



@CrewBase  # REQUIRED for AMP deployments
class WeatherChatCrew:
    """Weather Chat Crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def weather_chat_agent(self) -> Agent:
        azure_llm = build_azure_llm()
        return Agent(
            config=self.agents_config["weather_chat_agent"],  # type: ignore[index]
            tools=[weather_by_city],
            llm=azure_llm,
        )

    @task
    def chat_task(self) -> Task:
        return Task(
            config=self.tasks_config["chat_task"],  # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
