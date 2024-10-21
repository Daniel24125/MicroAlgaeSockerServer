from utils.utils import SetInterval



if __name__ == "__main__": 
    t = SetInterval(lambda: print("HELLO"), 1)
    t.start()
    import time 
    time.sleep(5)
    t.stop()
    time.sleep(2)
    t.start()

