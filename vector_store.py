# Package imports
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.retrievers import BM25Retriever

# Import the read module
from read import read

# Initialize the text splitter
text_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n"],
    chunk_size=1250,
    chunk_overlap=250
)

# Initialize SentenceTransformer embeddings
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")


def create_new_collection_streamlit(collection_name_str=None, pdf_file=None):

     # Convert PDF to text
    read([f'{pdf_file}.pdf'])


    # Load the document and split it into chunks
    loader = TextLoader(f'{pdf_file}.txt')
    documents = loader.load()

    # Apply the text splitter to the documents
    splits = text_splitter.split_documents(documents)

    return splits


def load_BM25Retriever(filepath):


    # Load the document and split it into chunks
    # loader = TextLoader(f'{filepath}.txt')
    loader = TextLoader(f"data/{filepath}")
    documents = loader.load()

    # Apply the text splitter to the documents
    splits = text_splitter.split_documents(documents)

    return BM25Retriever.from_documents(splits)   