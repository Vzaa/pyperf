import subprocess as sub
import threading
import time


class Bopen(object):
    def __init__(self, cmd_line, callback=None):
        """init stuff """
        self.cmd_line = cmd_line
        self.running = False
        self.proc = None
        self.q = []
        self.t = None
        self.lock = threading.Lock()
        self._callback = callback

    def start(self):
        #sub.Popen(cmd_line)
        self.proc = sub.Popen(self.cmd_line, stdin=sub.PIPE, stdout=sub.PIPE, stderr=sub.PIPE)
        self.running = True
        self.t = threading.Thread(target=self.self_loop, args=())
        self.t.start()

    def stop(self):
        self.proc.kill()
        self.running = False

    def self_loop(self):
        while True:
            line = self.proc.stdout.readline()
            if line:
                self.lock.acquire()
                self.q.append(line)
                self.lock.release()
            else:
                self.running = False
                self.proc.stderr.close()
                self.proc.stdin.close()
                self.proc.stdout.close()
                self.proc.wait()

                if self._callback is not None:
                    self._callback()
                break

    def get_output(self):
        self.lock.acquire()
        readlines = list(self.q)
        self.lock.release()
        return readlines


def main():
    pass

if __name__ == '__main__':
    main()
