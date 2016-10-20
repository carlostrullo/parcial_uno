from flask import Flask, abort, request 
from subprocess import Popen, PIPE
import os
import json


app = Flask(__name__)
api_url = '/v1.0'

@app.route(api_url+'/files',methods=['POST'])
def create_files():
  content = request.get_json(silent=True)
  filename = content['filename']
  content =  content['content']
  grep_process2 = open(filename+'.txt','a')
  grep_process2.write(content+'\n')
  grep_process2.close()
  return "el archivo ha sido creado",201

@app.route(api_url+'/files',methods=['GET'])
def get_list_files():
 path= '/home/filesystem_user/'
 list = []
 lstDir =os.walk(path)
 for root,dirs,files in lstDir:
     for fichero in files:
        (nombreFichero,extension)=os.path.splitext(fichero)
        if(extension==".txt"):
           list.append(nombreFichero+extension)
 return json.dumps(list)



@app.route(api_url+'/files',methods=['DELETE'])
def delete_files():
 process1 = os.system('cd /home/filesystem_user')
 process2 = os.system('find . -name "*.txt" -type f -delete')
 return "los archivos txt han sido eliminados",200 


@app.route(api_url+'/files',methods=['PUT'])
def request_put():
  return "HTTP 404 not found",404


@app.route(api_url+'/files/recently_created',methods=['GET'])
def request_get():
 process1 = Popen(["grep","/bin/bash","/home/filesystem_user","find / -type f -mtime -0"], stdout=PIPE, stderr=PIPE)
 process3 = Popen(["awk",'-F',':','{print $1}'], stdin=process1.stdout, stdout=PIPE, stderr=PIPE).communicate()[0].split('\n')
 list = {}
 list["files"] = filter(None,process3)
 return json.dumps(list), 200



@app.route(api_url+'/files/recently_created',methods=['POST'])
def request_post():
  return "HTTP 404 not found",404

@app.route(api_url+'/files/recently_created',methods=['PUT'])
def request_put_one():
  return "HTTP 404 not found",404

@app.route(api_url+'/files/recently_created',methods=['DELETE'])
def request_delete_one():
  return "HTTP 404 not found",404


if __name__ == "__main__":
  app.run(host='0.0.0.0',port=8088,debug='True')



