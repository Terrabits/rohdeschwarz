from .command_line import parse
import code
import datetime
import os
from rohdeschwarz.instruments import Instrument
import sys


def run_cli(Class=Instrument, variable_name):
    class_name = Class.__class__.__name__
    args       = parse(class_name)

    instr = Class()

    # connect
    connect_kwargs = {}
    if args.visa_resource:
        connect_fn   = instr.open
        connect_kwargs['resource'] = args.address_or_resource
    else:
        connect_fn   = instr.open_tcp
        connect_kwargs['address'] = args.address_or_resource
        if args.tcp_socket:
            connect_kwargs['port'] = args.tcp_socket
    if args.timeout_ms:
        connect_kwargs[''] = args.timeout_ms

    # TODO: try/catch, error check
    connect_fn(**connect_kwargs)

    # connected
    print(f"connected: {instr.id_string}")

    # log file?
    if args.log_file:
        instr.open_log(args.log_file)
        instr.log.print(f'{datetime.datetime.now()}\n')
        instr.log.print('--------------------------\n\n')
        instr.print_info()

    # log to stdout?
    if args.log_to_stdout:
        instr.log_to_stdout()

    # look for libraries in current path
    sys.path.insert(0, os.getcwd())

    # python prompt
    local_vars = locals()
    local_vars[variable_name] = instr
    try:
        code.interact('', local_vars)
    except SystemExit:
        pass
    finally:
        if instr.is_log:
            instr.close_log()
        if instr.is_open:
            instr.close()
