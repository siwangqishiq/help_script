import torch
import time
import sys


if(torch.cuda.is_available()):
    print("CUDA can available")
else:
    print("CUDA cannot run")
    

print(f"input params size: {len(sys.argv)}")

param_len = len(sys.argv)

current_device = torch.device("cpu")

param_device = None
if(param_len > 1):
    param_device = sys.argv[1]
    current_device = param_device

param_mat_size = None
matrix_size = 100
if(param_len > 2):
    param_mat_size = int(sys.argv[2])
    matrix_size = param_mat_size

if(not (param_device is None)):
    print(f"param_device:{param_device}")

if(not (param_mat_size is None)):
    print(f"param_mat_size:{param_mat_size}")  

a = torch.rand(matrix_size,matrix_size , device=current_device)
print("a: ", a)
print("device: ", a.device)

b = torch.rand(matrix_size,matrix_size , device=current_device)
print("b: " , b)

start_time = time.time_ns()
c = torch.matmul(a , b)
end_time = time.time_ns()
print(c)

print(f"deltaTime : {(end_time - start_time)/1000000} ms")



