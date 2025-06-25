from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    print(f"📥 收到訊息：{user_message}")

    # 模擬角色語氣的固定回應（之後會改成 GPT 回應）
    response = {
        "reply": f"（角色語氣）你說的『{user_message}』很有意思呢！"
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(port=5005, debug=True)
