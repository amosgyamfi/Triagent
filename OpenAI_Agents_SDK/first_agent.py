from agents import Agent, Runner

agent = Agent(name="Assistant", instructions="You are a helpful assistant")

result = Runner.run_sync(agent, "Write a simple SwiftUI animation that moves a rectangle from point a to b repeatedly.")

print(result.final_output)
