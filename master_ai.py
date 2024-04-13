import os
import json
import sys

import pandas as pd
from langchain.document_loaders import DirectoryLoader

f = open('secrets.json')

data = json.load(f)
 
API_KEY = data['openapi-key']# great learning resource wasn't working, so I used my own OpenAI API key
OPENAI_API_BASE = "https://api.openai.com/v1/"

os.environ['OPENAI_API_KEY'] = API_KEY
os.environ['OPENAI_API_BASE'] = OPENAI_API_BASE

os.environ['SERPAPI_API_KEY'] = data['serpapi-key']

from scripts import master_agent, plant_agent, eda_agent, rag_agent

question = sys.argv[1]

master = master_agent.init_config()

print("init master agent")

plant = plant_agent.init_config()

print("init plant agent")

df = pd.read_csv('data/csv/plant_syn.csv')

eda = eda_agent.init_config(df)

print("init eda agent")

loader = DirectoryLoader("data/txt", glob="*.txt")

rag = rag_agent.init_config(loader)

print("init rag agent")

question_category = eval(master_agent.answer_question(master, question))

print(question_category)

if question_category['category_number'] == 1:
    response = eval(plant_agent.answer_question(plant, question))

    response = response['category_number']

    # TODO: plant_do(response)


elif question_category['category_number'] == 2:
    response = eda_agent.answer_question(eda, question)

    print(response)

elif question_category['category_number'] == 3:
    response = rag_agent.answer_question(rag, question)

    print(response)
