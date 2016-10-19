from flask import Flask, abort, request 
from subprocess import Popen, PIPE
import json


app = Flask(__name__)
api_url = '/v1.0'

@app.route(api_url+'/files',methods=['GET'])
def get_list_files():
 grep_process = Popen(["grep","cd /home","ls"], stdout=PIPE, stderr=PIPE)
 files_list = Popen(["awk",'{print $1}'], stdin=grep_process.stdout, stdout=PIPE, stderr=PIPE).communicate()[0].split('\n')
 list = {}
 list["files"] =files_list
 return json.dumps(list), 200


@app.route(api_url+'/files',methods=['PUT'])
def create_files():
  content = request.get_json(silent=True)
  filename = content['filename']
  content =  content['content']
  grep_process = Popen(["grep","cd /home","vi "+filename+".txt",":wq"], stdout=PIPE, stderr=PIPE)
  return "el archivo ha sido creado",200 

if __name__ == "__main__":
  app.run(host='0.0.0.0',port=8088,debug='True')




