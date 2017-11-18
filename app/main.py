#!/usr/bin/env python

from flask import Flask, jsonify, render_template, request, Response
import json
import os
import socket
import datetime
import requests

__author__ = 'slowe'

app = Flask(__name__)

host_name = socket.gethostname()
ip_address = socket.gethostbyname(socket.gethostname())

# Define method to fetch information from remote web service
def get_svc_info(host,port,service):
    url = "http://" + host + ":" + str(port) + "/" + service + "/json/"
    payload = ""
    headers = {
        'content-type': "application/json",
        'accept': "application/json",
        'cache-control': "no-cache",
    }

    # Make the request, then parse/process the response
    raw_response = requests.request("GET", url, data = payload, 
        headers = headers)
    json_response = json.loads(raw_response.text)

    return json_response

# Define back-end route for web services
@app.route('/<svc_url>/json/', methods=['GET'])
def show_info_json(svc_url):
    # Gather information about the request and return as JSON
    if request.headers.getlist('X-Forwarded-For'):
        proxy_addr = request.remote_addr
        client_addr = request.headers.getlist('X-Forwarded-For')[0]
    else:
        proxy_addr = 'No proxy (direct)'
        client_addr = request.remote_addr
    return jsonify(
        container_hostname = host_name,
        container_ip = ip_address,
        time = datetime.datetime.now().strftime("%Y-%b-%d %H:%M:%S"),
        proxy = proxy_addr,
        client = client_addr,
        baseurl = request.base_url,
        urlroot = request.url_root)

# Define front-end route that pulls from back-end web services
@app.route('/', methods=['GET'])
def show_info_html():
    # Get information from "users" web service
    user_ws_response = get_svc_info(
        host = str(os.getenv('USER_API_HOST', 'localhost')),
        port = str(os.getenv('USER_API_PORT', '5000')),
        service = 'users')

    # Get information from "orders" web service
    order_ws_response = get_svc_info(
        host = str(os.getenv('ORDER_API_HOST', 'localhost')),
        port = str(os.getenv('ORDER_API_PORT', '5000')),
        service = 'orders')

    # Gather information for front-end service
    if request.headers.getlist('X-Forwarded-For'):
        proxy_addr = request.remote_addr
        client_addr = request.headers.getlist('X-Forwarded-For')[0]
    else:
        proxy_addr = 'No proxy (direct)'
        client_addr = request.remote_addr
    fe_ws_response = { 'container_hostname': host_name,
        'container_ip': ip_address,
        'time': datetime.datetime.now().strftime("%Y-%b-%d %H:%M:%S"),
        'proxy': proxy_addr,
        'client': client_addr,
        'baseurl': request.base_url,
        'urlroot': request.url_root }

    # Render and return template
    return render_template('index.html', title = 'Home', 
        users = user_ws_response, orders = order_ws_response,
        frontend = fe_ws_response)

if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug = False, threaded = True, 
        port=int(os.getenv('PORT', '5000')))
