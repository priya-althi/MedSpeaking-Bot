from flask import Flask, request, jsonify
from flask import send_file
from gtts import gTTS
import uuid
import os
from flask_cors import CORS
from ml.predict import get_medical_response
from ml.age_rules import age_warning
from deep_translator import GoogleTranslator
import re
import threading
import time


def remove_emojis(text):
    # remove emoji unicode ranges only
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport
        "\U0001F700-\U0001F77F"
        "\U0001F780-\U0001F7FF"
        "\U0001F800-\U0001F8FF"
        "\U0001F900-\U0001F9FF"
        "\U0001FA00-\U0001FAFF"
        "\u2600-\u26FF"
        "\u2700-\u27BF"
        "]+",
        flags=re.UNICODE,
    )
    text = emoji_pattern.sub("", text)
    text = text.replace("\n", ". ")
    return text


def delete_file_later(path, delay=20):
    def task():
        time.sleep(delay)
        if os.path.exists(path):
            os.remove(path)
    threading.Thread(target=task).start()

app = Flask(__name__)
CORS(app)   

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json

        user_msg = data.get("message", "")
        lang = data.get("lang", "en")

        # Safe age parsing
        try:
            age = int(data.get("age", 0))
        except:
            age = 0

        # ---- Translate input to English ----
        if lang != "en":
            user_msg_en = GoogleTranslator(source=lang, target="en").translate(user_msg)
        else:
            user_msg_en = user_msg

        # ---- ML / Rule Prediction ----
        result = get_medical_response(user_msg_en)

        # ===============================
        # CASE 1 → NEED MORE DETAILS
        # ===============================
        if result.get("status") == "clarification":
            msg = result["message"]

            if lang != "en":
                msg = GoogleTranslator(source="en", target=lang).translate(msg)

            return jsonify({
                "status": "clarification",
                "message": msg
            })

        # ===============================
        # CASE 2 → FINAL RESPONSE
        # ===============================
        warning = age_warning(age, result["disease"])

        response_data = {
            "status": "final",
            "disease": result["disease"],
            "advice": result["advice"],
            "medicine": result["medicine"],
            "warning": warning,
        }

        # ---- Translate output if needed ----
        if lang != "en":
            for key in response_data:
                response_data[key] = GoogleTranslator(
                    source="en", target=lang
                ).translate(str(response_data[key]))

        return jsonify(response_data)

    except Exception as e:
        return jsonify({
            "error": "Server error occurred",
            "details": str(e)
        }), 500
@app.route("/speak", methods=["POST"])
def speak():
    try:
        data = request.json
        text = data.get("text", "")
        lang = data.get("lang", "en")

        # language mapping for gTTS
        lang_map = {
            "en": "en",
            "hi": "hi",
            "te": "te",
            "ta": "ta",
            "kn": "kn",
            "ml": "ml",
            "mr": "mr",
            "bn": "bn",
            "gu": "gu",
            "pa": "pa",
            "ur": "ur",
            "or": "or",
            "as": "as"
        }

        tts_lang = lang_map.get(lang, "en")
        os.makedirs("temp_audio", exist_ok=True)

        filename = f"voice_{uuid.uuid4()}.mp3"
        filepath = os.path.join("temp_audio", filename)

        
        clean_text = remove_emojis(text)
        tts = gTTS(text=clean_text, lang=tts_lang)

        tts.save(filepath)
        delete_file_later(filepath, delay=20)
        return send_file(filepath, mimetype="audio/mpeg")

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
