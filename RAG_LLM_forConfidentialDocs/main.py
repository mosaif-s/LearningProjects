from dotenv import load_dotenv, find_dotenv
import os

from openai import vector_stores
from pinecone.core.openapi.db_control.model.serverless_spec import ServerlessSpec

load_dotenv(find_dotenv(), override=True)
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY


import warnings
warnings.filterwarnings("ignore")
warnings.showwarning = lambda *args, **kwargs: None

def load_document(file):
    name, extension=file.split('.')
    if extension=='pdf':
        from langchain.document_loaders import PyPDFLoader
        print(f"Loading {file}")
        loader=PyPDFLoader(file)
    elif extension=='docx':
        from langchain.document_loaders import Docx2txtLoader
        print(f"Loading {file}")
        loader=Docx2txtLoader(file)
    else:
        print("Document extension not supported (yet hahaha")
        return

    data=loader.load()
    return data

def chunk_data(data, chunk_size=256):
    from langchain.text_splitter import  RecursiveCharacterTextSplitter
    splitter=RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=0) #get to know more anout the arguements
    chunks=splitter.split_documents(data)
    return chunks


def print_embedding_costs(texts):
    import tiktoken
    enc=tiktoken.encoding_for_model('text-embedding-ada-002')
    total_tokens=sum([len(enc.encode(page.page_content)) for page in texts])
    print(f"Total tokens: {total_tokens}")
    print(f"Embedding Cost in USD: {total_tokens/1000*0.0004:.6f}")

def insert_or_fetch_embeddings(index_name,chunks):
    from langchain_openai import OpenAIEmbeddings
    import pinecone
    from langchain_community.vectorstores import Pinecone
    from langchain_pinecone import PineconeVectorStore
    from pinecone import ServerlessSpec

    pc=pinecone.Pinecone(api_key=PINECONE_API_KEY)
    embeddings=OpenAIEmbeddings(model='text-embedding-3-small', dimensions=1536)
    if index_name in pc.list_indexes().names():
        print(f"Index {index_name} already exists. Loading embeddings...", end='')
        print('Ok')
        return PineconeVectorStore(index=pc.Index(index_name),embedding=embeddings)
    else:
        print(f"Creating index {index_name} and embeddings ...", end='')
        pc.create_index(
            name=index_name,
            dimension=1536,
            metric='cosine',
            spec=ServerlessSpec(cloud='aws',region='us-east-1')
        )
    index = pc.Index(index_name)
    vector_store = PineconeVectorStore(index=index, embedding=embeddings)
    vector_store.add_documents(documents=chunks)
    print('Ok')
    return vector_store

def delete_pinecone_index(index_name='all'):
    import pinecone
    pc=pinecone.Pinecone()
    if index_name=='all':
        indexes=pc.list_indexes().names()
        for index in indexes:
            pc.delete_index(index)
        print('Ok')
    else:
        print(f"Deleting index {index_name} ....", end="")
        pc.delete_index(index_name)
        print('Ok')

def ask_and_get_answer(vector_store, q):
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import PromptTemplate
    from langchain.chains import RetrievalQA # it was not a model , why ids
    from langchain.chains import ConversationalRetrievalChain
    from langchain.memory import ConversationBufferMemory

    llm=ChatOpenAI(model='gpt-3.5-turbo', temperature=1)
    retriever=vector_store.as_retriever(search_type='similarity',search_kwargs={'k':3})
    custom_prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
    You are an assistant for the user's private documents. Use the context below to answer the question.
    Only use the context. If you don’t know, say so.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
    )

    #chain=RetrievalQA.from_chain_type(llm=llm,retriever=retriever,chain_type='stuff', chain_type_kwargs={"prompt":custom_prompt})
    memory=ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    crc=ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        chain_type='stuff',
        verbose=False
    )
    #answer=chain.run(q)
    answer = crc.invoke({'question':q})
    return answer['answer']

def runLoop(vector_store):
    import time
    i=1
    while True:
        q=input(f"Question {i}: ")
        i=i+1
        if q.lower() in ['quit','bye']:
            print("Alright! Thanks for chatting!")
            time.sleep(2)
            break
        else:
            answer=ask_and_get_answer(vector_store, q)
            print(f'Answer: {answer}')
            print('-'*50)

data=load_document('21220405_ThePaperSon_Assign1.pdf')
chunks=chunk_data(data)
print_embedding_costs(chunks)
#delete_pinecone_index()
index_name='askadocument'
vector_store=insert_or_fetch_embeddings(index_name,chunks)
runLoop(vector_store)

