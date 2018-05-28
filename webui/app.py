from flask import Flask
from flask import render_template
from flask import request, Response
import json


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('main.html')
    else:
        print(request.form)
        req = request.form
        name = req.get('name')
        ip = req.get('ip')
        dns = req.get('dns')
        cpu = req.get('vcpu')
        disk = req.get('disk')
        mem = req.get('mem')
        hostname = req.get('hostname')
        sshkey = req.get('sshkey')
        passwd = req.get('pass')
        os = req.get('type')
        expire = req.get('expire').capitalize()
        data = {
            'name': name,
            'ip': ip,
            'dns': dns,
            'ip': ip,
            'cpu': cpu,
            'disk': disk,
            'mem': mem,
            'hostname': hostname,
            'sshkey': sshkey,
            'passwd': passwd,
            'os': os,
            'expire': expire
        }
        return Response(json.dumps({'success': True, 'data': data}), mimetype='application/json')



if __name__ == '__main__':
    app.debug = True    
    app.run()

