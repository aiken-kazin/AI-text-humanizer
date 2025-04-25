import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file.")

llm = ChatOpenAI(
    temperature=0.5,   # temperatura jogary bolsa bolee AI emes dep tusintin siyakty, birak katty azaimaidy
    model="gpt-4",
    api_key=openai_api_key 
)


# Prompt template

business_prompt = """
You are a professional business writer. 
Your job is to rewrite AI-generated or robotic text to make it sound natural, 
confident, and suitable for professional communication such as emails, reports, or LinkedIn posts.

Keep the original meaning, but improve clarity, flow, and tone. 
Use plain, human language. Avoid awkward phrasing, overly formal expressions, or repetition.

### Example:

Original:
"We are reaching out to inform you that we have evaluated the potential partnership 
opportunities and have found them to be advantageous."

Humanized:
"We wanted to let you know that we’ve reviewed the partnership options and see real potential."

Now rewrite the following:

Original:
{input_text}

Humanized Business Version:

"""
gen_z_prompt = """
You're a Gen Z content creator. Rewrite the text below to sound more casual, relatable, and 
expressive — like something you'd post on TikTok, Instagram, or Twitter. Use slang, emojis, humor, 
or Internet lingo, but don’t overdo it. Keep the meaning, but make it vibe.

### Example:

Original:
"This product offers great features and can help users save time."

Gen Z Version:
"Yo, this thing’s packed with cool stuff — total time-saver. 🔥⏱️"

Now rewrite the following:

Original:
{input_text}

Gen Z Version:
"""

academic_prompt = """
You are an academic writing assistant. Rewrite the text below to sound more formal, 
structured, and suitable for academic papers, essays, or research communication. 
Improve clarity, grammar, and vocabulary, while keeping the original meaning intact.

Avoid contractions or casual language. Use a neutral, precise tone.

### Example:

Original:
"We looked at different ideas and found some useful stuff."

Academic Version:
"The study examined multiple perspectives and identified several valuable insights."

Now rewrite the following:

Original:
{input_text}

Academic Version:
"""

default_prompt = """
You're a writing assistant helping to make text sound more natural and human — like it was written by a real person. 
Rewrite the input to improve flow, fix awkward phrasing, and make it feel smooth, friendly, and easy to read.

Keep the meaning, but make the tone human and conversational.

### Example:

Original:
"Following are the steps that must be followed to ensure success."

Humanized Version:
"Here’s what you need to do to succeed:"

Now rewrite the following:

Original:
{input_text}

Humanized Version:
"""



PROMPT_TEMPLATES = {
    "business": business_prompt,
    "gen_z": gen_z_prompt,
    "academic": academic_prompt,
    "default": default_prompt,
}



def humanize_text(text: str, audience: str = "default") -> str:
    # Pick the correct prompt template
    template = PROMPT_TEMPLATES.get(audience, PROMPT_TEMPLATES["default"])
    
    # Create the prompt with the selected template
    prompt = ChatPromptTemplate.from_template(template=template)

    # Run the LLM chain
    humanizer_chain = prompt | llm
    response = humanizer_chain.invoke({"input_text": text})

    return response.content

# text = ""
# humanized_text =  humanize_text(text)
# print(humanized_text)