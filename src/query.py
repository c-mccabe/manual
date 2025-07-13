from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.chains import create_retrieval_chain


SYSTEM_PROMPT = "You are a concise and helpful product support assistant. Keep answers short and focused."
MODEL = "gpt-4o"

def load_vectorstore(persist_directory: str = "./chroma_store") -> Chroma:
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    return Chroma(persist_directory=persist_directory, embedding_function=embeddings)

def query_manual(question: str, persist_directory: str = "./chroma_store") -> dict:
    # Load retriever
    vectorstore = load_vectorstore(persist_directory)
    retriever = vectorstore.as_retriever()

    # Prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "Use the following context to answer the question.\n\nContext:\n{context}\n\nQuestion: {input}")
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
    result = retrieval_chain.invoke({"input": question})

    retrieved_docs = retriever.invoke(question)
    retrieved_texts = [doc.page_content for doc in retrieved_docs]

    return {
        "answer": result["answer"].content,
        "sources": retrieved_texts
    }
