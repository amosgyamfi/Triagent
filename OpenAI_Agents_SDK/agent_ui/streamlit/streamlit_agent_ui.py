# pip install streamlit

import streamlit as st
import asyncio
from agents import Agent, Runner


st.title("Agent Assistant")
st.write("Enter a prompt and the agent will respond.")

# Initialize the agent with the API key
agent = Agent(
    name="Assistant", 
    instructions="You are a helpful assistant",
)

# Create a text input for the user's prompt
user_prompt = st.text_area("Enter your prompt:", "Write a haiku about recursion in programming.")

# Create a button to submit the prompt
if st.button("Submit"):
    with st.spinner("Agent is thinking..."):
        # Fix for asyncio event loop in threaded environment
        try:
            # Create a new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Run the agent with the user's prompt
            result = loop.run_until_complete(Runner.run(agent, user_prompt))
        finally:
            # Clean up
            loop.close()
    
    # Display the result
    st.write("### Response")
    st.write(result.final_output)
