from .agent_base import AgentBase

class SanitizeDataTool(AgentBase):
    def __init__(self, max_retries=3, verbose=True):
        super().__init__(name="SanitizeDataTool", max_retries=max_retries, verbose=verbose)

    def execute(self, medical_data):
        messages = [
            {"role": "system", "content": "You are an AI assistant that sanitizes medical data by removing Protected Health Information (PHI)."},
            {
                "role": "user",
                "content": f"Remove all PHI from the following data:\n\n{medical_data}\n\nSanitized Data:"
            }
        ]
        sanitized_data = self.call_groq(messages, max_tokens=500)  # ✅ Changed from `call_openai` to `call_groq`
        return sanitized_data
