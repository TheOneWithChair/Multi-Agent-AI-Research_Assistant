# agents/summarize_validator_agent.py

from .agent_base import AgentBase

class SummarizeValidatorAgent(AgentBase):
    def __init__(self, max_retries=2, verbose=True):
        super().__init__(name="SummarizeValidatorAgent", max_retries=max_retries, verbose=verbose)

    def execute(self, original_text, summary):
        messages = [
            {
                "role": "system",
                "content": "You are an AI assistant that validates summaries of medical texts for accuracy, completeness, and conciseness."
            },
            {
                "role": "user",
                "content": (
                    "Assess the given summary against the original text based on the following criteria:\n"
                    "- **Accuracy** (Does the summary correctly represent key points?)\n"
                    "- **Conciseness** (Is the summary brief but informative?)\n"
                    "- **Relevance** (Does it exclude unnecessary details while covering the main ideas?)\n\n"
                    "Provide structured feedback on each aspect and an **overall rating (1-5)**, where **5** indicates an excellent summary.\n\n"
                    f"**Original Text:**\n{original_text}\n\n"
                    f"**Summary:**\n{summary}\n\n"
                    "**Summary Validation Report:**"
                )
            }
        ]
        validation = self.call_groq(
            messages=messages,
            temperature=0.3,
            max_tokens=512
        )
        return validation
