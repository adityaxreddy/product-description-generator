from crewai_tools import SerperDevTool

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from product_description_generator.tools import GCSProductInfoTool
from product_description_generator.utils import format_output


@CrewBase
class ProductDescriptionGenerator:
    """Product Description Generator crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def root_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["root_agent"],
            tools=[GCSProductInfoTool(), SerperDevTool()],
            allow_delegation=True,
            verbose=True,
        )

    @agent
    def product_description_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["product_description_agent"],
            tools=[SerperDevTool()],
            allow_delegation=True,
            verbose=True,
        )

    @agent
    def refinement_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["refinement_agent"],
            tools=[SerperDevTool()],
            allow_delegation=False,
            verbose=True,
        )

    @task
    def retrieve_product_info_task(self) -> Task:
        return Task(
            config=self.tasks_config["retrieve_product_info_task"],
            tools=[GCSProductInfoTool(), SerperDevTool()],
            async_execution=False,
            agent=self.root_agent(),
        )

    @task
    def generate_description_task(self) -> Task:
        return Task(
            config=self.tasks_config["generate_description_task"],
            tools=[SerperDevTool()],
            agent=self.product_description_agent(),
            async_execution=False,
            context=[self.retrieve_product_info_task()],
        )

    @task
    def refine_description_task(self) -> Task:
        return Task(
            config=self.tasks_config["refine_description_task"],
            tools=[SerperDevTool()],
            agent=self.refinement_agent(),
            async_execution=False,
            context=[self.retrieve_product_info_task(), self.generate_description_task()],
            output_file="product_description.md",
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Product Description Generator"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,    # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            output_formatter=self.format_output
        )
    
    def format_output(self, output):
        """Format the final output to separate product description and marketing materials"""
        # Extract product info from the first task
        product_info_task = next((task for task in self.tasks if task.id == "retrieve_product_info_task"), None)
        product_info_str = product_info_task.output if product_info_task else "{}"
        
        # Extract product description from the second task
        description_task = next((task for task in self.tasks if task.id == "generate_description_task"), None)
        description = description_task.output if description_task else ""
        
        # Extract refined description from the third task
        refined_task = next((task for task in self.tasks if task.id == "refine_description_task"), None)
        refined_description = refined_task.output if refined_task else ""
        
        # Parse product info
        try:
            import json
            product_info = json.loads(product_info_str)
        except:
            product_info = {"product_name": output.get("user_query", "Product")}
        
        # Format the final output
        product_name = product_info.get("product_name", "Product")
        formatted_output = f"""# {product_name} Description

        {refined_description}

        ---
        *This description was generated based on product information and refined for optimal engagement and SEO performance.*

        """
        return formatted_output
