from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.agents import load_tools
from langchain_openai import ChatOpenAI

def init_config():

    search_tool = load_tools(['serpapi'])
    
    tools = [search_tool[0]]

    prompt = hub.pull("hwchase17/openai-tools-agent")

    llm = ChatOpenAI(model="gpt-4", temperature=0)

# Construct the OpenAI Tools agent
    agent = create_openai_tools_agent(llm, tools, prompt)

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    return agent_executor

def answer_question(agent, question):

    full_prompt = f"""
                You are a master AI that can control other AI agents. You are specifically designed to automate plant maintenance.
                You will recieve a prompt from a user regarding plant maintenance, and will have to classify the prompt's purpose as one of the following categories:
                [0] Fertilizing the plant
                [1] Turning plant lights on
                [2] Turning plant lights off
                [3] Watering the plant

                Return the category number and name of the prompt in a JSON format.

                User: {question}
    """

    return agent.invoke({"input": full_prompt})['output']
