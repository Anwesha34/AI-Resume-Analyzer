import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

# API KEY
os.environ["GROQ_API_KEY"] = "YOUR_API_KEY"

# LLM Model
llm = ChatGroq(
    groq_api_key=os.environ["GROQ_API_KEY"],
    model_name="llama-3.3-70b-versatile"
)

# Function used in app.py
def get_ai_suggestions(text):

    prompt = PromptTemplate(
        input_variables=["resume"],
        template="""
Analyze this resume and give professional improvement suggestions.

Resume:
{resume}

Give suggestions in:
1. Skills Missing
2. ATS Optimization
3. Formatting
4. Stronger Wording
5. Job Readiness
"""
    )

    final_prompt = prompt.format(resume=text)

    response = llm.invoke(final_prompt)

    return response.content