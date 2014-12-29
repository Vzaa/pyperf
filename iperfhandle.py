"""iperf handler"""
import subprocess as sub
import Queue
import threading
import time


class IperfTcp(object):
    """iperf TCP class"""

    def __init__(self, destination, duration=10, pairs=1):
        """init stuff """
        self.destination = destination
        self.duration = duration
        self.pairs = pairs
        self.running = False
        self.proc = None
        self.q = []
        self.t = None
        self.lock = threading.Lock()

    def get_dict(self):
        return {'destination': self.destination,
                'duration': self.destination}

    def start(self):
        """@todo: Docstring for start
        :returns: @todo

        """
        cmd_line = ['iperf',
                '-i', '1',
                '-c', str(self.destination),
                '-t', str(self.duration),
                '-P', str(self.pairs)]
        #sub.Popen(cmd_line)
        self.proc = sub.Popen(cmd_line, stdin=sub.PIPE, stdout=sub.PIPE, stderr=sub.PIPE)
        self.running = True
        self.t = threading.Thread(target=self.self_loop, args=())
        self.t.start()

    def self_loop(self):
        while True:
            line = self.proc.stdout.readline()
            if line:
                self.lock.acquire()
                self.q.append(line)
                self.lock.release()
            else:
                self.running = False
                break

    def get_copy(self):
        self.lock.acquire()
        readlines = list(self.q)
        self.lock.release()
        return readlines


def main():
    """main"""
    handle = IperfTcp('localhost', 3)
    handle.start()

    while handle.running:
        time.sleep(1)
        print handle.get_copy()

if __name__ == '__main__':
    main()
