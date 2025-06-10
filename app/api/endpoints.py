from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.chains.humanizer_chain import humanize_text  # Assuming this is your humanizer function
# from app.chains.mistral_hu import humanize_text

router = APIRouter()


class HumanizeInput(BaseModel):
    text: str


@router.post("/humanize")
async def humanize_text_endpoint(input_data: HumanizeInput):
    try:
        # Call your humanizer function with just the text
        humanized = humanize_text(
            input_data.text,
        )
        return {
            "original": input_data.text, 
            "humanized": humanized
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))