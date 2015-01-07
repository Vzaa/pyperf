import json
from pyperf import Iperftcp, Iperfudp, Iperftcps, Iperfudps
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, Response, jsonify

app = Flask(__name__)

ID_NO = 0
JOBLIST = {}


@app.route("/ipc.sh", methods=['GET'])
def ipc_sh():
    global JOBLIST
    ret = {}
    if ('cmd' in request.args):
        cmd = request.args['cmd']
        if cmd == 'udp_listener_list':
            ret['udp_listeners'] = []
            for key in JOBLIST:
                if JOBLIST[key].is_running() and JOBLIST[key].get_type() == 'udp_server':
                    ret['udp_listeners'].append({'port': JOBLIST[key].get_port()})
            return jsonify(ret)
    return jsonify({})


@app.route("/jobs", methods=['GET'])
def jobs():
    global JOBLIST
    retlist = {'jobs': []}
    for job in JOBLIST:
        retlist['jobs'].append(JOBLIST[job].get_state())

    return jsonify(retlist)


@app.route("/get_info", methods=['GET'])
def get_info():
    global JOBLIST
    if ('id_no' in request.args):
        id_no = int(request.args['id_no'])
        if id_no in JOBLIST:
            dat = JOBLIST[id_no].get_state()
            return jsonify(dat)
        else:
            return jsonify({})


@app.route("/get_parsed", methods=['GET'])
def get_parsed():
    global JOBLIST
    if ('id_no' in request.args):
        id_no = int(request.args['id_no'])
        if id_no in JOBLIST:
            dat = JOBLIST[id_no].get_parsed_dict()
            return jsonify(dat)
        else:
            return jsonify({})


@app.route("/get_log", methods=['GET'])
def get_log():
    global JOBLIST
    if ('id_no' in request.args):
        id_no = int(request.args['id_no'])
        if id_no in JOBLIST:
            dat = JOBLIST[id_no].get_log_dict()
            return jsonify(dat)
        else:
            return jsonify({})


@app.route("/stop", methods=['GET'])
def stop():
    global JOBLIST
    if ('id_no' in request.args):
        id_no = int(request.args['id_no'])
        if id_no in JOBLIST:
            JOBLIST[id_no].stop()
            ret = {'result': 'success'}
            return jsonify(ret)
        elif id_no == -1:
            for key in JOBLIST:
                if JOBLIST[key].is_running():
                    JOBLIST[key].stop()
            return jsonify({})
        else:
            return jsonify({})


@app.route("/tcp_start", methods=['GET'])
def tcp_start():
    global JOBLIST
    global ID_NO

    if ('dest' in request.args) and ('dur' in request.args) and ('pair' in request.args):
        newjob = Iperftcp(request.args['dest'], int(request.args['dur']),
                          int(request.args['pair']), name=request.args['name'])
        newjob.start()
        JOBLIST[ID_NO] = newjob
        ret = {'result': 'success', 'id_no': ID_NO}
        ID_NO += 1
        return jsonify(ret)
    else:
        ret = {'result': 'fail'}
        return jsonify(ret)


@app.route("/udp_start", methods=['GET'])
def udp_start():
    global JOBLIST
    global ID_NO

    if ('dest' in request.args) and ('dur' in request.args) and ('bw' in request.args):
        newjob = Iperfudp(request.args['dest'], int(request.args['dur']),
                          int(request.args['bw']), name=request.args['name'])
        newjob.start()
        JOBLIST[ID_NO] = newjob
        ret = {'result': 'success', 'id_no': ID_NO}
        ID_NO += 1
        return jsonify(ret)
    else:
        ret = {'result': 'fail'}
        return jsonify(ret)


@app.route("/udp_server", methods=['GET'])
def udp_server():
    global JOBLIST
    global ID_NO

    newjob = Iperfudps(name=request.args['name'])
    newjob.start()
    JOBLIST[ID_NO] = newjob
    ret = {'result': 'success', 'id_no': ID_NO}
    ID_NO += 1
    return jsonify(ret)


@app.route("/tcp_server", methods=['GET'])
def tcp_server():
    global JOBLIST
    global ID_NO

    newjob = Iperftcps(name=request.args['name'])
    newjob.start()
    JOBLIST[ID_NO] = newjob
    ret = {'result': 'success', 'id_no': ID_NO}
    ID_NO += 1
    return jsonify(ret)


@app.route("/")
def hello():
    global JOBLIST
    return render_template('list.html', joblist=JOBLIST)
    #return "Hello World!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=4444)
