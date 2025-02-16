"""Chain to create prompts."""

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_google_vertexai import ChatVertexAI


with open("data/prompting.txt", "r", encoding="utf-8") as f:
    context = f.read()


model = ChatVertexAI(model_name="gemini-1.5-flash-002", temperature=0)


TEMPLATE = """
{context}
------------------------------
------------------------------
------------------------------
Based on the above instructions help me write a good prompt TEMPLATE.
This template should be a python f-string. It can take any number of variables depending on my objective.
Return answer in the following format:
\"""
<The prompt>
\"""
This is my objective:
{objective}
Return only a singular specific prompt for the objective, not the code to generate the prompt.
IMPORTANT: Each input variable should be in the form of legal python variable name.
""".strip()

prompt = PromptTemplate.from_template(template=TEMPLATE)
prompt = prompt.partial(context=context)

chain = prompt | model | StrOutputParser()