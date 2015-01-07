import re
from bopen import Bopen


def parse_udp(lines):
    dat = []

    idx = 0
    for line in lines:
        line = line.strip()
        if re.match(r'.*bits/sec.*', line):
            tputstr = re.search(r'[0-9]+(\.[0-9]+)? .?bits/sec', line).group(0)
            tputstr = re.search(r'[0-9]+(\.[0-9]+)?', tputstr).group(0)
            tput = float(tputstr)
            dat.append([idx, tput])
            idx += 1
    return dat


class Iperfjob(object):
    def __init__(self, name='', port=5001):
        self._running = False
        self._log = []
        self._name = name
        self._port = port
        self._handle = None
        self._type = ''
        self._log_parser = parse_udp

    def get_port(self):
        return self._port

    def get_type(self):
        return self._type

    def _done(self):
        self._running = False
        self._log = self._handle.get_output()

    def start(self):
        self._running = True
        self._handle.start()


    def get_name(self):
        return self._name

    def stop(self):
        self._log = self._handle.get_output()
        if self._running:
            self._running = False
            self._handle.stop()

    def get_log(self):
        self._log = self._handle.get_output()
        return self._log

    def get_parsed_dict(self):
        return {'tput': self._log_parser(self.get_log()),
                'running': self._running}

    def get_log_dict(self):
        self._log = self._handle.get_output()
        return {'type': self._type,
                'log': self._log,
                'running': self._running
                }

    def get_state(self):
        return {'type': self._type,
                'running': self._running
                }

    def is_running(self):
        return self._running


class Iperftcp(Iperfjob):
    def __init__(self, destination, duration=10, pairs=1, name=''):
        Iperfjob.__init__(self, name=name)
        self._type = 'tcp_client'
        self._duration = duration
        self._destination = destination
        self._pairs = pairs
        self._handle = Bopen(['iperf',
                              '-c', destination,
                              '-P', str(pairs),
                              '-t', str(duration),
                              '-i', '1',
                              '-f', 'm'], self._done)


class Iperfudp(Iperfjob):
    def __init__(self, destination, duration=10, bw=1,
                 name=''):
        Iperfjob.__init__(self, name=name)
        self._type = 'udp_client'
        self._duration = duration
        self._destination = destination
        self._bw = bw
        self._handle = Bopen(['iperf',
                              '-c', destination,
                              '-b', str(bw) + 'm',
                              '-t', str(duration),
                              '-i', '1',
                              '-f', 'm'], self._done)


class Iperfudps(Iperfjob):
    def __init__(self, name=''):
        Iperfjob.__init__(self, name=name)
        self._type = 'udp_server'
        self._handle = Bopen(['iperf',
                              '-s',
                              '-u',
                              '-i', '1',
                              '-f', 'm'], self._done)


class Iperftcps(Iperfjob):
    def __init__(self, name=''):
        Iperfjob.__init__(self, name=name)
        self._type = 'tcp_server'
        self._handle = Bopen(['iperf',
                              '-s',
                              '-i', '1',
                              '-f', 'm'], self._done)


def main():
    pass

if __name__ == '__main__':
    main()
