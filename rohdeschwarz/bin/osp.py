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
    parser.add_argument('--driver')
    parser.add_argument('--log', default='',
                        help='SCPI command log filename')
    args = parser.parse_args()

    osp_switch = OspSwitch()
    if not args.driver:
        print('Switch matrix driver is required')
        parser.print_help()
        sys.exit(1)
    try:
        switch_dict = {}
        with open(args.driver, 'r') as f:
            switch_dict = yaml.safe_load(f.read())
        if args.visa:
            osp_switch.open(args.visa, args.address)
        else:
            osp_switch.open_tcp(args.address)

        if osp_switch.connected():
            print("connected: {0}".format(osp_switch.id_string()))
            if args.log:
                osp_switch.open_log(args.log)
                osp_switch.log.write('{0}\n'.format(datetime.datetime.now()))
                osp_switch.log.write('--------------------------\n\n')
                osp_switch.print_info()
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
        if osp_switch.log:
            osp_switch.close_log()
        if osp_switch.connected():
            osp_switch.close()

if __name__ == "__main__":
    main()
    sys.exit(0)
