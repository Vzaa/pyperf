import subprocess as sub
import threading


class Bopen(object):
    def __init__(self, cmd_line, callback=None):
        """init stuff """
        self._cmd_line = cmd_line
        self._running = False
        self._proc = None
        self._buf = []
        self._thread = None
        self._lock = threading.Lock()
        self._callback = callback

    def start(self):
        #sub.Popen(cmd_line)
        self._proc = sub.Popen(self._cmd_line, stdin=sub.PIPE, stdout=sub.PIPE, stderr=sub.PIPE)
        self._running = True
        self._thread = threading.Thread(target=self.self_loop, args=())
        self._thread.start()

    def stop(self):
        self._proc.kill()
        self._running = False

    def self_loop(self):
        while True:
            line = self._proc.stdout.readline()
            if line:
                with self._lock:
                    self._buf.append(line)
            else:
                self._running = False
                self._proc.stderr.close()
                self._proc.stdin.close()
                self._proc.stdout.close()
                self._proc.wait()

                if self._callback is not None:
                    self._callback()
                break

    def get_output(self):
        readlines = None
        with self._lock:
            readlines = list(self._buf)
        return readlines

    def is_running(self):
        return self._running


def main():
    pass

if __name__ == '__main__':
    main()
