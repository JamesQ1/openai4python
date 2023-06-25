import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        animal = request.form["animal"]
        # return redirect(url_for("index", result=chat(animal)))
        try:
            response = chat(animal)
            return render_template("index.html", result=response)
        except Exception as e:
            print('错误信息：'+str(e))
            return render_template("index.html", result='调用超出限制，请过20秒再尝试')

    result = request.args.get("result")
    return render_template("index.html", result=result)

#调用openai 问答示例
def chat(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content":prompt}
        ]
    )
    answer = response.choices[0].message.content
    return answer

def generate_prompt(animal):
    return """Suggest three names for an animal that is a superhero.

Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(
        animal.capitalize()
    )

if __name__ == '__main__':
    app.run()

