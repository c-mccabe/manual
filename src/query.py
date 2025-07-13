from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

def load_vectorstore(persist_directory: str = "./chroma_store") -> Chroma:
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    return Chroma(persist_directory=persist_directory, embedding_function=embeddings)

def query_manual(question: str, persist_directory: str = "./chroma_store") -> str:
    vectorstore = load_vectorstore(persist_directory)
    retriever = vectorstore.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(temperature=0),
        retriever=retriever
    )
    return qa_chain.run(question)
