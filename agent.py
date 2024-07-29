import os
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langsmith import traceable
from langchain_community.tools.shell.tool import ShellTool
from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from tools import *
from prompts import *
from dotenv import load_dotenv

# Ensure ffmpeg path is set if needed
os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/local/bin/ffmpeg"  

# Load environment variables from a .env file
load_dotenv()

# Function to create an agent with the specified tools and system prompt
def create_agent(tools, system_prompt):
    llm = ChatOpenAI(model="gpt-4o", temperature=0)  # Initialize the language model (LLM) with GPT-4 and temperature 0
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),  # System message
            ("user", "{input}"),  # User input message placeholder
            MessagesPlaceholder(variable_name="agent_scratchpad"),  # Placeholder for intermediate steps (scratchpad)
        ]
    )
    llm_with_tools = llm.bind_tools(tools)  # Bind the tools to the LLM
    agent = (
        {
            "input": lambda x: x["input"],  # Input message
            "agent_scratchpad": lambda x: format_to_openai_tool_messages(x["intermediate_steps"]),  # Format intermediate steps
        }
        | prompt  # Combine the input with the prompt
        | llm_with_tools  # Add the LLM with tools
        | OpenAIToolsAgentOutputParser()  # Add the output parser
    )
    return AgentExecutor(agent=agent, tools=tools, verbose=True)  # Return the agent executor with the agent and tools

# Define the tools for the agent
tdm_tools = [
    ShellTool(ask_human_input=True), 
    extract_video_transcript,  # Custom tool to extract video transcript
    summarize_transcript,  # Custom tool to summarize the transcript
    
]

# Create an agent executor with the defined tools and prompt
tdm_agent_executor = create_agent(tdm_tools, TDM_PROMPT)

if __name__ == "__main__":
    try:
        iteration_count = 0  # Initialize iteration counter
        user_prompt = input("Please provide the video path: ")  # Get user input for video path
        while iteration_count < 5:  # Loop up to 5 iterations
            try:
                # Execute the agent with the provided input and get the last output
                tdm_output = list(tdm_agent_executor.stream({"input": user_prompt}))[-1]['output']
                print(f"TDM output: {tdm_output}")  # Print the output
            except AttributeError as e:
                print(f"An error occurred: {e}")  # Handle errors
            iteration_count += 1  # Increment the iteration counter
        
        print(f"Finished the program after {iteration_count} iterations.")  # Print when the program finishes
    except KeyboardInterrupt:
        print("\nExiting the program.") 