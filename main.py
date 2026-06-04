import logging
from fastapi import FastAPI 
import inngest
import inngest.fast_api
from dotenv import load_dotenv
import uuid
import os
import datetime
from inngest.experimental import ai
from data_loader import load_and_chunk_pdf, embed_texts
from vector_db import QdrantStorage
from custom_types import RAGChunkAndSrc, RAGUpsertResult, RAGSearchResult, RAGQueryResult

load_dotenv()

inngest_client = inngest.Inngest(
    app_id="rag-app",
    logger = logging.getLogger("uvicorn"),
    is_production=False,
    serializer= inngest.PydanticSerializer() 
    #inngest supports Pydantic typing which allows us to define types of different variables.
)

@inngest_client.create_function(
    fn_id= "RAG: Ingest PDF",
    trigger = inngest.TriggerEvent(event="rag/ingest_pdf")

)



 #Setting up the steps for the ingest function. Each step is defined as a separate function and can be executed independently. This allows for better modularity and easier debugging. The steps are defined as follows:
async def rag_ingest_pdf(ctx: inngest.Context):
    def _load(ctx:inngest.Context) -> RAGChunkAndSrc:
        pdf_path = ctx.event.data["pdf_path"]
        source_id = ctx.event.data.get("source_id", pdf_path)
        chunks = load_and_chunk_pdf(pdf_path)
        return RAGChunkAndSrc(chunks=chunks, source_id=source_id)
    
    def _upsert(chunks_and_src: RAGChunkAndSrc) -> RAGUpsertResult:
        chunks = chunks_and_src.chunks
        source_id = chunks_and_src.source_id
        vecs = embed_texts(chunks)
        ids = [str(uuid.uuid5(uuid.NAMESPACE_URL, name:= f"{source_id}: {i}")) for i in range(len(chunks))]
        payloads =[{"source_id": source_id, "text": chunks[i]} for i in range(len(chunks))]
        QdrantStorage().upsert(ids, vecs, payloads)
        return RAGUpsertResult(ingested=len(chunks))
    

    
    #calling the steps sequentially and passing the output of one step to another. Each step is also typed with the custom types we defined in custom_types.py
    chunks_and_src = await ctx.step.run("load-and-chunk", lambda: _load(ctx), output_type=RAGChunkAndSrc)
    ingested = await ctx.step.run("embed-and-upsert", lambda: _upsert(chunks_and_src), output_type=RAGUpsertResult)
    return ingested.model_dump()



@inngest_client.create_function(
    fn_id= "RAG: Query PDF",
    trigger = inngest.TriggerEvent(event="rag/query_pdf_ai")
)

async def rag_query_pdf_ai(ctx: inngest.Context):
    def _search(question:str, top_k:int = 5) -> RAGSearchResult:
        q_vec = embed_texts([question])[0]
        store = QdrantStorage()
        found = store.search(q_vec, top_k)
        return RAGSearchResult(contexts=found["contexts"], sources=found["sources"])
    
    question = ctx.event.data["question"]
    top_k = int(ctx.event.data.get("top_k", 5))

    found = await ctx.step.run("search", lambda: _search(question, top_k), output_type=RAGSearchResult)
    context_block = "\n\n".join(f" - {c}" for c in found.contexts)
    user_cotent = (
       "Use the following context to answer the question.\n\n"
       f"context:\n{context_block}\n\n "
       f"Question: {question}\n"
       "Answer concisely using the context above."
       )
    adapter = ai.OpenAIAdapter(
        auth_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4o-mini",

    )

    res = await ctx.step.ai.infer(
        "llm-answer",
        adapter= adapter,
        body ={
            "max_tokens": 1024,
            "temperature": 0.2,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant for answering questions based on the provided context."},
                {"role": "user", "content": user_cotent}
            ]       
        }
    )

    answer= res["choices"][0]["message"]["content"].strip()
    return {"answer": answer, "sources": found.sources, "num_contexts" : len(found.contexts)}

app = FastAPI()

inngest.fast_api.serve(app, inngest_client, [rag_ingest_pdf, rag_query_pdf_ai])

