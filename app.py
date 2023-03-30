from flask import Flask, render_template, request, redirect, url_for, jsonify
import openai

openai.api_key = ""
messages = [{"role": "user", "content": "Hello there!"},]

def bot():
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=messages)
    content = response['choices'][0]['message']['content']
    update_messages("assistant",content)
    return content

def human(content):
    update_messages("user",content)

def update_messages(role, content):
    messages.append({"role":role, "content":content})


       

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/ajax', methods=['GET','POST'])
def ajax_request():
    data = request.json['input']
    human(data)
    response = bot()
    return jsonify({'result': response})


if __name__ == '__main__':
    app.run(debug=True,port=5000)


