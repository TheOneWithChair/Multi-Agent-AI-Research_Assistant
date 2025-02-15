import groq
from abc import ABC, abstractmethod
from loguru import logger
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
client = groq.Client(api_key=groq_api_key)

class AgentBase(ABC):
    def __init__(self, name, max_retries=2, verbose=True):
        self.name = name
        self.max_retries = max_retries
        self.verbose = verbose

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass

    def call_groq(self, messages, temperature=0.7, max_tokens=150):
        retries = 0
        while retries < self.max_retries:
            try:
                if self.verbose:
                    logger.info(f"[{self.name}] Sending messages to Groq:")
                    for msg in messages:
                        logger.debug(f"  {msg['role']}: {msg['content']}")
                
                response = client.chat.completions.create(
                    model="llama3-8b-8192",  # Updated to Llama 3
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                reply = response.choices[0].message
                
                if self.verbose:
                    logger.info(f"[{self.name}] Received response: {reply}")
                
                return reply
            except Exception as e:
                retries += 1
                logger.error(f"[{self.name}] Error during Groq call: {e}. Retry {retries}/{self.max_retries}")
        
        raise Exception(f"[{self.name}] Failed to get response from Groq after {self.max_retries} retries.")
