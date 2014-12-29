import json
from pyperf import Iperftcp, Iperfudp, Iperfs
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, Response

app = Flask(__name__)

ID_NO = 0
JOBLIST = {}


@app.route("/jobs", methods=['GET'])
def jobs():
    global JOBLIST
    retlist = {'jobs': []}
    for job in JOBLIST:
        retlist['jobs'].append(JOBLIST[job].get_state())

    return Response(json.dumps(retlist), mimetype="application/json")


@app.route("/get_info", methods=['GET'])
def get_info():
    global JOBLIST
    if ('id_no' in request.args):
        id_no = int(request.args['id_no'])
        if id_no in JOBLIST:
            dat = JOBLIST[id_no].get_state()
            return Response(json.dumps(dat), mimetype="application/json")
        else:
            return Response('{}', mimetype="application/json")


@app.route("/get_log", methods=['GET'])
def get_log():
    global JOBLIST
    if ('id_no' in request.args):
        id_no = int(request.args['id_no'])
        if id_no in JOBLIST:
            dat = JOBLIST[id_no].get_log()
            return Response(json.dumps(dat), mimetype="application/json")
        else:
            return Response('{}', mimetype="application/json")


@app.route("/stop", methods=['GET'])
def stop():
    global JOBLIST
    if ('id_no' in request.args):
        id_no = int(request.args['id_no'])
        if id_no in JOBLIST:
            JOBLIST[id_no].stop()
            ret = {'result': 'success'}
            return Response(json.dumps(ret), mimetype="application/json")
        elif id_no == -1:
            for key in JOBLIST:
                if JOBLIST[key].running:
                    JOBLIST[key].stop()
        else:
            return Response('{}', mimetype="application/json")


@app.route("/tcp_start", methods=['GET'])
def tcp_start():
    global JOBLIST
    global ID_NO

    if ('dest' in request.args) and ('dur' in request.args) and ('pair' in request.args):
        newjob = Iperftcp(request.args['dest'], int(request.args['dur']), int(request.args['pair']))
        newjob.start()
        JOBLIST[ID_NO] = newjob
        ret = {'result': 'success', 'id_no': ID_NO}
        ID_NO += 1
        return Response(json.dumps(ret), mimetype="application/json")
    else:
        ret = {'result': 'fail'}
        return Response(json.dumps(ret), mimetype="application/json")


@app.route("/udp_start", methods=['GET'])
def udp_start():
    global JOBLIST
    global ID_NO

    if ('dest' in request.args) and ('dur' in request.args) and ('bw' in request.args):
        newjob = Iperfudp(request.args['dest'], int(request.args['dur']), int(request.args['bw']))
        newjob.start()
        JOBLIST[ID_NO] = newjob
        ret = {'result': 'success', 'id_no': ID_NO}
        ID_NO += 1
        return Response(json.dumps(ret), mimetype="application/json")
    else:
        ret = {'result': 'fail'}
        return Response(json.dumps(ret), mimetype="application/json")


@app.route("/udp_server", methods=['GET'])
def udp_server():
    global JOBLIST
    global ID_NO

    newjob = Iperfs(stype='udps')
    newjob.start()
    JOBLIST[ID_NO] = newjob
    ret = {'result': 'success', 'id_no': ID_NO}
    ID_NO += 1
    return Response(json.dumps(ret), mimetype="application/json")


@app.route("/tcp_server", methods=['GET'])
def tcp_server():
    global JOBLIST
    global ID_NO

    newjob = Iperfs(stype='tcps')
    newjob.start()
    JOBLIST[ID_NO] = newjob
    ret = {'result': 'success', 'id_no': ID_NO}
    ID_NO += 1
    return Response(json.dumps(ret), mimetype="application/json")


@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=4444)
