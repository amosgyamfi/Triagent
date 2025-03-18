from agents import Agent, function_tool, Runner

@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny"

agent = Agent(
    name="Weather agent",
    instructions="Always respond with reliable weather information",
    model="o3-mini",
    tools=[get_weather],
)

output = Runner.run_sync(
    starting_agent=agent,
    input="What is the weather in Helsinki, Finland?",
)
print(output)