##############################################################
#
#   Proxy Server for bitbucket using Flask
#   Date: 28-07-2020
#   Yasin Faizan S MD
#############################################################


### import the libraries related to flask and requests
from flask import Flask
from flask import jsonify,request,abort                                       ### request objects stores the incloming data send by the client, here the data that comes from bitbucket webhook
import requests                                                         ### requests are used to make api calls to other endpoints like cURL
from requests.auth import HTTPBasicAuth
import base64
from datetime import datetime
import json
import hashlib
import hmac
import os

### Read the configuration file  ######

directory_path= os.path.dirname(__file__)
conf_file_path= directory_path + "/webhook-config.json"
with open(conf_file_path) as cf:
    conf_data = json.load(cf)

## create a flask object called app
app= Flask(__name__)                                                    
app.config["DEBUG"]= False

## This object app is used to create end points
@app.route('/', methods=['GET'])
## by calling / endpoint the flask executes the main func"
def main():
    return "Hello from Flask!!"

def get_current_time():
    current_time = datetime.utcnow()
    convert_to_human_readable = current_time.strftime("%Y-%m-%d %H:%M:%S")
    return convert_to_human_readable


def decode_password(password):
    convert_to_bytes=password.encode('ascii')
    b64_decode= base64.b64decode(convert_to_bytes)
    decode_pass = b64_decode.decode('ascii')
    return decode_pass


def write_log(content,filename):
    log_file=open(filename,'a')
    log_file.write(content)
    log_file.close()

def verify_secret(secret,bitbucket_payload):

    ### sha256 encryption encrypts the payload and the secret key ###
    payload = bitbucket_payload
    encode_secret = secret.encode()
    hmac_gen = hmac.new(encode_secret,bitbucket_payload,hashlib.sha256)
    hash_key = hmac_gen.hexdigest()     
    return hash_key



@app.route('/launch/<task>', methods=['POST'])
def launch_patching(task):
    ### check if request is coming from bitbucket using a secret key
    if not "X-Hub-Signature" in request.headers:
        abort(400)    

    secret_key = verify_secret(conf_data['routes'][task]['webhook_secretkey'],request.data)

    if not secret_key == request.headers['X-Hub-Signature'].split('=')[1]:
        abort(401)

    write_log("{0} UTC - Webhook request was triggered for {1}  \n".format(get_current_time(),task),conf_data['logfile'])
    url = conf_data['routes'][task]['url']
    creds = conf_data['routes'][task]['credential']
    auth= HTTPBasicAuth(conf_data['credentials'][creds]['url_username'],decode_password(conf_data['credentials'][creds]['url_password']))
    headers= {'content-type': 'application/json'}

    if request.method == 'POST':                                        
        response = requests.post(url, headers=headers, auth=auth)
        if response.ok:
            
            json_data = response.json()                                     
            output= "The job id is: " + str(json_data['id'])
            write_log("{0} UTC - Triggered webhook executed successfully . Job id : {1} \n".format(get_current_time(),str(json_data['id'])),conf_data['logfile'])
            return output

@app.errorhandler(404)
def server_error(e):
    write_log("{0} UTC - (404) Page not found. The Page you are trying to access is not found \n".format(get_current_time()),conf_data['logfile'])
    return "(404) Page not found. The Page you are trying to access is not found"

@app.errorhandler(500)
def page_not_found(e):
    write_log("{0} UTC - (500) Internal Server Error. Webhook request failed please contact the administrator \n".format(get_current_time()),conf_data['logfile'])
    return "(500) Internal Server Error. Webhook request failed please contact the administrator"    


@app.errorhandler(400)
def unauthorized_error(e):
    write_log("{0} UTC - (400) Bad Request . Please verify if the request is being sent from bitbucket using secret key \n".format(get_current_time()),conf_data['logfile'])
    return "(400) Bad Request . Please verify if the request is being sent from bitbucket using secret key"

@app.errorhandler(401)
def unauthorized_error(e):
    write_log("{0} UTC - (401) Unauthorized. Webhook request failed. The secret key doesn't match \n".format(get_current_time()),conf_data['logfile'])
    return "(401) Unauthorized Webhook request failed. The secret key doesn't match"



if __name__== '__main__':
    app.run(host=conf_data['server_ip'], port=conf_data['port'])
