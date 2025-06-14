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
        temperature=0.1,
        top_p=0.9,
        frequency_penalty=0.5,
        presence_penalty=0.3,
        api_key=openai_api_key
    )



default_prompt = \
"""
Rewrite the following text in the style of a non-native English speaker with an **IELTS Band 6** writing level. 

The rewritten text should maintain the original meaning clearly, but **include some natural grammatical mistakes, 
occasional vocabulary misuse, and slightly awkward phrasing** typical of an IELTS Band 6 writer. 

Make sure the tone remains human-like and genuine, with a readable flow, and not too polished or “perfect.” 

This style should be applied **regardless of the content type** (academic, casual, technical, marketing, etc.), 
so preserve the original tone and context while infusing the non-native characteristics. 

The goal is to **make the text sound human-written (with minor errors)** to reduce the likelihood of 
AI detection by tools like GPTZero or Originality.ai. 

**Instructions:** Provide **only** the rewritten passage as the output, with no explanations or extra commentary. 

Aim for roughly **400 words** in the rewritten version (adjusting length as needed to stay proportional to the input).

**Text to rewrite:** 

{input_text}
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