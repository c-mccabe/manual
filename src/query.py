from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

MODEL = "gpt-4o"

def load_vectorstore(persist_directory: str = "./chroma_store") -> Chroma:
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    return Chroma(persist_directory=persist_directory, embedding_function=embeddings)

def query_manual(question: str, persist_directory: str = "./chroma_store") -> str:
    vectorstore = load_vectorstore(persist_directory)
    retriever = vectorstore.as_retriever()
    llm = ChatOpenAI(temperature=0.1, max_tokens=250, model=MODEL)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever
    )
    return qa_chain.run(question)
