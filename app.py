# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from flask_cors import CORS
import os, json
import openai

app = Flask(__name__)
CORS(app)  # allow all origins; for production, restrict this to your domain

# Load OpenAI key from environment
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

# Load rules if exist
RULES_FILE = os.path.join(os.path.dirname(__file__), "rules.json")
def load_rules():
    try:
        with open(RULES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"rules": []}

def find_matching_rule(text: str, rules):
    t = text.lower()
    for rule in rules.get("rules", []):
        for kw in rule.get("match_any", []):
            if kw.strip().lower() in t:
                return rule
    return None

def generate_ai_reply(user_text: str, rule=None):
    if not OPENAI_API_KEY:
        return "⚠️ OpenAI API key not configured."
    system_prompt = "أنت مساعد ذكي يجيب بالعربية وبأسلوب مهني ومفيد ومختصر."
    if rule and rule.get("ai_instructions"):
        system_prompt += " " + rule["ai_instructions"]

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"المستخدم: {user_text}\nأجب باختصار وبوضوح."}
    ]
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=250,
            temperature=0.3,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        # Return friendly error for client and log to server console
        print("OpenAI error:", e)
        return "⚠️ Failed to generate AI reply. See server logs."

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True, silent=True)
    if not data or "text" not in data:
        return jsonify({"ok": False, "error": "Invalid payload; expected JSON with 'text' field."}), 400

    text = data.get("text", "").strip()
    rules = load_rules()
    rule = find_matching_rule(text, rules)

    if rule:
        reply_type = rule.get("reply_type", "static")
        static_reply = rule.get("static_reply", "")
        if reply_type == "static":
            reply = static_reply
        elif reply_type == "ai":
            reply = generate_ai_reply(text, rule)
        elif reply_type == "both":
            reply = (static_reply + "\n\n" + generate_ai_reply(text, rule)) if static_reply else generate_ai_reply(text, rule)
        else:
            reply = "⚙️ Unknown reply_type in rules."
    else:
        reply = generate_ai_reply(text, None)

    return jsonify({"ok": True, "reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
