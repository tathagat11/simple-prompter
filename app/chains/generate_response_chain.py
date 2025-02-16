"""Chain to get response from LLM."""

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_google_vertexai import ChatVertexAI

model = ChatVertexAI(model_name="gemini-1.5-flash-002", temperature=0)

prompt = PromptTemplate(
    template="{promptTemplate}",
    input_variables=["promptTemplate"],
)

chain = prompt | model | StrOutputParser()