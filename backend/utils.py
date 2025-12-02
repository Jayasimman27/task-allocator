import json
import re

def extract_json(text: str):
    try:
        return json.loads(text)
    except:
        pass

    # Try to find JSON inside text
    json_match = re.search(r"\{.*\}", text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except:
            pass

    # If still not valid
    raise ValueError("Could not parse valid JSON:\n" + text)
