import torch

if __name__ == "__main__":
    if torch.cuda.is_available():
        print("GPU is available")
    else:
        print("No GPU found")