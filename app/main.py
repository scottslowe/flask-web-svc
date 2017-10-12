#!/usr/bin/env python

from flask import Flask, jsonify, render_template, request, Response
import json
import os
import socket
import datetime

__author__ = 'slowe'

app = Flask(__name__)

host_name = socket.gethostname()
ip_address = socket.gethostbyname(socket.gethostname())

@app.route('/<svc_url>', methods=['GET'])
def show_info_html(svc_url):
    if request.headers.getlist('X-Forwarded-For'):
        proxy_addr = request.remote_addr
        client_addr = request.headers.getlist('X-Forwarded-For')[0]
    else:
        proxy_addr = 'No proxy (direct)'
        client_addr = request.remote_addr
    host = {'hostname': host_name, 'ip': ip_address}
    time = datetime.datetime.now().strftime("%Y-%b-%d %H:%M:%S")
    client = client_addr
    proxy = proxy_addr
    baseurl = request.base_url
    urlroot = request.url_root
    return render_template('index.html', title = 'Home', host = host, client = client, proxy = proxy, baseurl = baseurl, urlroot = urlroot, time = time)

@app.route('/<svc_url>/json', methods=['GET'])
def show_info_json(svc_url):
    if request.headers.getlist('X-Forwarded-For'):
        proxy_addr = request.remote_addr
        client_addr = request.headers.getlist('X-Forwarded-For')[0]
    else:
        proxy_addr = 'No proxy (direct)'
        client_addr = request.remote_addr
    return jsonify(container_hostname = host_name,
                   container_ip = ip_address,
                   time = datetime.datetime.now().strftime("%Y-%b-%d %H:%M:%S"),
                   proxy = proxy_addr,
                   client = client_addr,
                   baseurl = request.base_url,
                   urlroot = request.url_root)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, threaded=True, port=int(os.getenv('PORT', '5000')))
