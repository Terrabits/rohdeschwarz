interfaces:
- asrl
- gpib
- pxi


def vxi11_instrument_resource(interface, *addresses):
    address_str = '::'.join(addresses)
    return f'{interface}::{addresses_str}::instr'
