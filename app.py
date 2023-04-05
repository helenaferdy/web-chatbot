from flask import Flask, render_template, request, redirect, url_for, jsonify
import openai
from router import Routers
import csv
import requests
import base64
import json

CSV_PATH = "static/csv/device.csv"
NOT_KEY = base64.b64decode(("c2stU2J0cWZ1RXp5blZjaU5RTDRndDNUM0JsYmtGSjJjVWNZcmZ6N2JESm43TjZTZ2NE").encode('utf-8')).decode('utf-8')
openai.api_key = NOT_KEY
messages = [{"role": "user", "content": "Hello there!"},]

# CHAT GPT
def bot():
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=messages)
    content = response['choices'][0]['message']['content']
    update_messages("assistant",content)
    return content

def human(content):
    update_messages("user",content)

def update_messages(role, content):
    messages.append({"role":role, "content":content})



# NETMIKO
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



# CVE

# def get_product_name(input_name):
#     url = "https://sec.cloudapps.cisco.com/security/center/productBoxData.x?prodType=CISCO"
#     response = requests.get(url, verify=False)
#     product = response.json()['Cisco']['products']
#     i = 1
#     for p in product:
#         pp = p['productName']
#         if input_name.lower() in pp.lower():
#             products.append(pp)
#             i += 1

def get_product_name2(input_name):
    products = []
    with open('static/cve/products.txt', 'r') as product:
        i = 1
        for p in product:
            if input_name.lower() in p.lower():
                products.append(p)
                i += 1
    return products

def get_token():
    url = "https://cloudsso.cisco.com/as/token.oauth2"
    client_id = "8smzjznfz8vmrm7qcft458x2"
    client_secret = "uqya83hAxn8R6S9vqZjMYW82"

    params = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }

    response = requests.post(url, data=params)
    token = response.json()['access_token']
    return token


def open_token():
    with open("static/cve/token.txt", "r") as file:
        for f in file:
            token = f
    return token

def get_advisory(token, encoded_product):
    advisories = []
    url = "https://api.cisco.com/security/advisories/v2/product?product="

    success = False
    while not success:
        print(f"token : {token}")
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Bearer {token}",
        }
        response = requests.get(url+encoded_product, headers=headers)

        if response.status_code == 403:
            print("token expired")
            token = get_token()
        else:
            success = True
            with open("static/cve/token.txt", "w") as file:
                file.write(token)
            response = response.json()['advisories']
            for r in response:
                a = r['advisoryTitle']
                b = r['bugIDs']
                c = r['cves']
                advisory = {
                    "advisory" : a,
                    "bugid" : b,
                    "cve" : c
                    }
                advisories.append(advisory)
    return advisories

def get_cve(cve):
    url = "https://services.nvd.nist.gov/rest/json/cve/1.0/"
    response = requests.get(url + cve)
    json_data = json.loads(response.content)

    description = json_data["result"]["CVE_Items"][0]["cve"]["description"]["description_data"][0]["value"]
    date = json_data["result"]["CVE_data_timestamp"]
    ref_data = json_data["result"]["CVE_Items"][0]["cve"]["references"]["reference_data"]
    links = []
    for ref in ref_data:
        link = ref["url"]
        links.append(link)
                            
    end_cve = {
        "desc" : description,
        "date" : date,
        "links": links 
    }

    return end_cve





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




@app.route('/cve/')
def cve():
    products = get_product_name2("contact center")
    return render_template("cve.html", products=products)


@app.route('/cve/product/<product>')
def cve_product(product):
    product = product.rstrip()
    product = product.replace(" ", "%20")
    print(product)
    advisories = get_advisory(open_token(), product)
    return render_template("cve_product.html", product=product, advisories=advisories)

@app.route('/cve/cve/<cve>')
def cve_cve(cve):
    cve_response = get_cve(cve)
    return render_template("cve_cve.html", cve=cve, response=cve_response)


if __name__ == '__main__':
    app.run(debug=True,port=5000)


