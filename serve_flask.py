import redis
import atexit
import json
import threading
import signal
import sys
from pyperf import Iperftcp, Iperfudp, Iperftcps, Iperfudps
from pyperf import parse_udp
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, Response, jsonify

app = Flask(__name__)

red = redis.StrictRedis()
JOBLIST = {}
JOBLOCK = threading.Lock()


@app.route("/ipc.sh", methods=['GET'])
def ipc_sh():
    with JOBLOCK:
        global JOBLIST
        ret = {}
        if ('cmd' in request.args):
            cmd = request.args['cmd']
            if cmd == 'udp_listener_list':
                ret['udp_listeners'] = []
                for key in JOBLIST:
                    if JOBLIST[key].is_running() and JOBLIST[
                            key].get_type() == 'udp_server':
                        ret['udp_listeners'].append({
                            'port': JOBLIST[key].get_port()
                        })
                return jsonify(ret)
        return jsonify({})


@app.route("/jobs", methods=['GET'])
def jobs():
    with JOBLOCK:
        global JOBLIST
        retlist = {'jobs': []}
        for job in JOBLIST:
            retlist['jobs'].append(JOBLIST[job].get_state())

        return jsonify(retlist)


@app.route("/get_info", methods=['GET'])
def get_info():
    with JOBLOCK:
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
    with JOBLOCK:
        global JOBLIST
        if ('id_no' in request.args):
            id_no = int(request.args['id_no'])
            if id_no in JOBLIST:
                dat = JOBLIST[id_no].get_parsed_dict()
                return jsonify(dat)
            else:
                ret = dict()
                ret['running'] = False
                ret['tput'] = parse_udp(red.get('log:%s' % id_no).split('\n'))
                return jsonify(ret)


@app.route("/get_log", methods=['GET'])
def get_log():
    with JOBLOCK:
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
    with JOBLOCK:
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
    with JOBLOCK:
        global JOBLIST

        if ('dest' in request.args) and ('dur' in request.args) and (
                'pair' in request.args):
            ID_NO = red.incr('id_no')
            newjob = Iperftcp(
                ID_NO,
                request.args['dest'],
                int(request.args['dur']),
                int(request.args['pair']),
                name=request.args['name'])
            newjob.start()
            JOBLIST[ID_NO] = newjob
            ret = {'result': 'success', 'id_no': ID_NO}
            return jsonify(ret)
        else:
            ret = {'result': 'fail'}
            return jsonify(ret)


@app.route("/udp_start", methods=['GET'])
def udp_start():
    with JOBLOCK:
        global JOBLIST

        if ('dest' in request.args) and ('dur' in request.args) and (
                'bw' in request.args):
            ID_NO = red.incr('id_no')
            newjob = Iperfudp(
                ID_NO,
                request.args['dest'],
                int(request.args['dur']),
                int(request.args['bw']),
                name=request.args['name'])
            newjob.start()
            JOBLIST[ID_NO] = newjob
            ret = {'result': 'success', 'id_no': ID_NO}
            return jsonify(ret)
        else:
            ret = {'result': 'fail'}
            return jsonify(ret)


@app.route("/udp_server", methods=['GET'])
def udp_server():
    with JOBLOCK:
        global JOBLIST

        ID_NO = red.incr('id_no')
        newjob = Iperfudps(ID_NO, name=request.args['name'])
        newjob.start()
        JOBLIST[ID_NO] = newjob
        ret = {'result': 'success', 'id_no': ID_NO}
        return jsonify(ret)


@app.route("/tcp_server", methods=['GET'])
def tcp_server():
    with JOBLOCK:
        global JOBLIST

        ID_NO = red.incr('id_no')
        newjob = Iperftcps(ID_NO, name=request.args['name'])
        newjob.start()
        JOBLIST[ID_NO] = newjob
        ret = {'result': 'success', 'id_no': ID_NO}
        return jsonify(ret)


@app.route("/")
def hello():
    with JOBLOCK:
        global JOBLIST
        joblist = dict()
        ID_NO = int(red.get('id_no'))

        for id_no in xrange(1, ID_NO + 1):
            item = dict()
            if id_no in JOBLIST:
                item['name'] = JOBLIST[id_no].get_name()
                item['running'] = JOBLIST[id_no].is_running()
                joblist[id_no] = item
            else:
                entry = red.get('name:%s' % id_no)
                if entry is not None:
                    props = json.loads(entry)
                    name_str = ""
                    for key in props:
                        name_str += '%s -> %s ' % (key, props[key])
                    item['name'] = name_str
                    item['running'] = False
                    joblist[id_no] = item

        return render_template('list.html', joblist=joblist)


@app.before_request
def before_request():
    pass


@app.teardown_request
def teardown_request(exception):
    pass


def cleanup():
    global JOBLIST
    for job in JOBLIST.values():
        job.stop()
        while not job.did_quit():
            pass


if __name__ == "__main__":
    atexit.register(cleanup)
    app.run(host='0.0.0.0', debug=True, port=4444)
