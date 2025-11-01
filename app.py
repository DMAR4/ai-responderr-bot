from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

# تهيئة التطبيق
app = Flask(__name__)
CORS(app)

# تهيئة OpenAI Client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return jsonify(message="🤖 AI Responder is running successfully!")

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    user_text = data.get("text", "")

    if not user_text:
        return jsonify(ok=False, error="No text provided")

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",  # يمكنك تغييره إلى "gpt-3.5-turbo" لو ما عندك وصول لـ GPT-4
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي وودود. أجب المستخدم باللغة العربية دائماً."},
                {"role": "user", "content": user_text}
            ]
        )
        reply = completion.choices[0].message.content.strip()
        return jsonify(ok=True, reply=reply)

    except Exception as e:
        print("OpenAI error:", e)
        return jsonify(ok=False, error=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

