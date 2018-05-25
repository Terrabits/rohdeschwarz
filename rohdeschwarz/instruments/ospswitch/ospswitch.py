from   rohdeschwarz.instruments.genericinstrument import GenericInstrument
from   rohdeschwarz.instruments.ospswitch.enums   import Spdt

import re
from   ruamel import yaml

class OspSwitch(GenericInstrument):
    def __init__(self, switch_dict={}):
        super(OspSwitch, self).__init__()
        self.switches = switch_dict

    def __getattr__(self, name):
        if _is_switch_name(name):
            name = name.lower()
            if not name in self.switches:
                raise AttributeError("Switch '{0}' not found in switch_dict".format(name))
            address = self.switches[name.lower()]
            return self.switch_state(address)
        else:
            return GenericInstrument.__getattribute__(self, name)

    def __setattr__(self, name, value):
        if _is_switch_name(name):
            name = name.lower()
            if not name in self.switches:
                raise AttributeError("Switch '{0}' not found in switch_dict".format(name))
            address = self.switches[name]
            if self.is_switch_state(address, value):
                return
            self.close_switch(address, value)
        else:
            GenericInstrument.__setattr__(self, name, value)

    def close_switch(self, address, state):
        instr   = address['instrument']
        module  = address['module']
        switch  = address['switch']
        state = _interpret_switch_state(state)
        scpi = _close_switch_scpi(instr, module, switch, state)
        self.write(scpi)

    def switch_state(self, address):
        state = 0
        while not self.is_switch_state(address, state):
            state += 1
        return state

    def is_switch_state(self, address, state):
        instr   = address['instrument']
        module  = address['module']
        switch  = address['switch']
        state = _interpret_switch_state(state)
        scpi = _query_switch_scpi(instr, module, switch, state)
        result = self.query(scpi).strip()
        if result == '1':
            return True
        else:
            return False

    def set_switches(self, switch_states):
    	for switch, state in switch_states.items():
    		self.__setattr__(switch, state)
    	self.pause()

def _close_switch_scpi(instr, module, switch, state):
    scpi = 'ROUT:CLOS (@F{0:02d}A{1:02d}({2:02d}{3:02d}))'
    scpi = scpi.format(instr, module, state, switch)
    return scpi

def _query_switch_scpi(instr, module, switch, state):
    scpi = 'ROUT:CLOS? (@F{0:02d}A{1:02d}({2:02d}{3:02d}))'
    scpi = scpi.format(instr, module, state, switch)
    return scpi

def _is_switch_name(name):
    return re.match('^k\d+', name, flags=re.IGNORECASE)

def _interpret_switch_state(state):
    if isinstance(state, str):
        state = state.lower()
        if state == 'nc':
            state = Spdt.nc
        elif state == 'no':
            state = Spdt.no
    return int(state)
