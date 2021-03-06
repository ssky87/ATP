import signal
import time
from atp.errcode import ER_TIMEOUT
from atp.logger import L

def signalAlarmHandler(signum, frame):
    raise Exception("Catch SigAlarm")

signal.signal(signal.SIGALRM, signalAlarmHandler)
    
def timeLimitExecute(timeout):
    def decorator(func):
        def realFunc(*args, **kwargs):
            signal.alarm(timeout)
            try:
                ret = func(*args, **kwargs)
                signal.alarm(0)
            except Exception as e:
                L.error(e)
                L.error("execute timeout")
                return ER_TIMEOUT
            
            return ret
        return realFunc

    return decorator
 
 
if __name__ == '__main__':
    class MyTest:
        def __init__(self):
            pass
        @timeLimitExecute(10)
        def longTimeCall(self, sleepTime):
            time.sleep(sleepTime)
            
        def testFunc(self):
            timeLimitExecute(self.longTimeCall, 10, 20)
            
    testCase = MyTest()
    #testCase.testFunc()
    testCase.longTimeCall(2)        
