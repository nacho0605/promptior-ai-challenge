from agent_executor import get_agent_executor
from retrieval_chain import get_retrieval_chain
from schemas import Input, Output
from utils import gather_promptior_context
from fastapi import FastAPI
from langchain.cache import SQLiteCache
from langchain.globals import set_llm_cache
from langserve import add_routes

import uvicorn


set_llm_cache(SQLiteCache(database_path=".langchain.db"))


promptior_context = gather_promptior_context()


app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple API server using LangChain's Runnable interfaces",
)


retrieval_chain = get_retrieval_chain(promptior_context)
add_routes(
    app,
    retrieval_chain.with_types(input_type=Input, output_type=Output),
    path="/retrieval-chain",
)


agent_executor = get_agent_executor(promptior_context)
add_routes(
    app,
    agent_executor.with_types(input_type=Input, output_type=Output),
    path="/agent",
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
