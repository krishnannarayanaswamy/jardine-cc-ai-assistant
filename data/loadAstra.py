from langchain_openai import OpenAIEmbeddings
from langchain_astradb import AstraDBVectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
#from langchain_community.document_loaders import UnstructuredFileLoader
import glob
from pathlib import Path
import json
#from langchain_community.document_loaders import UnstructuredMarkdownLoader
#from unstructured.partition.text import partition_text
#from unstructured.cleaners.core import group_broken_paragraphs

import os

token=os.environ['ASTRA_DB_APPLICATION_TOKEN']
api_endpoint=os.environ['ASTRA_DB_API_ENDPOINT']
keyspace=os.environ['ASTRA_DB_KEYSPACE']
openai_api_key=os.environ["OPENAI_API_KEY"]

vstore = AstraDBVectorStore(
    embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
    collection_name="jardinecc_chatbot",
    api_endpoint=api_endpoint,
    token=token,
)

text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size = 4096,
    chunk_overlap  = 64,
    length_function = len,
    is_separator_regex = False,
)

directory = 'files'
ids = []
llmtexts = []
#book = []
#section = []
source = []
for filename in glob.glob(directory + '/*.txt'):
    with open(filename) as f:
        #head, tail = os.path.split(filename)
        #name, extension = os.path.split(tail) 
        file_section = Path(filename).stem
        contents = f.read()
        text = contents.replace('\n\n', '')
        text = text.replace('\n', '')
        llmtexts.append(text)
        ids.append(file_section)
        #book.append("10002000123")
        #section.append(file_section)
        source.append(filename)
        
        #metadatas = metadatas.append(json_data)
        #print(json_data)

metadatas = [{"source": t } for t in zip(source)]


#print (metadatas)
#print(llmtexts)
#print(ids)
#print(metadatas)

inserted_ids = vstore.add_texts(texts=llmtexts, metadatas=metadatas, ids=ids)
print(f"\nInserted {len(inserted_ids)} documents.")


#loader = UnstructuredFileLoader("captions/10002000123376.txt")
#docs = loader.load()
#chunks = partition_text(filename="captions/10002000123376.txt", chunking_strategy="basic", paragraph_grouper=group_broken_paragraphs)
#chunks = chunk_elements(elements)
#markdown_path = "captions/10002000123376.txt"
#loader = UnstructuredMarkdownLoader(markdown_path)
#data = loader.load()

#loader = TextLoader("captions/100020001235.txt")
#docs = loader.load()
#texts = text_splitter.split_documents(docs)



#for chunk in chunks[:20]:
#    print(chunk)
#    print("\n")
#print(texts)




