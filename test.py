import random

def get_num(min,max): 
    return min + random.random()*(max-min)
if __name__ == "__main__": 
    num = get_num(1,10)
    print(num)

