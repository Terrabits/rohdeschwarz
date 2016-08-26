import argparse
import datetime
import code
import os
from rohdeschwarz.instruments.genericinstrument import GenericInstrument

def main():
    parser = argparse.ArgumentParser(description='Connect to an instrument')
    parser.add_argument('--visa', metavar='bus', default=False,
                        help="use VISA with 'bus'")
    parser.add_argument('--address', default='127.0.0.1',
                        help='instrument address')
    parser.add_argument('--log', default='',
                        help='SCPI command log filename')
    args = parser.parse_args()

    instr = GenericInstrument()
    try:
        if args.visa:
            instr.open(args.visa, args.address)
        else:
            instr.open_tcp(args.address)

        if instr.connected():
            print("connected: {0}".format(instr.id_string()))
            if args.log:
                instr.open_log(args.log)
                instr.log.write('{0}\n'.format(datetime.datetime.now()))
                instr.log.write('--------------------------\n\n')
                instr.print_info()
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
        if instr.log:
            instr.close_log()
        if instr.connected():
            instr.close()

if __name__ == "__main__":
    main()
