
def add(x , y) :
    print(f"{x} + {y} = {x + y}")
    return x + y

def sub(x ,y):
    print(f"{x} - {y} = {x - y}")
    return x - y

def test_case1(x , y , acton):
    return acton(x, y)

def test_lambda():
    x = 3
    y = 4
    
    action = lambda x,y:x-y
    z = test_case1(x , y , sub)
    print("z = %d"%z)

test_lambda()

