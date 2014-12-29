import time
import pyperfapi as perf


def main():
    serv_id = perf.tcp_server_start('localhost', 4444)
    cli_id = perf.tcp_client_start('localhost', 4444, 'localhost', 10, 5)

    while True:
        cli_info = perf.get_info('localhost', 4444, cli_id)
        if cli_info['running']:
            time.sleep(1)
        else:
            break

    perf.stop('localhost', 4444, serv_id)

    cli_info = perf.get_info('localhost', 4444, cli_id)
    serv_info = perf.get_info('localhost', 4444, serv_id)

    for line in cli_info['log']:
        print line,

    for line in serv_info['log']:
        print line,

if __name__ == '__main__':
    main()
