import torch
import time


if(torch.cuda.is_available()):
    print("CUDA can available")
else:
    print("CUDA cannot run")

deviceCpu = torch.device("cpu");

dimSize = 10000
a = torch.rand(dimSize,dimSize , device=deviceCpu)
print("a: ", a)
print("device: ", a.device)

b = torch.eye(dimSize,dimSize , device=deviceCpu)
print("b: " , b)

start_time = time.time_ns()
c = torch.matmul(a , b)
end_time = time.time_ns()
print(c)

print(f"deltaTime : {(end_time - start_time)/1000000} ms")



