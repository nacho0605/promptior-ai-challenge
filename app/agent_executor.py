from langchain import hub
from langchain.agents import create_openai_functions_agent
from langchain.agents import AgentExecutor
from langchain.tools.retriever import create_retriever_tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


def get_agent_executor(context):

    text_splitter = RecursiveCharacterTextSplitter()
    text = text_splitter.split_text(context)
    embeddings = OpenAIEmbeddings()
    vector = FAISS.from_texts(text, embeddings)

    retriever = vector.as_retriever()

    retriever_tool = create_retriever_tool(
        retriever,
        "promptior_search",
        "Buscar información sobre Promptior",
    )

    search = TavilySearchResults()

    tools = [retriever_tool, search]

    prompt = hub.pull("hwchase17/openai-functions-agent")
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    agent = create_openai_functions_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    return agent_executor
