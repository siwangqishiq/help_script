import torch

print("Hello Pytorch")

matOne = torch.ones(3,3)
print(matOne)
print(matOne.type())

matZeros = torch.zeros_like(matOne,device=torch.device("cuda"))
print(matZeros)

print(torch.__version__)

