import os

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
import os
import shutil

from langchain.vectorstores.chroma import Chroma
from langchain.embeddings import OpenAIEmbeddings

from langchain.agents.agent_toolkits import create_retriever_tool
from langchain.agents.agent_toolkits import create_conversational_retrieval_agent

from langchain.agents import load_tools

from langchain_openai import ChatOpenAI


def init_config(loader):
    # We use the loader created above to load the document
    documents = loader.load()

    # We split the document into several chunks as mentioned above
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    CHROMA_PATH = "../duke_chroma"

    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
    # Create a new DB from the documents.
    db = Chroma.from_documents(
        texts, OpenAIEmbeddings(), persist_directory=CHROMA_PATH
    )
    db.persist()
    print(f"Saved {len(texts)} chunks to {CHROMA_PATH}.")

    retriever = db.as_retriever()

    # This is the prompt to create a RAG agent for us


    retriever_name = "plant_os_pdf"
    retriever_desc = """The purpose of this tool is to answer questions about the blue indigo false plant and its maintenance."""

    rag_tool = create_retriever_tool(
        retriever,
        retriever_name,
        retriever_desc
    )

    search_tool = load_tools(['serpapi'])
    tools = [rag_tool, search_tool[0]]

    llm = ChatOpenAI(model_name="gpt-4")

    RAG_executor = create_conversational_retrieval_agent(llm=llm, tools=tools, verbose=True) # setting verbose=True to output the thought process of the agent

    return RAG_executor

def answer_question(agent, question):
    question = "what is the scientific for the plant?"
    
    user_query = {"input": question}
    
    result = agent(user_query)

    return result['output']
