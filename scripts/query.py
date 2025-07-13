from src.query import query_manual

from dotenv import load_dotenv


load_dotenv()

QUERY = ("I'm having issues with my phone's camera - it's always quite blurry. Can you help?")

if __name__ == "__main__":
    response = query_manual(QUERY, persist_directory="./chroma_store")
    print(response)