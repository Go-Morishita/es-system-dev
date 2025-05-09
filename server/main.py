from fastapi import FastAPI, HTTPException, Response
from openai import OpenAI
from dotenv import load_dotenv
import xml.etree.ElementTree as ET
import os

from create_pdf import create_pdf
from models import GPTRequest, CONFIG_JSON

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()


@app.post("/get_json")
async def get_json_endpoint(req: GPTRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": req.instruction},
                {"role": "user", "content": req.user_input}
            ],
            max_tokens=1000
        )

        raw_text = response.choices[0].message.content
        root = ET.fromstring(raw_text)

        result_json = CONFIG_JSON(
            name=root.find("name").text.strip(),
            question1=root.find("question1").text.strip(),
            answer1=root.find("answer1").text.strip(),
            question2=root.find("question2").text.strip(),
            answer2=root.find("answer2").text.strip()
        )

        return result_json.model_dump()

    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Error processing the request in get_json: " + str(e))


@app.post("/create_pdf")
async def create_pdf_endpoint(json: CONFIG_JSON):
    try:
        pdf_bytes = create_pdf(json)
        return Response(content=pdf_bytes, media_type="application/pdf")

    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Error processing the request in create_pdf: " + str(e))
