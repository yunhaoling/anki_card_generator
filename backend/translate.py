import requests
import json


def translate(source, source_language, target_language):
    r = requests.post(
        "http://127.0.0.1:5000/translate",
        data=json.dumps(
            {
                "q": source,
                "source": source_language,
                "target": target_language,
                "format": "text",
                "api_key": ""
            }
        ),
        headers={
            "Content-Type": "application/json"
        }
    )
    # TODO: error handling
    return r.json()['translatedText']
