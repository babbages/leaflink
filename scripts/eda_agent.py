# from langchain.agents.agent_types import AgentType
import pandas as pd

import sys

sys.path.append('..')

from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import OpenAI, ChatOpenAI
from langchain.agents.agent_types import AgentType

def init_config(df):

    llm = ChatOpenAI(model_name="gpt-4")

    agent = create_pandas_dataframe_agent(llm=llm, df=df, verbose=True)

    return agent

def answer_question(agent, question):
    return agent.invoke(question)['output']

