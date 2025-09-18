from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from pathlib import Path

from .tools import (
    ProfileResponder,
    ChinaEducationExplainer,
    EmailDraftTool,
    BootcampFAQTool,
)

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class EduSales():
    """EduSales crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def coco(self) -> Agent:
        tools = [
            ProfileResponder(),
            ChinaEducationExplainer(),
            EmailDraftTool(),
            BootcampFAQTool(),
        ]

        return Agent(
            config=self.agents_config['coco'], # type: ignore[index]
            verbose=True,
            tools=tools,
            allow_delegation=False,
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def intro_task(self) -> Task:
        return Task(
            config=self.tasks_config['intro_task'], # type: ignore[index]
            tools=[self.coco().tools[0]], # ProfileResponder only
        )

    @task
    def china_ecosystem_task(self) -> Task:
        return Task(
            config=self.tasks_config['china_ecosystem_task'], # type: ignore[index]
            tools=[self.coco().tools[1]], # ChinaEducationExplainer only
        )

    @task
    def email_draft_task(self) -> Task:
        return Task(
            config=self.tasks_config['email_draft_task'], # type: ignore[index]
            tools=[self.coco().tools[2]], # EmailDraftTool only
        )

    @task
    def bootcamp_qa_task(self) -> Task:
        return Task(
            config=self.tasks_config['bootcamp_qa_task'], # type: ignore[index]
            tools=[self.coco().tools[3]], # BootcampFAQTool only
        )

    @crew
    def crew(self) -> Crew:
        """Creates the EduSales crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
