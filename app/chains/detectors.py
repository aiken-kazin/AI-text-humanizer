import requests


def detect_ai(text):
    response = requests.post(
        "https://api.sapling.ai/api/v1/aidetect",
        json={
            "key": "RHMMYVZX39KKSOJP5VZTCRUQLCB7LFFX",
            "text": text
        }
    )

    # return str(round(float(response.json()['score']),3) * 100) + "% AI generated"
    return [
        {
            "name": "GPTZero",
            "probability": 0.3  # 85% AI probability
        },
        {
            "name": "Another Detector",
            "probability": 0.2  # 85% AI probability
        },
        {
            "name": "Another Detector ",
            "probability": 0.9  # 85% AI probability
        }
    ]









