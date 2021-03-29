from   .buffer         import Buffer
from   .c_visa_library import CVisaLibrary
from   .definitions    import Attributes, ErrorCodes, Types
import ctypes


class VisaLibrary:
    def __init__(self):
        self._visa   = CVisaLibrary()
        self._status = None

    def is_success(self):
        return self._status == ErrorCodes.VI_SUCCESS

    def openDefaultRM(self):
        resource_mgr = Types.ViSession()
        self._status = self._visa.viOpenDefaultRM(ctypes.byref(resource_mgr))
        return resource_mgr.value

    def open(self, resource_mgr, resource, timeout_ms):
        resource_mgr = Types.ViSession(resource_mgr)
        resource     = ctypes.create_string_buffer(resource.encode())
        access_mode  = Types.ViUInt32(0)
        timeout_ms   = Types.ViUInt32(timeout_ms)
        instr        = Types.ViSession()
        self._status = self._visa.viOpen(resource_mgr, resource, access_mode, timeout_ms, ctypes.byref(instr))
        return instr.value

    def close(self, session):
        session = Types.ViObject(session)
        self._status = self._visa.viClose(session)
        return self.is_success

    def set_timeout_ms(self, instr, timeout_ms):
        instr      = Types.ViSession(instr)
        timeout_ms = Types.ViAttrState(timeout_ms)
        self._status = self._visa.viSetAttribute(instr, Attributes.VI_ATTR_TMO_VALUE, timeout_ms)
        return self.is_success

    def set_termchar_en(self, instr, enable):
        instr  = Types.ViSession(instr)
        enable = Types.ViAttrState(enable)
        self._status = self._visa.viSetAttribute(instr, Attributes.VI_ATTR_TERMCHAR_EN, enable)
        return self.is_success

    def set_send_end_en(self, instr, enable):
        instr  = Types.ViSession(instr)
        enable = Types.ViAttrState(enable)
        self._status = self._visa.viSetAttribute(instr, Attributes.VI_ATTR_SEND_END_EN, enable)
        return self.is_success

    def read(self, instr, buffer):
        instr       = Types.ViSession(instr)
        buffer_size = Types.ViUInt32(buffer.size)
        byte_count  = Types.ViUInt32()
        self._status = self._visa.viRead(instr, buffer.to_ViBuf(), buffer_size, ctypes.byref(byte_count))
        return buffer.value

    def write(self, instr, data):
        instr     = Types.ViSession(instr)
        bytes_in  = Types.ViUInt32(len(data))
        bytes_out = Types.ViUInt32()
        data      = ctypes.cast(data, Types.ViBuf)
        self._status = self._visa.viWrite(instr, data, bytes_in, ctypes.byref(bytes_out))
        return self.is_success
