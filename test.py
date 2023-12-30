

def test1():
    global str
    str = "2222"
    print(f" str= {str}")

def test2():
    global str
    str = "333"
    print(f" str= {str}")

if __name__ == "__main__" :
    print("run")
    test1()
    test2()
    print(f" str= {str}")