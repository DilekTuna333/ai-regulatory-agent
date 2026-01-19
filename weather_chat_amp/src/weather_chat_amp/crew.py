from typing import List

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task

from weather_chat_amp.tools.weather_tool import weather_by_city


@CrewBase  # REQUIRED for AMP deployments
class WeatherChatCrew:
    """Weather Chat Crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def weather_chat_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["weather_chat_agent"],  # type: ignore[index]
            tools=[weather_by_city],
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
