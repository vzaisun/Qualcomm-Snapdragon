import asyncio
import os
import re
import yaml

# Assuming ModelInterface and Tool are defined in src.model and src.tools respectively
from src.model import ModelInterface
from src.tools import Tool

class Agent:
    # Added type hints for clarity
    def __init__(self, tools: list[Tool], identity: str):
        # The 'config.yaml' file needs to exist for this to work
        try:
            with open("config.yaml", "r") as f:
                self.config = yaml.safe_load(f)
        except FileNotFoundError:
            print("Warning: config.yaml not found. Proceeding with default behavior.")
            self.config = {}
        
        self.model = ModelInterface()
        self.tools = {tool.name: tool for tool in tools}
        self.core_identity = identity

    def run(self):
        print("Type 'exit' to end the chat.")

        while True:
            user_input = input("You: ").strip()
            if user_input.lower() in {"exit"}:
                print("Bye!")
                break
            # Awaiting the asynchronous chat_completion function within the synchronous run loop
            result = asyncio.run(self.chat_completion(user_input))
            # Fixed the f-string syntax
            print(f"Agent: {result}")

    # Renamed the first argument from 'seld' to 'self'
    async def chat_completion(self, user_input):
        messages = self._build_prompt(user_input)

        # Corrected the regex pattern and function call
        tool_call_pattern = re.compile(
            r"^(\w+)\((.*)\)$",  # Changed \\W+ to \\w+ for function names, and used single backslashes
            re.DOTALL
        )
        response = self.model.chat_completion(messages)
        match = tool_call_pattern.match(response.strip())

        result = ""
        if match: # call a tool
            name, arg = match.groups()
            tool = self.tools.get(name)
            if tool:
                response_from_tool = tool.run(arg) if arg else tool.run("")
                # Added code to handle the tool's response (e.g., return it)
                result = f"Tool '{name}' executed. Response: {response_from_tool}"
            else:
                result = f"Error: Unknown tool '{name}'."
        else:
            # If no tool call was matched, the response is the direct chat output
            result = response
            
        return result # Ensure the function always returns a value

    def _build_prompt(self, user_input):
        messages = [
            {"role" : "system",
             # Fixed the attribute access (added self.) and closing quote
             "content": self.core_identity
             }
        ]
        # Fixed dictionary key/value syntax and proper variable access
        messages.append({
            "role": "user",
            "content": user_input # Use user_input here, not self.core_identity
        })
        
        return messages # Ensure the function returns the built list
