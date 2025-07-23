from langchain.chains import RetrievalQA
from langchain_community.document_loaders import TextLoader
# from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_community.llms import OpenAI
from langchain_openai import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import json_loader, YoutubeLoader, PyPDFium2Loader
from langchain_community.document_loaders.csv_loader import CSVLoader
from secret_keys import openaiapi_key
import os
import warnings
warnings.filterwarnings('ignore')

os.environ['OPENAI_API_KEY'] = openaiapi_key

def merch_func(input_query):
    loader1 = PyPDFium2Loader(file_path="MFCS24.1.401.0.pdf")
    data1 = loader1.load()

    text_splitter1 = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts1 = text_splitter1.split_documents(data1)

    embeddings1 = OpenAIEmbeddings(openai_api_key=openaiapi_key,model="text-embedding-3-large")
    llm1 = OpenAI(temperature=0.7)

    docsearch1 = Chroma.from_documents(texts1, embeddings1)
    qa1 = RetrievalQA.from_chain_type(llm=llm1, chain_type="stuff", retriever=docsearch1.as_retriever())
    return qa1.invoke(input_query)

def pricing_func(input_query):
    loader2 = PyPDFium2Loader(file_path="PRICING23.1.401.0.pdf")
    data2 = loader2.load()

    text_splitter2 = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts2 = text_splitter2.split_documents(data2)

    embeddings2 = OpenAIEmbeddings(openai_api_key=openaiapi_key,model="text-embedding-3-large")
    llm2 = OpenAI(temperature=0.7)

    docsearch2 = Chroma.from_documents(texts2, embeddings2)
    qa2 = RetrievalQA.from_chain_type(llm=llm2, chain_type="stuff", retriever=docsearch2.as_retriever())
    return qa2.invoke(input_query)

def rds_func(input_query):
    loader3 = PyPDFium2Loader(file_path="RDS_Implementation.pdf")
    data3 = loader3.load()

    text_splitter3 = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts3 = text_splitter3.split_documents(data3)

    embeddings3 = OpenAIEmbeddings(openai_api_key=openaiapi_key,model="text-embedding-3-large")
    llm3 = OpenAI(temperature=0.7)

    docsearch3= Chroma.from_documents(texts3, embeddings3)
    qa3 = RetrievalQA.from_chain_type(llm=llm3, chain_type="stuff", retriever=docsearch3.as_retriever())
    return qa3.invoke(input_query)

