from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, DOCXSearchTool
from .tools.notion_tool import NotionTool

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class YouTubeScript():
	"""YouTubeScript crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def youtuber_manager(self) -> Agent:
		return Agent(
			config=self.agents_config['youtuber_manager'],
			verbose=True,
			allow_delegation=True
        )

	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			verbose=True,
			tools=[SerperDevTool()]
		)

	@agent
	def screenwriter(self) -> Agent:
		return Agent(
			config=self.agents_config['screenwriter'],
			verbose=True,
			tools=[DOCXSearchTool("/Users/danielerazo/Documents/yt-scripts/script-template.docx"), NotionTool()],
			allow_delegation=True
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
		)

	@task
	def screenwriting_task(self) -> Task:
		return Task(
			config=self.tasks_config['screenwriting_task']
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the LatestTechAnalysis crew"""
		manager = self.youtuber_manager()
		agents = [agent for agent in self.agents if agent is not manager]
		return Crew(
			agents=agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.hierarchical,
			manager_agent=manager,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
