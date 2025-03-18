from agents import Agent, ModelSettings, function_tool, Runner

@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny"

agent = Agent(
    name="Haiku agent",
    instructions="Always respond in haiku form",
    model="o3-mini",
    tools=[get_weather],
    model_settings=ModelSettings(
        model="o3-mini",
        temperature=0.5,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    ),
)

output = Runner.run_sync(
    starting_agent=agent,
    input="What is the weather in Tokyo?",
)
print(output)