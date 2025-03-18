import gradio as gr
from agents import Agent, Runner
import asyncio

# Initialize the agent
agent = Agent(name="Assistant", instructions="You are a helpful assistant")

# Async function to process user queries
async def process_query_async(message):
    # Use the async version directly
    response = await Runner.run(agent, message)
    return response

# Wrapper function that creates a new event loop for the async operation
def process_query(message):
    # Create a new event loop for this thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        # Run the async function in the loop
        result = loop.run_until_complete(process_query_async(message))
        # Extract final_output from the result object
        return result.final_output
    finally:
        # Clean up
        loop.close()

# Create a Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Agent Assistant")
    
    with gr.Row():
        with gr.Column():
            # Input components
            msg = gr.Textbox(
                label="Your message",
                placeholder="Type your message here...",
                lines=3
            )
            submit_btn = gr.Button("Submit", variant="primary")
            
        with gr.Column():
            # Output component
            output = gr.Markdown(label="Assistant's Response")
    
    # Set up the click event
    submit_btn.click(
        fn=process_query,
        inputs=msg,
        outputs=output
    )
    
    # Also allow submission by pressing Enter in the textbox
    msg.submit(
        fn=process_query,
        inputs=msg,
        outputs=output
    )

# Launch the Gradio app
if __name__ == "__main__":
    demo.launch()
