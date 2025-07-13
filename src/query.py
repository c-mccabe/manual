from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.chains import create_retrieval_chain


SYSTEM_PROMPT = "You are a concise and helpful product support assistant. Keep answers short and focused."
MODEL = "gpt-4o"

def load_vectorstore(persist_directory: str = "./chroma_store") -> Chroma:
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    return Chroma(persist_directory=persist_directory, embedding_function=embeddings)

def query_manual(input: str, persist_directory: str = "./chroma_store") -> str:
    # Load retriever
    vectorstore = load_vectorstore(persist_directory)
    retriever = vectorstore.as_retriever()

    # Prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{input}")
    ])

    # LLM
    llm = ChatOpenAI(
        temperature=0.15,
        max_tokens=750,
        model=MODEL
    )

    # Build runnable chain
    chain = prompt | llm

    # Build retrieval chain
    retrieval_chain = create_retrieval_chain(retriever, chain)

    # Run with input dict (note: question is key)
    result = retrieval_chain.invoke({"input": input})
    return result["answer"].content
