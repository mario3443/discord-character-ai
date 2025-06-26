from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "").strip()

    print(f"收到訊息：{user_message}")

    # 簡單的回應邏輯
    # 之後再加入更複雜的 AI 模型或邏輯
    response = {
        "reply": f"Yo～你說『{user_message}』？這種程度的話題對我來說簡直小菜一碟😎 不過我喜歡，繼續講，我有在聽～"
    }

    return jsonify(response)

if __name__ == "__main__":
    app.run(port=5005, debug=True)
