#!/usr/bin/env python

from flask import Flask, jsonify, render_template, request, Response
import json
import os
import socket
import datetime

__author__ = 'slowe'

app = Flask(__name__)

if 'SVCURL' in os.environ:
  svc_url = os.environ.get('SVCURL')
else:
  svc_url = 'api'

HOSTNAME = socket.gethostname()
LOCALADDR = socket.gethostbyname(socket.gethostname())

@app.route('/<svc_url>', methods=['GET'])
def show_info(svc_url):
    host = {'hostname': HOSTNAME, 'ip': LOCALADDR}
    time = datetime.datetime.now().strftime("%Y-%b-%d %H:%M:%S")
    client = request.remote_addr
    baseurl = request.base_url
    urlroot = request.url_root
    return render_template('index.html', title='Home', host=host, client=client, baseurl=baseurl, urlroot=urlroot, time=time)

@app.route('/<svc_url>/json', methods=['GET'])
def show_info_json(svc_url):
    return jsonify(hostname=HOSTNAME,
                   ip=LOCALADDR,
                   time=datetime.datetime.now().strftime("%Y-%b-%d %H:%M:%S"),
                   client=request.remote_addr,
                   baseurl=request.base_url,
                   urlroot=request.url_root)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, threaded=True, port=5000)
