from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.messages import HumanMessage, AIMessage
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain_community.embeddings import OpenAIEmbeddings

import os
import openai

CHROMA_PATH = "./chroma_db"


def create_chain(vectorStore):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

    qa_system_prompt = """"Answer the user's questions based on the context:
    {context}"""

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ]
    )

    chain = create_stuff_documents_chain(llm=llm, prompt=prompt)

    retriever = vectorStore.as_retriever(search_kwargs={"k": 1})

    contextualize_q_system_prompt = """You are a data engineer, given the above conversation, \
    create a search query to retrieve relevant information \
    to answer the interview. \
    The answer should be concise.\
    """

    retriever_prompt = ChatPromptTemplate.from_messages(
        [
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            ("human", contextualize_q_system_prompt),
        ]
    )

    history_aware_retriever = create_history_aware_retriever(
        llm=llm, retriever=retriever, prompt=retriever_prompt
    )

    retrieval_chain = create_retrieval_chain(history_aware_retriever, chain)

    return retrieval_chain


def process_chat(chain, question, chat_history):

    response = chain.invoke({"input": question, "chat_history": chat_history})
    return response["answer"]


def conversation(user_input):
    vectorStore = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=OpenAIEmbeddings()
    )
    chain = create_chain(vectorStore)

    chat_history = []

    while True:
        response = process_chat(chain, user_input, chat_history)
        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(AIMessage(content=response))

        print("Assistant:", response)
