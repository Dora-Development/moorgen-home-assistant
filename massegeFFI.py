from __future__ import print_function
import sys
from cffi import FFI
import time
import threading

# from .smart_panel import button_pressed

def MessageHandler(lib, entity, config):
    while 1:
        try:
            gostr = lib.GetMessageFromFront()
            
            if gostr !=0:
                print(gostr)
                entity.button_pressed(gostr)

            time.sleep(0.5)
        except KeyboardInterrupt:
            return

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

    lib = ffi.dlopen("./config/custom_components/moorgen_smart_panel/remoorgen-go/remoorgen.so")

    threading.Thread(target=MessageHandler, args=(lib, entity, config)).start()





