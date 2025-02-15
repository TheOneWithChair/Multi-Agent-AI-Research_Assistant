# agents/__init__.py

import logging
from .summarize_tool import SummarizeTool
from .write_article_tool import WriteArticleTool
from .sanitize_data_tool import SanitizeDataTool
from .summarize_validator_agent import SummarizeValidatorAgent
from .write_article_validator_agent import WriteArticleValidatorAgent
from .sanitize_data_validator_agent import SanitizeDataValidatorAgent
from .refiner_agent import RefinerAgent
from .validator_agent import ValidatorAgent

# Configure logging for debugging
logging.basicConfig(level=logging.INFO)

class AgentManager:
    def __init__(self, max_retries=2, verbose=True):
        self.max_retries = max_retries
        self.verbose = verbose
        self.agent_classes = {
            "summarize": SummarizeTool,
            "write_article": WriteArticleTool,
            "sanitize_data": SanitizeDataTool,
            "summarize_validator": SummarizeValidatorAgent,
            "write_article_validator": WriteArticleValidatorAgent,
            "sanitize_data_validator": SanitizeDataValidatorAgent,
            "refiner": RefinerAgent,
            "validator": ValidatorAgent
        }
        self.agents = {}

    def get_agent(self, agent_name):
        if agent_name not in self.agent_classes:
            logging.error(f"Agent '{agent_name}' not found.")
            raise ValueError(f"Agent '{agent_name}' not found.")

        # Lazy loading (only initialize when needed)
        if agent_name not in self.agents:
            self.agents[agent_name] = self.agent_classes[agent_name](
                max_retries=self.max_retries, verbose=self.verbose
            )
            logging.info(f"Initialized agent: {agent_name}")

        return self.agents[agent_name]
