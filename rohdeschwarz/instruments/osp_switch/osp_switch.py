from ..instrument import Instrument
# from ..mixins     import scpi_method, scpi_property, ScpiMixin


class OSPSwitch(Instrument):
    def __init__(self):
        Instrument.__init__(self)

    # TODO
    #
    # set_switch = scpi_method(
    #     'ROUT:CLOS (@F{instrument:02d}A{module:02d}({state:02d}{switch:02d}))',
    #     instrument=int, module=int, state=int, switch=int )
    #
    # is_switch_state = scpi_method(
    #     'ROUT:CLOS? (@F{instrument:02d}A{module:02d}({state:02d}{switch:02d}))',
    #     instrument=int, module=int, state=int, switch=int,
    #     return_type=bool )
