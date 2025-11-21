from datetime import datetime

class Tool:
    def __init__(self,name=str,func=callable,description=str):
        self.name=name
        self.func=func
        self.description=description

    def run(self,arg=str):
        return self.func(arg) if arg!='' else self.func()
    

def time_tool():
        now = datetime.now()
        formatted_string = f"The current time is {now.strftime('%I:%M %p')} on {now.strftime('%A, %B %d, %Y')}"
        return formatted_string
    
tools=[
        Tool(
            "Time",
            time_tool,
            "Prints current date and time"
        )
    ]

tool_descriptions="\n".join(f" -{tool.name}:{tool.description}" for tool in tools)