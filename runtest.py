import time
import pyperfapi as perf


def main():
    test = {'chains': '3x3', 'channel': 36}
    serv_id = perf.udp_server_start('localhost', 4444, name=test)
    cli_id = perf.udp_client_start(
        'localhost', 4444, 'localhost', 10, 5, name=test)
    print serv_id
    print cli_id


if __name__ == '__main__':
    main()
