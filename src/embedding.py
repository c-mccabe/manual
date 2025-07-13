from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from typing import List
from tqdm import tqdm
import tiktoken

PRICE_PER_MILLION = 0.02  # $0.02 per 1M tokens for text-embedding-3-small

def count_tokens(text: str, model: str = "text-embedding-3-small") -> int:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def embed_chunks(chunks: List[str], persist_directory: str = "./chroma_store") -> Chroma:
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    print("📏 Counting tokens...")
    total_tokens = sum(count_tokens(chunk) for chunk in chunks)
    estimated_cost = (total_tokens / 1_000_000) * PRICE_PER_MILLION
    print(f"🔢 Total tokens: {total_tokens}")
    print(f"💸 Estimated embedding cost: ${estimated_cost:.4f}")

    print("📦 Embedding and storing chunks...")
    vectorstore = Chroma.from_texts(
        texts=tqdm(chunks),
        embedding=embeddings,
        persist_directory=persist_directory
    )
    vectorstore.persist()
    return vectorstore
