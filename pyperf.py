import re
from bopen import Bopen


def parse_udp(lines):
    """parse udp iperf log, returns avg. val times sample cnt"""
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


class Iperftcp(object):
    def __init__(self, destination, duration=10, pairs=1, name=''):
        self.running = False
        self.log = []
        self._name = name
        self._duration = duration
        self._destination = destination
        self._pairs = pairs
        self._handle = Bopen(['iperf',
                              '-c', destination,
                              '-P', str(pairs),
                              '-t', str(duration),
                              '-i', '1',
                              '-f', 'm'], self._done)
    def get_type(self):
        return 'tcp_client'

    def get_port(self):
        return 5001

    def _done(self):
        self.running = False
        self.log = self._handle.get_output()

    def get_state(self):
        return {'type': 'tcp',
                'duration': self._duration,
                'destination': self._destination,
                'pairs': self._pairs,
                'running': self.running
                }

    def get_log(self):
        self.log = self._handle.get_output()
        return {'type': 'tcp',
                'duration': self._duration,
                'destination': self._destination,
                'pairs': self._pairs,
                'log': self.log,
                'running': self.running
                }

    def get_parsed(self):
        return {'tput': parse_udp(self.get_log()['log']), 'running': self.running}

    def get_name(self):
        return self._name

    def start(self):
        self.running = True
        self._handle.start()

    def stop(self):
        self.log = self._handle.get_output()
        if self.running:
            self.running = False
            self._handle.stop()


class Iperfudp(object):
    def __init__(self, destination, duration=10, bw=1, port='default', name=''):
        self.running = False
        self.log = []
        self._name = name
        self._port = port
        self._duration = duration
        self._destination = destination
        self._bw = bw
        self._handle = Bopen(['iperf',
                              '-c', destination,
                              '-b', str(bw) + 'm',
                              '-t', str(duration),
                              '-i', '1',
                              '-f', 'm'], self._done)

    def get_type(self):
        return 'udp_client'

    def get_port(self):
        return 5001

    def _done(self):
        self.running = False
        self.log = self._handle.get_output()

    def get_state(self):
        return {'type': 'udp',
                'duration': self._duration,
                'destination': self._destination,
                'bw': self._bw,
                'running': self.running
                }

    def get_log(self):
        self.log = self._handle.get_output()
        return {'type': 'udp',
                'duration': self._duration,
                'destination': self._destination,
                'bw': self._bw,
                'log': self.log,
                'running': self.running
                }

    def get_parsed(self):
        return {'tput': parse_udp(self.get_log()['log']), 'running': self.running}

    def get_name(self):
        return self._name

    def start(self):
        self.running = True
        self._handle.start()

    def stop(self):
        self.log = self._handle.get_output()
        if self.running:
            self.running = False
            self._handle.stop()


class Iperfs(object):
    def __init__(self, stype='tcps', name=''):
        self.running = False
        self._name = name
        self.log = []
        self._stype = stype
        if stype == 'tcps':
            self._handle = Bopen(['iperf',
                                  '-s',
                                  '-i', '1',
                                  '-f', 'm'], self._done)
        elif stype == 'udps':
            self._handle = Bopen(['iperf',
                                  '-s',
                                  '-u',
                                  '-i', '1',
                                  '-f', 'm'], self._done)

    def _done(self):
        self.running = False
        self.log = self._handle.get_output()

    def get_type(self):
        if self._stype == 'tcps':
            return 'tcp_server'
        else:
            return 'udp_server'

    def get_port(self):
        return 5001

    def get_state(self):
        return {'type': self._stype,
                'running': self.running
                }

    def get_log(self):
        self.log = self._handle.get_output()
        return {'type': self._stype,
                'log': self.log,
                'running': self.running
                }

    def get_parsed(self):
        return {'tput': parse_udp(self.get_log()['log']), 'running': self.running}

    def get_name(self):
        return self._name

    def start(self):
        self.running = True
        self._handle.start()

    def stop(self):
        self.log = self._handle.get_output()
        if self.running:
            self.running = False
            self._handle.stop()


def main():
    pass

if __name__ == '__main__':
    main()
