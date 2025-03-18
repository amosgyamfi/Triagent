import streamlit as st
import asyncio
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI
from openai.types.responses import ResponseTextDeltaEvent

# Initialize the model and agent
local_model = OpenAIChatCompletionsModel(
    model="deepseek-r1:8b",
    openai_client=AsyncOpenAI(base_url="http://localhost:11434/v1")
)

agent = Agent(
    name="Assistant",
    instructions="You are a helpful reasoning assistant who can help with a wide range of questions and answers only in English",
    model=local_model
)

# Set up the Streamlit page
st.title("AI Assistant")
st.write("Enter your question and deepseek-r1:8b will respond in real-time.")

# Create a text input for the user's message
user_input = st.text_area("Your question:", "")

async def stream_response(prompt):
    # Create a placeholder for the streaming output
    response_placeholder = st.empty()
    full_response = ""
    
    # Stream the response
    result = Runner.run_streamed(agent, prompt)
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            # Append new text to the full response
            full_response += event.data.delta
            # Update the placeholder with the accumulated text
            response_placeholder.markdown(full_response)

# Handle the submit button
if st.button("Submit") and user_input:
    # Create a spinner while waiting for the response
    with st.spinner("Thinking..."):
        # Run the async function in a way that works with Streamlit
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(stream_response(user_input))
        finally:
            loop.close()