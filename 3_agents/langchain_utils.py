from pydantic import BaseModel, Field
from langchain.agents import AgentExecutor, Tool, ZeroShotAgent, load_tools, AgentType, initialize_agent
from langchain.chains import LLMChain
from langchain.chat_models import AzureChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.tools import Tool, StructuredTool
from langchain.chains import ConversationChain
from langchain.output_parsers.retry import RetryOutputParser
from dotenv import load_dotenv, get_key, set_key

import openai
load_dotenv(dotenv_path="../.env")

deployment_id = get_key(dotenv_path="../.env", key_to_get="OPENAI_DEPLOYMENT")

tools = []


def simple_conversation(input: str):
    return "Stop and the give the Final Answer as best as you can. Final Answer can be a question to the human."


class RegistrationInput(BaseModel):
    model: str = Field(description="Vehicule model, required")
    year: int = Field(description="Car year, required")
    owner_name: str = Field(description="Car owner name, required")


def create_registration_tool(input: RegistrationInput):
    # TODO register car
    print("Registering car with input", input)
    return "AA-123-BB"


def update_registration_tool(
        registration_number: str, model: str = None, year: int = None,
        owner_name: str = None):
    # TODO update car registration
    return True


def delete_registration_tool(registration_number: str):
    # TODO delete car registration
    return True


tools.extend([
    Tool.from_function(
        func=simple_conversation,
        name="SIMPLE_CONVERSATION",
        description="Use if you want to output something to human, and if no other tool can be used.",
    ),
    Tool.from_function(
        func=create_registration_tool,
        name="CREATE_REGISTRATION",
        description="Use to create a registration. Required arguments: model, year, owner_name. Before use, output all arguments to the user and ask for confirmation. All arguments are mandatory. Outputs a registration number. The output needs to be used to answer the question.",
        # args_schema=RegistrationInput,
    ),
    Tool.from_function(
        func=update_registration_tool,
        name="UPDATE_REGISTRATION",
        description="Use to update a registration. Human must have confirmed arguments before use. Outputs true if the update succeeded, else false. The output needs to be used to answer the question.",
    ),
    Tool.from_function(
        func=delete_registration_tool,
        name="DELETE_REGISTRATION",
        description="Use to delete a registration. Human must have confirmed arguments before use. Outputs false if the update succeeded, else false. The output needs to be used to answer the question.",
    ),
])


def create_agent() -> AgentExecutor:
    prefix = """
You are an assistant for a system that manages vehicle registrations.
Have a conversation with a human, answer has best as you can.
You have access to the following tools:
    """

    format_instructions = """Use the following format:

You can only use the tools if the human has given you all the requires arguments and confirmed them. Always ask for confirmation before taking an action.
You can not use a tool if some required arguments were not given by the human.
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question or a question asking for more information
Always end with Final Answer.
    """

    suffix = """
Begin!"

===== Chat History =====
{chat_history}
========================

Question: {input}
{agent_scratchpad}
    """

    prompt = ZeroShotAgent.create_prompt(
        tools,
        prefix=prefix,
        format_instructions=format_instructions,
        suffix=suffix,
        input_variables=["input", "chat_history", "agent_scratchpad"],
    )
    memory = ConversationBufferMemory(memory_key="chat_history")
    azure_openai_chat = AzureChatOpenAI(deployment_name=get_key(dotenv_path="../.env", key_to_get="OPENAI_DEPLOYMENT"))
    llm_chain = LLMChain(llm=azure_openai_chat, prompt=prompt)
    agent = ZeroShotAgent(
        llm_chain=llm_chain, tools=tools, verbose=True,
        handle_parsing_errors=True, memory=memory)
    agent_chain = AgentExecutor.from_agent_and_tools(
        agent=agent, tools=tools, verbose=True, memory=memory, handle_parsing_errors=True, )
    return agent_chain
