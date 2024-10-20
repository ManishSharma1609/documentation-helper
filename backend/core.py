import os
from dotenv import load_dotenv
from langchain import hub
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_pinecone import PineconeVectorStore

load_dotenv()
INDEX_NAME = os.environ["INDEX_NAME"]


def query_LLM(query: str):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    docsearch = PineconeVectorStore(index_name=INDEX_NAME, embedding=embeddings)
    chat = ChatOpenAI(verbose=True, temperature=0)

    retrieval_qa_chat_promt = hub.pull("langchain-ai/retrieval-qa-chat")
    stuff_document_chain = create_stuff_documents_chain(chat, retrieval_qa_chat_promt)

    qa = create_retrieval_chain(
        retriever=docsearch.as_retriever(), combine_docs_chain=stuff_document_chain
    )

    result = qa.invoke(input={"input": query})
    return result


if __name__ == "__main__":
    res = query_LLM(query="What is Langchain chain?")
    print(res["answer"])
