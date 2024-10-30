from   rohdeschwarz.instruments.powersupply import Ngu

import argparse
import code
import datetime
import os
import sys


def main():
    parser = argparse.ArgumentParser(description='Connect to a Rohde & Schwarz NGE Power Supply')
    parser.add_argument('--visa', metavar='bus', default=False,
                        help="use VISA with 'bus'")
    parser.add_argument('--address', default='127.0.0.1',
                        help='instrument address')
    parser.add_argument('--port',    default=5025, type=int,
                        help='port (TCP only)')
    parser.add_argument('--timeout', default=5000, type=int,
                        help='default instrument timeout (ms)')
    parser.add_argument('--log', default='',
                        help='SCPI command log filename')
    parser.add_argument('--log-to-stdout', action='store_true',
                        help='print all SCPI IO to stdout')
    args = parser.parse_args()

    if args.log and args.log_to_stdout:
        print('error: cannot use both --log and --log-to-stdout')
        parser.print_help()

    ngu = Ngu()
    try:
        if args.visa:
            ngu.open(args.visa, args.address)
        else:
            ngu.open_tcp(args.address, args.port)
        if args.timeout:
            ngu.timeout_ms = args.timeout

        if ngu.connected():
            print("connected: {0}".format(ngu.id_string()))
            if args.log:
                ngu.open_log(args.log)
                ngu.log.write('{0}\n'.format(datetime.datetime.now()))
                ngu.log.write('--------------------------\n\n')
                ngu.print_info()
            elif args.log_to_stdout:
                ngu.log = sys.stdout
            sys.path.insert(0, os.getcwd())
            code.interact('', local=locals())
            sys.exit(0)
        else:
            raise Exception('Could not connect to instrument')
    except SystemExit:
        pass
    except:
        print('Error connecting to instrument\n')
        parser.print_help()
    finally:
        if ngu.log:
            ngu.close_log()
        if ngu.connected():
            ngu.close()

if __name__ == "__main__":
    main()
    sys.exit(0)
