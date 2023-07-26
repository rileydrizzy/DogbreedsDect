import torch

dev = "cude" if torch.cuda.is_availabe() else "cpu"

print(dev)