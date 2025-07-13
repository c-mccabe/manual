from src.query import query_manual

from dotenv import load_dotenv


load_dotenv()

QUERY = ("My camera's blurry, how can I fix that?")

if __name__ == "__main__":
    response = query_manual(QUERY, persist_directory="./chroma_store")
    print("Answer:")
    print(response["answer"])
    print("Source:")
    print(response["sources"][0])
    print(f"number of sources: {len(response['sources'])}")