from   rohdeschwarz.instruments.ospswitch import OspSwitch

from   ruamel import yaml

import argparse
import code
import datetime
import os
import sys

def main():
    parser = argparse.ArgumentParser(description='Connect to a Rohde & Schwarz OSP Switch')
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
    parser.add_argument('driver')
    args = parser.parse_args()

    if args.log and args.log_to_stdout:
        print('error: cannot use both --log and --log-to-stdout')
        parser.print_help()

    if not args.driver:
        print('Switch matrix driver is required')
        parser.print_help()
        sys.exit(0)

    switch_dict = {}
    try:
        with open(args.driver, 'r') as f:
            switch_dict = yaml.safe_load(f.read())
        assert switch_dict
    except:
        print('Could not read driver file')
        sys.exit(0)

    osp = OspSwitch(switch_dict)
    try:
        if args.visa:
            osp.open(args.visa, args.address)
        else:
            osp.open_tcp(args.address, args.port)
        if args.timeout:
            osp.timeout_ms = args.timeout

        if osp.connected():
            print("connected: {0}".format(osp.id_string()))
            if args.log:
                osp.open_log(args.log)
                osp.log.write('{0}\n'.format(datetime.datetime.now()))
                osp.log.write('--------------------------\n\n')
                osp.print_info()
            elif args.log_to_stdout:
                vna.log = sys.stdout
            sys.path.insert(0, os.getcwd())
            code.interact('', local=locals())
        else:
            print('Could not connect to instrument\n')
            parser.print_help()
    except FileNotFoundError:
        print('Could not find driver')
        parser.print_help()
    except SystemExit:
        pass
    except:
        raise Exception('Error connecting to instrument')
        parser.print_help()
    finally:
        if osp.log:
            osp.close_log()
        if osp.connected():
            osp.close()

if __name__ == "__main__":
    main()
    sys.exit(0)
