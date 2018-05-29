from os import path
from flask import Flask
from flask import render_template
from flask import request, Response
import json
from backend.main import makeCmd
from system import settings
from backend import vm, main, img


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('main.html', netid=settings.NETWORK_ID)
    else:
        print(request.form)
        req = request.form
        name = req.get('name')
        if path.exists(settings.IMG_PATH.format(name=name)):
            return Response(json.dumps({'success': False, 'reason': '标识符已经存在！'}), mimetype='application/json')
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
            'cpu': cpu,
            'disk': disk,
            'mem': mem,
            'hostname': hostname,
            'sshkey': sshkey,
            'passwd': passwd,
            'os': os,
            'expire': expire
        }
        cmd = makeCmd(ip=ip, name=name, dns=dns, disk=disk, mem=mem, hostname=hostname, sshkey=sshkey,
                      passwd=passwd, ostype=os, expire=expire, cpu=cpu)
        print(cmd)
        return Response(json.dumps({'success': True, 'data': data, 'cmd': cmd}), mimetype='application/json')


if __name__ == '__main__':
    app.debug = True    
    app.run()
