from __future__ import print_function
import sys
from cffi import FFI
import time
import threading

from .enitiy import button_pressed

def MessageHandler(lib, entity, config):


    while 1:
        gostr = lib.GetMessageFromFront()
        
        if gostr !=0:
            print(gostr)
            button_pressed(entity, gostr)

        time.sleep(0.5)

def StartMessageHandler(entity, config):
    is_64b = sys.maxsize > 2**32

    ffi = FFI()
    if is_64b: ffi.cdef("typedef long GoInt;\n")
    else:      ffi.cdef("typedef int GoInt;\n")

    ffi.cdef("""
    typedef struct {
        void* data;
        GoInt len;
        GoInt cap;
    } GoSlice;

    typedef struct {
        const char *data;
        GoInt len;
    } GoString;

    GoInt GetMessageFromFront();
    """)

    lib = ffi.dlopen("/media/imixiru/EE98F9C398F989FB/work/home-assist-core/homeassistant/components/moorgen_smart_panel/awesome.so")

    threading.Thread(target=MessageHandler, args=(lib, entity, config)).start()





