from flask import Flask, render_template, request, redirect, url_for, jsonify
import openai
from router import Routers
import csv

CSV_PATH = "static/csv/device.csv"

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


def connect_netmiko(command, device_x):
    with open(CSV_PATH, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data = [row for row in csv_reader]
    
    device_y = Routers('null','99.99.99.99','null','null','null','null')
    for d in data:
        if d['hostname'] == device_x:
            new_router = Routers(
                d['hostname'],
                d['ip'],
                d['username'],
                d['password'],
                d['enable_password'],
                d['os']
            )
            device_y = new_router

    result = device_y.connect(command)
    return result


def get_hostname():
    the_hostnames = []
    with open(CSV_PATH, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data = [row for row in csv_reader]

    for d in data:
        the_hostnames.append(d['hostname'])

    return the_hostnames



app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/chatbot')
def chatbot():
    return render_template("chatbot.html")

@app.route('/get_chatbot', methods=['GET','POST'])
def get_chatbot():
    data = request.json['input']
    human(data)
    response = bot()
    return jsonify({'result': response})


@app.route('/show_netmiko')
def show_netmiko():
    hostnames = get_hostname()
    return render_template("show_netmiko.html", hostnames=hostnames)

@app.route('/get_show_netmiko', methods=['GET','POST'])
def get_show_netmiko():
    command = request.json['input']
    device_x = request.json['device']
    result = connect_netmiko(command, device_x)
    return jsonify(result)





if __name__ == '__main__':
    app.run(debug=True,port=5000)


