from src.query import query_manual

from dotenv import load_dotenv


load_dotenv()

QUERY = ("How can I block a spam message?")

if __name__ == "__main__":
    response = query_manual(QUERY, persist_directory="./chroma_store")
    print(response)