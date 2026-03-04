from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage

# ==============================
# LLMに問い合わせる関数
# ==============================
def get_llm_response(input_text: str, expert_type: str) -> str:
    """
    入力テキストと専門家タイプを受け取り、
    LLMからの回答を文字列で返す
    """

    # 専門家タイプに応じてシステムメッセージを変更
    if expert_type == "ITエンジニア":
        system_message = "あなたは優秀なITエンジニアです。専門的かつ分かりやすく技術的観点から回答してください。"
    elif expert_type == "マーケティングコンサルタント":
        system_message = "あなたは経験豊富なマーケティングコンサルタントです。市場視点・顧客視点で戦略的に回答してください。"
    else:
        system_message = "あなたは専門家です。"

    # LLMモデルの設定
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7
    )

    # プロンプトテンプレート
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("human", "{input}")
    ])

    # チェーン実行
    chain = prompt | llm
    response = chain.invoke({"input": input_text})

    return response.content


# ==============================
# Streamlit アプリ部分
# ==============================

st.set_page_config(page_title="専門家AIアプリ", layout="centered")

st.title("🎓 専門家AIアシスタント")

st.markdown("""
### 📌 アプリ概要
このアプリでは、入力したテキストをLLMに送信し、
選択した専門家として回答を生成します。

### 🛠 操作方法
1. ラジオボタンで専門家の種類を選択
2. 入力フォームに質問を入力
3. 「送信」ボタンを押す
4. 回答が画面下に表示されます
""")

# 専門家選択ラジオボタン
expert_choice = st.radio(
    "専門家の種類を選択してください",
    ("ITエンジニア", "マーケティングコンサルタント")
)

# 入力フォーム
user_input = st.text_area("質問を入力してください")

# 送信ボタン
if st.button("送信"):
    if user_input.strip() == "":
        st.warning("質問を入力してください。")
    else:
        with st.spinner("回答生成中..."):
            answer = get_llm_response(user_input, expert_choice)

        st.success("回答")
        st.write(answer)