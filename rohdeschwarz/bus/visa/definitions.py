import ctypes


class Types:
    # basic types
    ViBoolean = ctypes.c_bool
    ViUInt32  = ctypes.c_uint
    ViPUint32 = ctypes.POINTER(ViUInt32)
    ViInt32   = ctypes.c_int
    ViPInt32  = ctypes.POINTER(ViInt32)
    ViChar    = ctypes.c_char
    ViPChar   = ctypes.POINTER(ViChar)
    ViString  = ViPChar
    ViPString = ViPChar
    ViByte    = ctypes.c_ubyte
    ViPByte   = ctypes.POINTER(ViByte)

    # interface types
    ViStatus     = ctypes.c_int
    ViSession    = ctypes.c_uint
    ViPSession   = ctypes.POINTER(ViSession)
    ViRsrc       = ViPChar
    ViObject     = ctypes.c_uint
    ViPObject    = ctypes.POINTER(ViObject)
    ViAccessMode = ViUInt32
    ViAttr       = ViUInt32
    ViAttrState  = ViUInt32
    ViBuf        = ViPByte
    ViPBuf       = ViPByte


class ErrorCodes:
    VI_SUCCESS = ctypes.c_int(0)


class Attributes:
    VI_ATTR_SEND_END_EN = Types.ViAttr(0x3FFF0016)
    VI_ATTR_SUPPRESS_END_EN = Types.ViAttr(0x3FFF0036)
    VI_ATTR_TERMCHAR_EN = Types.ViAttr(0x3FFF0038)
    VI_ATTR_TMO_VALUE   = Types.ViAttr(0x3FFF001A)


class FunctionPrototypes:
    viOpenDefaultRM = {'restype':  Types.ViStatus,
                       'argtypes': [Types.ViPSession]}
    viOpen          = {'restype':  Types.ViStatus,
                       'argtypes': [Types.ViSession, Types.ViRsrc, Types.ViAccessMode, Types.ViUInt32, Types.ViPSession]}
    viClose         = {'restype':  Types.ViStatus,
                       'argtypes': [Types.ViObject]}
    viGetAttribute  = {'restype':  Types.ViStatus,
                       'argtypes': [Types.ViObject, Types.ViAttr, ctypes.c_void_p]}
    viSetAttribute  = {'restype':  Types.ViStatus,
                       'argtypes': [Types.ViObject, Types.ViAttr, Types.ViAttrState]}
    viStatusDesc    = {'restype':  Types.ViStatus,
                       'argtypes': [Types.ViObject, Types.ViStatus, Types.ViPChar]}
    viRead          = {'restype':  Types.ViStatus,
                       'argtypes': [Types.ViSession, Types.ViBuf, Types.ViUInt32, Types.ViPUint32]}
    viWrite         = {'restype':  Types.ViStatus,
                       'argtypes': [Types.ViSession, Types.ViBuf, Types.ViUInt32, Types.ViPUint32]}
