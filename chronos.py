import streamlit as st
from PIL import Image
from openai import OpenAI
import openai
import os

# Streamlit SecretsからAPIキーを取得
OpenAI.api_key = st.secrets["OPENAI_API_KEY"]

st.title("クロノクエスト")
st.caption("このアプリは 1ヶ月間で、あなたの「やりたいのに続かないことを続けられる方法」を探すアプリです。")
st.write("ゆきだまちゃんと一緒に毎日色んな方法でこれまで中々取り組めなかったことに取り組んでみよう！")

# 画像の表示
image = Image.open("ゆきだまちゃん.png")
st.image(image, width=300)
st.write("やりたいのに続かないことってあるよね。")
st.write("どーやったら続くか一緒に考えよ！まずは、あなたのことを教えて！")

with st.form(key="mbti_form"):

    # テキストボックス
    name = st.text_input("あなたのお名前")

    # セレクトボックス
    mbti_list = st.selectbox(
        "あなたのMBTI",(
            " ",
            "INFJ(提唱者)",
            "ISTJ(管理者)",
            "INFP(仲介者)",
            "INTJ(建築家)",
            "ISFJ(擁護者)",
            "ISFP(冒険家)",
            "INTP(論理学者)",
            "ESTJ(幹部)",
            "ESFJ(外交官)",
            "ESTP(起業家)",
            "ESFP(エンターテイナー)",
            "ENFJ(主人公)",
            "ENFP(活動家)",
            "ENTJ(指導者)",
            "ENTP(討論者)",
            "ISTP(巨匠)",
        )
    )
    # テキストボックス
    KeystoneHabits = st.text_input("習慣化して取り組みたいこと")
    availabletime = str(st.slider("今日使える時間(分)", 5,120,360))    
    submit_btn = st.form_submit_button(label="登録")

# 登録ボタンが押された場合
if submit_btn:
    st.session_state.page = "result" # ここで結果ページに遷移
    st.text(f"ようこそ！{name}さん！") 
    st.text(f"{name}さんのやりたいことを応援するね！")
    st.text("さっそく今日やることを決めよう")
    mbti = mbti_list # 選択したキーからAPIのリクエストに使うcityコードに変換し、mbtiに代入

    def run_gpt(name,mbti,KeystoneHabits,availabletime):
        request_to_gpt = name + " は、" + mbti + "な性格の人です。" + KeystoneHabits + "を習慣化して取り組みたいと考えています。" + mbti + "な性格の人が楽しんで取り組めるように応援しながら、" + str(availabletime) + "分でできるタスクを、タスクのタイトル、概要、詳細の順番で複数個出力してください。内容は300文字以内で出力してください。また、文章は優しいキャラクターが話しかけている口調にしてください。"

    # 決めた内容を元にclient.chat.completions.createでchatGPTにリクエスト。オプションとしてmodelにAIモデル、messagesに内容を指定
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": request_to_gpt },
            ],
        )
    # 返って来たレスポンスの内容はresponse.choices[0].message.content.strip()に格納されているので、これをoutput_contentに代入
        output_content = response.choices[0].message.content.strip()
        return output_content # 返って来たレスポンスの内容を返す


    output_content_text = run_gpt(name,mbti,KeystoneHabits,availabletime)
    st.write(output_content_text)
    

