import asyncio
import chainlit as cl
from agents import Agent, Runner

# Initialize the agent
agent = Agent(name="Assistant", instructions="You are a helpful assistant")

@cl.on_message
async def on_message(message: cl.Message):
    """Process incoming user messages"""
    user_input = message.content
    
    # Show a temporary thinking message
    await cl.Message(content="Thinking...").send()
    
    try:
        # Run the agent asynchronously
        result = await Runner.run(agent, user_input)
        
        # Extract the content from the result object
        if hasattr(result, 'content'):
            response_content = result.content
        elif hasattr(result, 'text'):
            response_content = result.text
        else:
            response_content = str(result.final_output)
        
        # Send a new message with the response instead of updating
        await cl.Message(content=response_content).send()
        
    except Exception as e:
        # Handle any errors by sending a new message
        await cl.Message(content=f"Error: {str(e)}").send()

@cl.on_chat_start
async def on_chat_start():
    """Runs when a new chat session starts"""
    # Send a welcome message
    await cl.Message(
        content="Hello! I'm your AI assistant. How can I help you today?"
    ).send()
