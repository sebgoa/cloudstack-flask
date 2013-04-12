#!/usr/bin/env python
# encoding: utf-8
#Licensed to the Apache Software Foundation (ASF) under one
#or more contributor license agreements.  See the NOTICE file
#distributed with this work for additional information
#regarding copyright ownership.  The ASF licenses this file
#to you under the Apache License, Version 2.0 (the
#"License"); you may not use this file except in compliance
#with the License.  You may obtain a copy of the License at
#http://www.apache.org/licenses/LICENSE-2.0
#Unless required by applicable law or agreed to in writing,
#software distributed under the License is distributed on an
#"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#KIND, either express or implied.  See the License for the
#specific language governing permissions and limitations
#under the License.

import sys
import os
import json
import requester

from flask import Flask, url_for, render_template, request, json
app = Flask(__name__)


apikey='plgWJfZK4gyS3mOMTVmjUVg-X-jlWlnfaUJ9GAbBbf9EdM-kAYMmAiLqzzq1ElZLYq_u38zCm0bewzGUdP66mg'
secretkey='VDaACYb0LV9eNjTetIOElcVQkvJck_J_QljX_FcHRj87ZKiy0z0ty0ZsYBkoXkY9b7eq1EhwJaw7FF3akA3KBQ'
path='/client/api'
host='localhost'
port='8080'
protocol='http'

listpages=['users']

@app.route('/')
def index():
    return render_template('index.html',pages=listpages)

def listusers():
    response, error = requester.make_request('listUsers',{},None,host,port,apikey,secretkey,protocol,path)
    resp=json.loads(str(response))
    return render_template('res.html',results=resp['listusersresponse'])

@app.route('/user/<uuid>', methods=['GET','DELETE','PATCH'])
def user(uuid):
    if request.method =='GET':
        response, error = requester.make_request('listUsers',{'id':uuid},None,host,port,apikey,secretkey,protocol,path)
        return response
    elif request.method =='PATCH':
        data = request.json
        data['id']=uuid
        response, error = requester.make_request('updateUser',data,None,host,port,apikey,secretkey,protocol,path)
        return response
    else:
        response, error = requester.make_request('deleteUser',{'id':uuid},None,host,port,apikey,secretkey,protocol,path)
        return response

@app.route('/user', methods=['GET','POST'])
def users():
    if request.method =='GET':
        return listusers()
    elif request.method =='POST':
        '''Need to pass a json dictionary in the request to feed to the update !!!'''
        response, error = requester.make_request('createUser',request.json,None,host,port,apikey,secretkey,protocol,path)
        return response
    
@app.route('/vm')
def vms():
    response, error = requester.make_request('listVirtualMachines',{},None,host,port,apikey,secretkey,protocol,path)
    resp=json.loads(str(response))
    return render_template('res.html',results=resp['listvirtualmachinesresponse'])

@app.route('/template')
def templates():
    response, error = requester.make_request('listTemplates',{'templatefilter':'all'},None,host,port,apikey,secretkey,protocol,path)
    resp=json.loads(str(response))
    return render_template('res.html',results=resp['listtemplatesresponse'])

if __name__ == '__main__':
    app.run(debug=True)

