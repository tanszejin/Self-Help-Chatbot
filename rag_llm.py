import os
import errno
from dotenv import load_dotenv
load_dotenv('./.env')
from langchain_groq import ChatGroq
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

groq_api_key = process.env.GROQ_API_KEY
chat = ChatGroq(temperature=0,
                api_key=groq_api_key,
                model_name="mixtral-8x7b-32768")
embed_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
chroma_vector_store = Chroma(persist_directory="./chroma_db",embedding_function=embed_model)

class RAG_LLM:
    def __init__(self, k: int = 3):
        self.k = k
        self.messages = [
            SystemMessage(content="""You are a helpful assistant. 
                        Answer the queries according to the books given, but do not mention the book in your response.
                        If you are unable to answer from the books, say "I cannot answer based on the given books." """),
        ]

    def ask(self, query: str):
        search_results = chroma_vector_store.similarity_search(query, k=self.k)

        books = "\n".join([c.page_content for c in search_results])
        sources = [c.metadata['source'] for c in search_results]
        sources = list(set(sources))
        sources_str = ", ".join(sources)

        augmented_prompt = f"""Books: {books} \nQuery: {query}"""
        # print(f"Augmented prompt:\n{augmented_prompt}")

        self.messages.append(HumanMessage(content=augmented_prompt))

        try:
            res = chat.invoke(self.messages)
            res.content += f"\n\nSource: {sources_str}"
            # self.messages.append(res)
            return res.content
        except:
            return "Error - too many queries sent in 1 min. Please wait before asking again..."
