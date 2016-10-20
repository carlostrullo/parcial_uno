# Carlos Arturo Arredondo Trullo. Cod 12107001

##Solución parcial uno.
### A continuación se describiran los pasos utilizados para resolver el primer parcial de sistemas operacionales
#### 1. Encienda la máquina vritual centos
#### 2. Ingrese inicialmente como root y luego cree un usuario llamado filesystem_user (con una contraseña de su preferencia)

```sh
$ useradd filesystem_user
$ passwd filesystem_user
```
#### 3. Ingrese al sistema con el usuario filesystem_user
![GitHub Logo](https://github.com/carlostrullo/parcial_uno/blob/master/usuario_parcial.png)


#### 4. como usuario root: descargue e instale python y virtualenv (necesarios para crear el ambiente virtual en el servidor)
```sh
# cd /tmp
# wget https://bootstrap.pypa.io/get-pip.py
# python get-pip.py
# pip install virtualenv
```

#### 5. regresando al usuario filesystem_user, ingrese a home/filesystem_user y cree el directorio flask_env, luego instale el ambiente en dicho directorio.
```sh
$ cd /home/filesystem/
$ mkdir flask_env
$ virtualenv flask_env
$ pip install virtualenv
```
#### 6. Una vez finalizada la instalación del ambiente, el siguiente paso es activarlo para instalar flask.
```sh
$ . flask_env/bin/activate
$  pip install Flask
```

#### 7. Desactive el ambiente por un momento para habilitar el puerto 8088, con el fin de tener servicio web

```sh
$ deactivate
```
####   -como usuario root ingrese al siguiente directorio y modifique el archivo iptables

```sh
# cd /etc/sysconfig
# ls
# vi iptables
```
#### - Debajo de la línea que contiene el puerto 8080 agregue una igual, pero cambie el puerto por 8088 (el puerto es de libre elección).
![GitHub Logo](https://github.com/carlostrullo/parcial_uno/blob/master/iptables.png)


#### - Una vez guardado el archivo iptables, reinicie los servicios
```sh
# service iptables restart
```

#### 8. Regrese al usuario filesystem_user, active el ambiente (item 1 paso 6) y con el editor "vi" cree el archivo parcial.py e ingrese el siguiente código
```py
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

```

#### - Una vez guardado el código, proceda a ejecutarlo para activar el servicio web
```sh
$ python parcial.py
```
![GitHub Logo](https://github.com/carlostrullo/parcial_uno/blob/master/activado.png)

#### 9. Una vez activado el servicio web, instale y ejecute el complemento de google Chrome postman. En ella pruebe cada una de las peticiones, "GET", "POST","DELETE", etc.
![GitHub Logo](https://github.com/carlostrullo/parcial_uno/blob/master/Sin%20t%C3%ADtulo.png)
![GitHub Logo](https://github.com/carlostrullo/parcial_uno/blob/master/image.png)
![GitHub Logo](https://github.com/carlostrullo/parcial_uno/blob/master/image2.png)
![GitHub Logo](https://github.com/carlostrullo/parcial_uno/blob/master/image3.png)
