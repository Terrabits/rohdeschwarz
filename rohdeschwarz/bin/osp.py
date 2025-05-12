from   rohdeschwarz.instruments.ospswitch import OspSwitch
from   rohdeschwarz.yaml import load_yaml
import argparse
import code
import datetime
import os
from   pathlib import Path
import sys


def main():


    # create command line interface
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


    # parse args
    args = parser.parse_args()


    # check log settings
    if args.log and args.log_to_stdout:
        print('error: cannot use both --log and --log-to-stdout')
        parser.print_help()
        sys.exit(1)


    # check driver file
    if not args.driver:
        print('Switch matrix driver is required')
        parser.print_help()
        sys.exit(2)


    # get driver file
    driver_file = Path(args.driver)
    if not driver_file.exists():
        print('Driver file does not exist')
        sys.exit(3)


    # parse driver file
    switches = load_yaml(driver_file)
    if not switches:
        print('No switch definitions found in driver file')
        sys.exit(4)


    # init osp

    osp = OspSwitch(switches)

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
                osp.log = sys.stdout
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
