from crewai_tools import SerperDevTool, WebsiteSearchTool

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class ProductDescriptionGenerator:
    """Product Description Generator crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def seo_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["seo_researcher"],
            tools=[SerperDevTool(), WebsiteSearchTool()],
            allow_delegation=True,
            verbose=True,
        )

    @agent
    def content_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["content_writer"],
            tools=[SerperDevTool()],
            allow_delegation=True,
            verbose=True,
        )

    @agent
    def marketing_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["marketing_specialist"],
            tools=[SerperDevTool()],
            allow_delegation=False,
            verbose=True,
        )

    @task
    def keyword_research_task(self) -> Task:
        return Task(
            config=self.tasks_config["keyword_research_task"],
            tools=[SerperDevTool(), WebsiteSearchTool()],
            async_execution=False,
            agent=self.seo_researcher(),
        )

    @task
    def product_description_task(self) -> Task:
        return Task(
            config=self.tasks_config["product_description_task"],
            tools=[SerperDevTool()],
            agent=self.content_writer(),
            async_execution=False,
            context=[self.keyword_research_task()],
        )

    @task
    def marketing_materials_task(self) -> Task:
        return Task(
            config=self.tasks_config["marketing_materials_task"],
            tools=[SerperDevTool()],
            agent=self.marketing_specialist(),
            async_execution=False,
            context=[self.keyword_research_task(), self.product_description_task()],
            output_file="product_marketing_package.md",
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Product Description Generator"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
output_formatter=self.format_output
        )
    
    def format_output(self, output):
        """Format the final output to separate product description and marketing materials"""
    # Extract product description from the product_description_task output
        product_description = next((task.output for task in self.tasks if task.id == "product_description_task"), "")
    
    # Extract marketing materials from the marketing_materials_task output
        marketing_materials = next((task.output for task in self.tasks if task.id == "marketing_materials_task"), "")
    
    # Format the final output
        formatted_output = f"""# {output.get('product_name', 'Product')} Description 
        {product_description}
        # Marketing Materials
        {marketing_materials}"""
        return formatted_output
