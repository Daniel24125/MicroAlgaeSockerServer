class TestClass: 
    
    def __init__(self):
        self.test = []

    def add_number(self, num): 
        self.test.append(num)

    def get_test(self): 
        return self.test

if __name__ == "__main__": 
    # TestClass.add_number(TestClass,10)
    # TestClass.add_number(TestClass,2)
    # TestClass.add_number(TestClass,4)
    # TestClass.add_number(TestClass,2)
    # print(TestClass.test)
    x = TestClass()
    print(x.test)
    y = TestClass()
    y.add_number(1000)
    print(x.get_test(), y.get_test())
