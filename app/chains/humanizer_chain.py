import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file.")


llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0.25,
        top_p=0.9,
        frequency_penalty=0.5,
        presence_penalty=0.3,
        api_key=openai_api_key
    )



default_prompt = """
Role: 
You are an experienced writing assistant skilled in humanizing and enhancing academic texts, 
ensuring they sound clear, natural, engaging, and authentically human-written.

Task:
Transform the following academic text by rewriting it into clear, conversational language that retains accuracy, 
readability, and professionalism. 

Specifically:
Improve flow by restructuring sentences or paragraphs if needed.
Eliminate awkward phrasing and overly formal expressions.
Replace overly technical jargon with simpler explanations where appropriate.
Maintain the original meaning and key academic points.
Ensure the tone is friendly, engaging, and genuinely human.
Original Text:
{input_text}

Humanized Version:
"""


def humanize_text(text: str) -> str:
    # template = PROMPT_TEMPLATES.get(audience, PROMPT_TEMPLATES["default"])
    
    prompt = ChatPromptTemplate.from_template(template=default_prompt)

    humanizer_chain = prompt | llm
    response = humanizer_chain.invoke({"input_text": text})

    return response.content

# text = ""
# humanized_text =  humanize_text(text)
# print(humanized_text)