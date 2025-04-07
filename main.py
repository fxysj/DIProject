import json
import os

from dotenv import load_dotenv
from flask import Flask, Response
from flask_cors import CORS
from openai import OpenAI
load_dotenv()
# print(os.getenv("OPENAI_API_KEY"))
app = Flask(__name__)
CORS(app)
#Initialize OPENAI client globally
openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
)
def generate_response(text: str) -> str | None:
    response = openai_client.chat.completions.create(
        model="yi-medium",
        messages=[{"role": "user", "content": text}],
        stream=False,
    )
    return response.choices[0].message.content
@app.route("/chat", methods=["POST"])
def chat() -> Response:
    text = request.json["text"]  # type: ignore
    response_text = generate_response(text)
    return Response(
        json.dumps({"response": response_text}, ensure_ascii=False),
        content_type="application/json; charset=utf-8",
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, debug=True)