# agents/sanitize_data_validator_agent.py

from .agent_base import AgentBase

class SanitizeDataValidatorAgent(AgentBase):
    def __init__(self, max_retries=2, verbose=True):
        super().__init__(name="SanitizeDataValidatorAgent", max_retries=max_retries, verbose=verbose)

    def execute(self, original_data, sanitized_data):
        messages = [
            {
                "role": "system",
                "content": "You are an AI assistant that validates the sanitization of medical data by ensuring all Protected Health Information (PHI) is removed."
            },
            {
                "role": "user",
                "content": (
                    "Compare the original data and the sanitized data to verify if all **Protected Health Information (PHI)** has been successfully removed.\n"
                    "- Identify and list any remaining PHI elements.\n"
                    "- Assess the effectiveness of sanitization and provide an **overall rating (1-5)**, where **5** indicates complete sanitization.\n\n"
                    f"**Original Data:**\n{original_data}\n\n"
                    f"**Sanitized Data:**\n{sanitized_data}\n\n"
                    "**Sanitization Validation Report:**"
                )
            }
        ]
        validation = self.call_groq(
            messages=messages,
            temperature=0.3,
            max_tokens=512
        )
        return validation
# from .agent_base import AgentBase

# class SanitizeDataValidatorAgent(AgentBase):
#     def __init__(self, max_retries=2, verbose=True):
#         super().__init__(name="SanitizeDataValidatorAgent", max_retries=max_retries, verbose=verbose)

#     def execute(self, original_data, sanitized_data):
#         messages = [
#             {
#                 "role": "system",
#                 "content": (
#                     "You are an AI assistant that validates the sanitization of medical data by ensuring all Protected Health Information (PHI) is removed.\n"
#                     "Generate a **structured validation report** that includes:\n"
#                     "- **Validation Status** (Pass/Fail)\n"
#                     "- **List of any remaining PHI elements** (if found)\n"
#                     "- **Sanitization Rating (1-5 stars)**\n"
#                     "- **Recommendations** for improving sanitization."
#                 )
#             },
#             {
#                 "role": "user",
#                 "content": (
#                     f"Compare the original data and the sanitized data to verify if all **Protected Health Information (PHI)** has been successfully removed.\n\n"
#                     f"**Original Data:**\n{original_data}\n\n"
#                     f"**Sanitized Data:**\n{sanitized_data}\n\n"
#                     "Generate a structured **Sanitization Validation Report:**"
#                 )
#             }
#         ]

#         response = self.call_groq(
#             messages=messages,
#             temperature=0.3,
#             max_tokens=512
#         )

#         # ✅ Extract the actual text response correctly
#         validation_text = response.content if hasattr(response, "content") else str(response)

#         return validation_text.strip()
