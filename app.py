from flask import Flask, render_template, request
from pytube import YouTube
import openai

app = Flask(__name__)
app.secret_key = "your_secret_key_here"


def downloadAudio(url):
    yt = YouTube(url)
    audio = yt.streams.filter(only_audio=True).first()
    audio_path = "audio.mp3"
    audio.download(filename=audio_path)
    return audio_path


def transcribeAudio(audio_path):
    with open(audio_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        text = transcript["text"]
        return text


def textToArticle(text):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"buat artikel dari text {text}! buat dalam format html"},
        ],
    )

    html = completion.choices[0].message["content"]
    return html


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        api_key = request.form["api_key"]
        openai.api_key = api_key

        audio_path = downloadAudio(url)
        text = transcribeAudio(audio_path)
        html = textToArticle(text)
        return render_template("hasil.html", article=html)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
