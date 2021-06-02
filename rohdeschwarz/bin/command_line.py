import argparse


def parse(class_name):
    parser = argparse.ArgumentParser(description=f'Connect to a(n) {class_name}')
    parser.add_argument('--tcp-socket',    action='store_true', help='connect to TCP socket (default)')
    parser.add_argument('--visa-resource', action='store_true', help='connect to resource via VISA')
    parser.add_argument('--tcp-port',   type=int)
    parser.add_argument('--timeout-ms', type=int)
    parser.add_argument('--log-file')
    parser.add_argument('--log-to-stdout', action='store_true')
    parser.add_argument('address_or_resource')
    args = parser.parse_args()

    if args.tcp_socket and args.visa_resource:
        print('error: cannot use both --tcp-socket and --visa-resource')
        parser.print_help()

    if args.visa_resource and args.tcp_port:
        print('error: cannot use --tcp-port with --visa-resource.')
        print('If this is what you mean to do,')
        print('use visa resource port syntax instead:')
        print('  tcpip::address::port::socket')
        print('otherwise use --tcp-port (default)')

    if args.log_file and args.log_to_stdout:
        print('error: cannot use both --log and --log-to-stdout')
        parser.print_help()

    return args
