from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv
import json
from pathlib import Path

load_dotenv()


class CrewAgent:
    """CrewAI Agent implementation for processing user requests"""
    
    def __init__(self, user_message: str):
        """
        Initialize and execute CrewAI agent with the user message
        
        Args:
            user_message: The input prompt from the user
        """
        self.user_message = user_message
        self.config = self._load_config()
        self.message = self._execute_crew()
    
    def _load_config(self):
        """Load configuration from JSON file"""
        config_path = Path(__file__).parent.parent / "config" / "crew_agents_config.json"
        
        try:
            with open(config_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found at {config_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Error parsing JSON configuration: {e}")
    
    def _create_agent(self, agent_name: str):
        """Create a CrewAI agent based on agent name from config"""
        agent_config = self.config['agents'][agent_name]
        llm_config = agent_config['llm']
        
        return Agent(
            role=agent_config['role'],
            goal=agent_config['goal'],
            backstory=agent_config['backstory'],
            verbose=agent_config['verbose'],
            allow_delegation=agent_config['allow_delegation'],
            llm=LLM(
                model=llm_config['model'],
                temperature=llm_config['temperature']
            )
        )
    
    def _create_task(self, task_config: dict, agent_instance):
        """Create a task from task configuration"""
        return Task(
            description=task_config['description_template'].format(
                user_message=self.user_message
            ),
            agent=agent_instance,
            expected_output=task_config['expected_output']
        )
    
    def _execute_crew(self):
        """Execute the CrewAI crew and return the result"""
        try:
            agents_list = []
            tasks_list = []
            crew_config = None
            
            # Iterate through all agents and create them with their tasks
            for agent_name, agent_config in self.config['agents'].items():
                agent_instance = self._create_agent(agent_name)
                agents_list.append(agent_instance)
                
                # Create tasks for this agent
                if 'tasks' in agent_config and agent_config['tasks']:
                    for task_config in agent_config['tasks']:
                        task_instance = self._create_task(task_config, agent_instance)
                        tasks_list.append(task_instance)
                
                # Get crew config from the first agent that has it
                if crew_config is None and 'crew' in agent_config:
                    crew_config = agent_config['crew']
            
            # Use default crew config if none found
            if crew_config is None:
                crew_config = {'process': 'sequential', 'verbose': True}
            
            # Create and execute crew
            crew = Crew(
                agents=agents_list,
                tasks=tasks_list,
                process=Process.sequential if crew_config['process'] == 'sequential' else Process.hierarchical,
                verbose=crew_config['verbose']
            )
            
            result = crew.kickoff()
            return str(result)
            
        except Exception as e:
            return f"Error processing request with CrewAI: {str(e)}"

