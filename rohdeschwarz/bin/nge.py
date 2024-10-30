from   rohdeschwarz.instruments.powersupply import Nge

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

    nge = Nge()
    try:
        if args.visa:
            nge.open(args.visa, args.address)
        else:
            nge.open_tcp(args.address, args.port)
        if args.timeout:
            nge.timeout_ms = args.timeout

        if nge.connected():
            print("connected: {0}".format(nge.id_string()))
            if args.log:
                nge.open_log(args.log)
                nge.log.write('{0}\n'.format(datetime.datetime.now()))
                nge.log.write('--------------------------\n\n')
                nge.print_info()
            elif args.log_to_stdout:
                nge.log = sys.stdout
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
        if nge.log:
            nge.close_log()
        if nge.connected():
            nge.close()

if __name__ == "__main__":
    main()
    sys.exit(0)
