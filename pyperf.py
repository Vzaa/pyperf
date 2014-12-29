from bopen import Bopen


class Iperftcp(object):
    def __init__(self, destination, duration=10, pairs=1):
        self.running = False
        self.log = []
        self._duration = duration
        self._destination = destination
        self._pairs = pairs
        self._handle = Bopen(['iperf',
                              '-c', destination,
                              '-P', str(pairs),
                              '-t', str(duration),
                              '-i', '1',
                              '-f', 'm'], self._done)

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

    def start(self):
        self.running = True
        self._handle.start()

    def stop(self):
        self.log = self._handle.get_output()
        self.running = False
        self._handle.stop()


class Iperfudp(object):
    def __init__(self, destination, duration=10, bw=1):
        self.running = False
        self.log = []
        self._duration = duration
        self._destination = destination
        self._bw = bw
        self._handle = Bopen(['iperf',
                              '-c', destination,
                              '-b', str(bw) + 'm',
                              '-t', str(duration),
                              '-i', '1',
                              '-f', 'm'], self._done)

    def _done(self):
        self.running = False
        self.log = self._handle.get_output()

    def get_state(self):
        self.log = self._handle.get_output()
        return {'type': 'udp',
                'duration': self._duration,
                'destination': self._destination,
                'bw': self._bw,
                'log': self.log,
                'running': self.running
                }

    def start(self):
        self.running = True
        self._handle.start()

    def stop(self):
        self.log = self._handle.get_output()
        self.running = False
        self._handle.stop()


class Iperfs(object):
    def __init__(self, stype='tcps'):
        self.running = False
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

    def get_state(self):
        self.log = self._handle.get_output()
        return {'type': self._stype,
                'log': self.log,
                'running': self.running
                }

    def start(self):
        self.running = True
        self._handle.start()

    def stop(self):
        self.log = self._handle.get_output()
        self.running = False
        self._handle.stop()


def main():
    """TODO: Docstring for main.
    :returns: TODO

    """
    asd = Iperftcp('localhost', 5)
    asd.start()
    while asd.running:
        pass
    print asd.log

if __name__ == '__main__':
    main()
