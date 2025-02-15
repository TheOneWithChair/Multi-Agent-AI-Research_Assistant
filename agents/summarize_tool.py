from .agent_base import AgentBase

class SummarizeTool(AgentBase):
    def __init__(self, max_retries=3, verbose=True):
        super().__init__(name="SummarizeTool", max_retries=max_retries, verbose=verbose)

    def execute(self, text):
        messages = [
            {"role": "system", "content": "You are an AI assistant that summarizes medical texts."},
            {
                "role": "user",
                "content": f"Please provide a concise summary of the following medical text:\n\n{text}\n\nSummary:"
            }
        ]
        summary = self.call_groq(messages, max_tokens=300)  # Changed from `call_openai` to `call_groq`
        return summary
