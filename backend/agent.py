from dotenv import load_dotenv
from google import genai
import os, json, re

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("API KEY NOT FOUND! Check .env")

client = genai.Client(api_key=api_key)

def extract_json(text: str):
    try:
        return json.loads(text)
    except:
        pass

    json_match = re.search(r"\{.*\}", text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except:
            pass

    raise ValueError("Could not extract valid JSON:\n" + text)

def fix_json_with_model(bad_text: str):
    fix_prompt_base = open("../model/json_fixed.txt").read()
    fix_prompt = f"{fix_prompt_base}\n{bad_text}"

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=fix_prompt
    )

    try:
        return extract_json(response.text)
    except:
        fallback = response.candidates[0].content.parts[0].text
        return extract_json(fallback)

def process_text(user_text: str):
    prompt = open("../model/prompt.txt").read()
    final_prompt = f"{prompt}\n\nUSER INPUT:\n{user_text}"

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=final_prompt
    )

    try:
        raw_text = response.text.strip() if response.text else response.candidates[0].content.parts[0].text.strip()
    except:
        raw_text = response.candidates[0].content.parts[0].text.strip()

    try:
        return extract_json(raw_text)
    except:
        return fix_json_with_model(raw_text)
