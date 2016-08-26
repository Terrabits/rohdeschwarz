import argparse
import datetime
import code
import os
from rohdeschwarz.instruments.vna import Vna

def main():
    parser = argparse.ArgumentParser(description='Connect to a Rohde & Schwarz VNA')
    parser.add_argument('--visa', metavar='bus', default=False,
                        help="use VISA with 'bus'")
    parser.add_argument('--address', default='127.0.0.1',
                        help='instrument address')
    parser.add_argument('--log', default='',
                        help='SCPI command log filename')
    args = parser.parse_args()

    vna = Vna()
    try:
        if args.visa:
            vna.open(args.visa, args.address)
        else:
            vna.open_tcp(args.address)

        if vna.connected():
            print("connected: {0}".format(vna.id_string()))
            if args.log:
                vna.open_log(args.log)
                vna.log.write('{0}\n'.format(datetime.datetime.now()))
                vna.log.write('--------------------------\n\n')
                vna.print_info()
            code.interact('', local=locals())
        else:
            print('Could not connect to instrument\n')
            parser.print_help()
    except SystemExit:
        pass
    except:
        print('Error connecting to instrument\n')
        parser.print_help()
    finally:
        if vna.log:
            vna.close_log()
        if vna.connected():
            vna.close()

if __name__ == "__main__":
    main()
