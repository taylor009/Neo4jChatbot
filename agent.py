from langchain.agents import AgentType, initialize_agent
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from llm import llm
from langchain.tools import Tool
import streamlit as st

from tools.vector import kg_qa

tools = [
    Tool.from_function(
        name="Vector Search Index",  # (1)
        description="Provides information about movie plots using Vector Search",  # (2)
        func=kg_qa,  # (3)
    )
]

memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k=5,
    return_messages=True,
)


def generate_response(prompt):
    """
    Create a handler that calls the Conversational agent
    and returns a response to be rendered in the UI
    """

    response = agent(prompt)

    return response['output']


# SYSTEM_MESSAGE = """
# You are a movie expert providing information about movies.
# Be as helpful as possible and return as much information as possible.
# Do not answer any questions that do not relate to movies, actors or directors.
#
# Do not answer any questions using your pre-trained knowledge, only use the information provided in the context.
# """

agent = initialize_agent(
    tools,
    llm,
    memory=memory,
    verbose=True,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    # agent_kwargs={"system_message": SYSTEM_MESSAGE}
)

user_input = st.chat_input('Chat Input')
st.write(f'You typed: {user_input}')
