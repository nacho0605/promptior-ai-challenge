from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


def get_retrieval_chain(context):

    llm = ChatOpenAI()

    text_splitter = RecursiveCharacterTextSplitter()
    text = text_splitter.split_text(context)
    embeddings = OpenAIEmbeddings()
    vector = FAISS.from_texts(text, embeddings)

    prompt = ChatPromptTemplate.from_template(
        """
        Answer the following question based only on the provided context:

        <context>
        {context}
        </context>

        Question: {input}
        """
    )

    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = vector.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    return retrieval_chain
