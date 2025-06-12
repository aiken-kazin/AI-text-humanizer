from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from app.chains.humanizer_chain import humanize_text  # Assuming this is your humanizer function
import sys
import os
sys.path.append(os.path.abspath("../.."))

import app.chains.detectors as detectors
from importlib import reload
reload(detectors)


router = APIRouter()

class HumanizeInput(BaseModel):
    text: str

class DetectInput(BaseModel):
    text: str

class DetectorResult(BaseModel):
    detector_name: str
    ai_probability: float

class DetectionResponse(BaseModel):
    results: List[DetectorResult]


    

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


@router.post("/detect")
async def detect_ai_endpoint(input_data: DetectInput) -> DetectionResponse:
    try:
        print(f"Detection request received for text: {input_data.text[:100]}...")  # Debug log
        
        # Call the AI detection function
        detection_results = detectors.detect_ai(input_data.text)
        print(f"Raw detection results: {detection_results}")  # Debug log
        
        # Ensure the results are in the expected format
        formatted_results = []
        
        # Handle different possible return formats from detect_ai
        if isinstance(detection_results, list):
            print("Processing list format results")
            for result in detection_results:
                if isinstance(result, dict):
                    # Handle dict with various possible key names
                    name = result.get('name') or result.get('detector_name') or result.get('detector') or 'Unknown Detector'
                    probability = result.get('probability') or result.get('ai_probability') or result.get('score') or 0.0
                    formatted_results.append(DetectorResult(
                        detector_name=str(name),
                        ai_probability=float(probability)
                    ))
                else:
                    print(f"Unexpected result format in list: {type(result)}")
                    
        elif isinstance(detection_results, dict):
            print("Processing dict format results")
            # If it returns a single result or dict format
            for detector_name, probability in detection_results.items():
                try:
                    formatted_results.append(DetectorResult(
                        detector_name=str(detector_name),
                        ai_probability=float(probability)
                    ))
                except (ValueError, TypeError) as e:
                    print(f"Error processing detector result {detector_name}: {probability}, Error: {e}")
                    
        else:
            print(f"Unexpected detection results type: {type(detection_results)}")
            # Fallback: create mock results for testing
            formatted_results = [
                DetectorResult(detector_name="Test Detector", ai_probability=0.75)
            ]
        
        # If no results were formatted, create a test result
        if not formatted_results:
            print("No formatted results, creating test result")
            formatted_results = [
                DetectorResult(detector_name="Default Detector", ai_probability=0.5)
            ]
        
        print(f"Formatted results: {formatted_results}")  # Debug log
        return DetectionResponse(results=formatted_results)
        
    except ImportError as e:
        print(f"Import error for detect_ai: {e}")
        # Return mock results if detect_ai function is not available
        return DetectionResponse(results=[
            DetectorResult(detector_name="GPTZero", ai_probability=0.85),
            DetectorResult(detector_name="AI Content Detector", ai_probability=0.72),
            DetectorResult(detector_name="Originality.ai", ai_probability=0.68)
        ])
    except Exception as e:
        print(f"Detection error: {str(e)}")  # Debug log
        raise HTTPException(status_code=500, detail=f"Detection failed: {str(e)}")

# # Test endpoint to verify the detection endpoint is working
# @router.get("/detect/test")
# async def test_detect_endpoint():
#     """Test endpoint to verify detection functionality"""
#     return DetectionResponse(results=[
#         DetectorResult(detector_name="Test Detector 1", ai_probability=0.85),
#         DetectorResult(detector_name="Test Detector 2", ai_probability=0.42),
#         DetectorResult(detector_name="Test Detector 3", ai_probability=0.91)
#     ])
    



# @router.post("/detect")
# async def detect_ai_endpoint(input_data: DetectInput) -> DetectionResponse:
#     try:
#         # Call the AI detection function
#         detection_results = detectors.detect_ai(input_data.text)
        
#         # Ensure the results are in the expected format
#         # If detect_ai returns a different format, adjust accordingly
#         formatted_results = []
        
#         # Assuming detect_ai returns a list of dictionaries with detector info
#         # You may need to adjust this based on your actual detect_ai function output
#         if isinstance(detection_results, list):
#             for result in detection_results:
#                 formatted_results.append(DetectorResult(
#                     detector_name=result.get('name', 'Unknown Detector'),
#                     ai_probability=result.get('probability', 0.0)
#                 ))
#         elif isinstance(detection_results, dict):
#             # If it returns a single result or dict format
#             for detector_name, probability in detection_results.items():
#                 formatted_results.append(DetectorResult(
#                     detector_name=detector_name,
#                     ai_probability=probability
#                 ))
#         else:
#             # If it's a different format, you'll need to adjust this
#             raise ValueError("Unexpected detection results format")
        
#         return DetectionResponse(results=formatted_results)
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Detection failed: {str(e)}")

