# agents/write_article_validator_agent.py

from .agent_base import AgentBase

class WriteArticleValidatorAgent(AgentBase):
    def __init__(self, max_retries=2, verbose=True):
        super().__init__(name="WriteArticleValidatorAgent", max_retries=max_retries, verbose=verbose)

    def execute(self, topic, article):
        messages = [
            {
                "role": "system",
                "content": "You are an AI assistant that validates research articles for clarity, structure, relevance, and academic quality."
            },
            {
                "role": "user",
                "content": (
                    "Validate the given research article based on the following criteria:\n"
                    "- **Clarity & Coherence** (Is the explanation clear and easy to follow?)\n"
                    "- **Relevance** (Does the content align with the given topic and cover key aspects?)\n"
                    "- **Logical Structure** (Is the information well-organized and follows a proper flow?)\n"
                    "- **Grammar & Academic Standards** (Is the language formal and meets academic quality?)\n\n"
                    "Provide a structured evaluation for each criterion and an **overall rating** from 1 to 5.\n\n"
                    f"**Topic:** {topic}\n\n"
                    f"**Article:**\n{article}\n\n"
                    "**Validation Report:**"
                )
            }
        ]
        validation = self.call_groq(
            messages=messages,
            temperature=0.3,
            max_tokens=512
        )
        return validation
