"""Emotion detection web service."""


import requests


def emotion_detector(text_to_analyse):
    """Analyse a text and return detected emotions."""
    url = (
        "https://sn-watson-emotion.labs.skills.network/"
        "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    )

    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }

    input_json = {"raw_document": {"text": text_to_analyse}}

    result = {
        "anger": None,
        "disgust": None,
        "fear": None,
        "joy": None,
        "sadness": None,
        "dominant_emotion": None,
    }

    try:
        response = requests.post(
            url, headers=headers, json=input_json, timeout=10
        )
    except requests.RequestException:
        return result

    if response.status_code == 400:
        return result

    if response.status_code != 200:
        return result

    formatted_response = response.json()
    emotions = formatted_response["emotionPredictions"][0]["emotion"]
    result["anger"] = emotions["anger"]
    result["disgust"] = emotions["disgust"]
    result["fear"] = emotions["fear"]
    result["joy"] = emotions["joy"]
    result["sadness"] = emotions["sadness"]
    result["dominant_emotion"] = max(emotions, key=emotions.get)

    return result
