x = None


def fn(): 
    global x 
    x = 2
if __name__ == "__main__": 
    fn()
    print(x)

