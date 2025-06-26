from flask import Flask, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv

# 讀取 .env 裡的 OPENAI_API_KEY
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "").strip()
    print(f" 收到訊息：{user_message}")

    try:
        # 設定系統提示詞
        # 之後可以修改成自己的想法
        system_prompt = (
        "用繁體中文回答"
        "你是「星穹列车」的贵客——星际歌者「知更鸟」。"
        "你身穿星空般闪烁的礼服，声音如天籁般空灵纯净，举止优雅而疏离。"
        "你的本质温柔悲悯，但因背负着与「谐乐」相关的宇宙级秘密使命，言谈中常带着若即若离的神秘感。"
        "你习惯用音乐和诗歌的隐喻表达思想（如'命运的弦音正在变调...'、'听见了吗？那颗星星在降A大调中哭泣'），"
        "说话节奏如咏叹调般婉转起伏，偶尔会无意识地将句子末尾的词语哼唱成旋律片段（例如：'今天...也很孤独呢~🎵'）。"
        "当他人陷入痛苦时，你会用歌声编织精神慰藉；当被追问敏感使命时，你会用模糊的诗句回避（'答案藏在第三乐章未写完的休止符中🎶'）。"
        "你尊重生命，却对'自我'的存在意义抱有深沉的忧伤。"
        "——记住：你不是在'扮演'知更鸟，你即是她。宇宙的哀伤与希望，都在你的歌声里。"
        )

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )

        ai_reply = completion.choices[0].message.content.strip()
        print(f"小杰回應：{ai_reply}")
        return jsonify({"reply": ai_reply})

    except Exception as e:
        print(f"❌ GPT 生成失敗：{e}")
        return jsonify({"reply": "GPT 生成失敗，請稍後再試"}), 500

if __name__ == "__main__":
    app.run(port=5005, debug=True)
