import os
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from src.prompt import custom_prompt

load_dotenv()
GEMINI_KEY = os.getenv("GOOGLE_API_KEY")
os.environ["GEMINI_KEY"] = GEMINI_KEY

def url_processor(urls):
    loader = UnstructuredURLLoader(urls=urls)
    data = loader.load()
    doc_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1100,
        chunk_overlap=200)
    doc_chunks = doc_splitter.split_documents(data)

    return doc_chunks


def llm_pipeline(urls, store_path="Vector_store"):
    # Define file paths
    index_file = os.path.join(store_path, "index.faiss")
    pkl_file = os.path.join(store_path, "index.pkl")
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001", google_api_key=GEMINI_KEY
    )
    # Ensure directory exists
    os.makedirs(store_path, exist_ok=True)

    # Load or create FAISS vector store
    if os.path.exists(index_file):
        vector_store = FAISS.load_local(store_path, embeddings, allow_dangerous_deserialization=True)
        print("Loaded existing vector store.")
    else:
        print("Creating new vector store...")
        doc_chunks = url_processor(urls)
        vector_store = FAISS.from_documents(doc_chunks, embeddings)
        vector_store.save_local(store_path)
        print("Vector store saved.")

    gemini_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-preview-04-17",
                                        temperature=0.7, top_p=0.85, google_api_key=GEMINI_KEY)


    chat_chain = RetrievalQA.from_chain_type(
        llm=gemini_llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(),
        chain_type_kwargs={"prompt": custom_prompt}
    )
    return chat_chain

