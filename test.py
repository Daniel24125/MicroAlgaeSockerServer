class Class1: 
    def method1(self): 
        print("This is method 1 from class 1")

    def method2(self): 
        print("This is method 2 from class 1")

class Class2(Class1): 
    def method1(self): 
        super().method1()
        self.method2()
        print("This is method 1 from class 2")


if __name__ == "__main__": 
    x = Class2()
    x.method1()
