import torch

if(torch.cuda.is_available()):
    print("CUDA can available")
else:
    print("CUDA cannot run")

deviceCpu = torch.device("cpu");

dimSize = 100
a = torch.rand(dimSize,dimSize , device=deviceCpu)
print("a: ", a)
print("device: ", a.device)

b = torch.eye(dimSize,dimSize , device=deviceCpu)
print("b: " , b)

c = torch.matmul(a , b)
print(c)



