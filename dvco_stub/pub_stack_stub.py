from dvco_stub.abstract_pub_stack import AbstractPubStack
from common.python.error import DopError
from common.python.threads import DopStopEvent

upy: bool
try:
    from typing import Callable, Tuple
    from threading import Lock 

    upy = False 

    
except ImportError:
    upy = True 
    import _thread
    Tuple = tuple


class PubStackStub(AbstractPubStack):
    def __init__(self):
        super().__init__()
        if upy:
            self._lock = _thread.allocate_lock()
            self._callback_lock = _thread.allocate_lock() 
        else: 
            self._lock = Lock()
            self._callback_lock = Lock()


    def init(self, pub_conf: dict):
        self._pub_conf = pub_conf


    def pump(self):
        return     
    

    def dopify(self, mess: bytes) -> Tuple[DopError, bytes]:
        self._on_dopified_message(mess.decode("UTF-8"))
        return DopError(), mess

    def _on_dopified_message(self, mess):
        
        if self._pub_callback is not None:
            with self._callback_lock: 
                self._pub_callback(mess, self._pub_userdata)

    