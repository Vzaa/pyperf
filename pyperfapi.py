import json
import requests

URLS = {'info': '/get_info',
        'log': '/get_log',
        'stop': '/stop',
        'tcp_start': '/tcp_start',
        'udp_start': '/udp_start',
        'tcp_server': '/tcp_server',
        'udp_server': '/udp_server'}


def udp_server_start(hostname, port, name=''):
    url = 'http://' + hostname + ':' + str(port) + URLS['udp_server']
    params = {'name': name}
    serve_req = requests.get(url, params=params)
    serv_handle = json.loads(serve_req.text)
    #print serv_handle['id_no']
    return serv_handle['id_no']


def tcp_server_start(hostname, port, name=''):
    url = 'http://' + hostname + ':' + str(port) + URLS['tcp_server']
    params = {'name': name}
    serve_req = requests.get(url, params=params)
    serv_handle = json.loads(serve_req.text)
    #print serv_handle['id_no']
    return serv_handle['id_no']


def udp_client_start(hostname, port, dest, dur, bw, name=''):
    url = 'http://' + hostname + ':' + str(port) + URLS['udp_start']
    params = {'dest': dest, 'dur': dur, 'bw': bw, 'name': name}
    client_req = requests.get(url, params=params)
    cli_handle = json.loads(client_req.text)
    return cli_handle['id_no']


def tcp_client_start(hostname, port, dest, dur, pair, name=''):
    url = 'http://' + hostname + ':' + str(port) + URLS['tcp_start']
    params = {'dest': dest, 'dur': dur, 'pair': pair, 'name': name}
    client_req = requests.get(url, params=params)
    cli_handle = json.loads(client_req.text)
    return cli_handle['id_no']


def get_info(hostname, port, id_no):
    url = 'http://' + hostname + ':' + str(port) + URLS['info']
    params = {'id_no': id_no}
    info_req = requests.get(url, params=params)
    info = json.loads(info_req.text)
    return info


def get_log(hostname, port, id_no):
    url = 'http://' + hostname + ':' + str(port) + URLS['log']
    params = {'id_no': id_no}
    log_req = requests.get(url, params=params)
    log = json.loads(log_req.text)
    return log


def stop(hostname, port, id_no):
    url = 'http://' + hostname + ':' + str(port) + URLS['stop']
    params = {'id_no': id_no}
    info_req = requests.get(url, params=params)
    info = json.loads(info_req.text)
    return info


def main():
    pass

if __name__ == '__main__':
    main()

