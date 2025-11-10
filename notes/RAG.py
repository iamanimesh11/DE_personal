# actions/query_vector_db.py

import logging
from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import Ollama

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Base project directory (one level above actions/)
BASE_DIR = Path(__file__).parent.parent  # D:\vector_document
VECTOR_DB_PATH = BASE_DIR / "vector_db"

def query_vector_db(query: str):
    try:
        # Load stored FAISS index
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        db = FAISS.load_local(str(VECTOR_DB_PATH), embeddings, allow_dangerous_deserialization=True)
        logger.info("✅ FAISS vector database loaded successfully.")
    except Exception as e:
        logger.error(f"❌ Error loading FAISS vector database: {e}")
        return None

    try:
        # Search for most relevant chunks
        docs = db.similarity_search(query, k=3)
        if not docs:
            logger.warning("⚠️ No relevant documents found.")
            return None
        context = "\n\n".join([d.page_content for d in docs])
        logger.info("📄 Retrieved context successfully.")
    except Exception as e:
        logger.error(f"❌ Error during similarity search: {e}")
        return None

    try:
        # Load LLM
        llm = Ollama(model="mistral:7b-instruct-q4_K_M")

        # Define prompt
        prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=(
                "You are a helpful assistant. Use the following context to answer the question.\n\n"
                "Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"
            ),
        ) 

        # Combine prompt + LLM into a runnable chain
        chain = prompt | llm

        # Invoke the chain
        response = chain.invoke({"context": context, "question": query})

        logger.info("💬 Answer generated successfully.")
        logger.info(f"Answer: {response}")
        return response
    except Exception as e:
        logger.error(f"❌ Error generating response from LLM: {e}")
        return None


if __name__ == "__main__":
    user_query = "Where can you go to submit an IT Helpdesk ticket? I need solution in stepwise"
    query_vector_db(user_query)
