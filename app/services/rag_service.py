from typing import Any, List
from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_core.language_models import BaseLLM
from langchain_core.outputs import LLMResult, Generation
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from app.services.chroma_service import retrieve_chunks
from app.services.groq_service import generate_response
from app.core.logger import logger

# 1.  RETRIEVER

class ChromaRetriever(BaseRetriever):
    """
    LangChain retriever backed by the project's
    existing ChromaDB collection.
    """

    call_id: int

    class Config:
        arbitrary_types_allowed = True

    def _get_relevant_documents(self, query: str,**kwargs: Any) -> List[Document]:
        
        try:
            chunks: list[str] = retrieve_chunks(
                call_id=self.call_id,
                query=query
            )
        except Exception:
            logger.exception(
        f"Chunk retrieval failed. call_id={self.call_id}"
    )
            raise

        return [
            Document(page_content=chunk)
            for chunk in chunks
        ]

    async def _aget_relevant_documents(self,query: str,**kwargs: Any) -> List[Document]:

        return self._get_relevant_documents(query)


# 2.  LLM WRAPPER

class GroqLLM(BaseLLM):
    """
    LangChain LLM wrapper around the project's
    existing Groq generate_response helper.
    """

    temperature: float = 0.0

    class Config:
        arbitrary_types_allowed = True

    @property
    def _llm_type(self) -> str:
        return "groq"

    def _generate(self,prompts: List[str],**kwargs: Any) -> LLMResult:

        generations = []

        for prompt in prompts:
            try:
                text = generate_response(
                    prompt=prompt,
                    temperature=self.temperature
                )
            except Exception:
                logger.exception(
        "RAG LLM generation failed"
    )          
                raise
            generations.append([Generation(text=text)])

        return LLMResult(generations=generations)

    async def _agenerate(self,prompts: List[str],**kwargs: Any) -> LLMResult:

        return self._generate(prompts, **kwargs)


# 3.  PROMPT TEMPLATE

QA_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""You are a banking call analyst.

Answer ONLY using the context below.
If the answer is not in the context, say "I don't have enough information."

Context:
{context}

Question:
{question}

Answer:"""
)


# 4.  CHAIN BUILDER

def _build_chain(call_id: int):
  

    retriever = ChromaRetriever(call_id=call_id)
    llm = GroqLLM(temperature=0.0)

    def format_docs(docs: List[Document]) -> str:
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | QA_PROMPT
        | llm
        | StrOutputParser()
    )

    return chain


def answer_question(call_id: int,question: str) -> str:
    """
    Answer a question about a specific call using
    the LangChain RAG chain.

    Args:
        call_id (int)
        question (str)

    Returns:
        str: LLM-generated answer.
    """
    logger.info(
    f"QA request received. call_id={call_id}"
)
    chain = _build_chain(call_id=call_id)

    try:
        answer: str = chain.invoke(question)
        logger.info(
            f"QA completed. call_id={call_id}"
        )
        return answer
    except Exception:
        logger.exception(
            f"QA failed. call_id={call_id}"
        )
        raise