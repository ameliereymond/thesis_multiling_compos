import torch
import os

if __name__ == "__main__":

    if "CUDA_VISIBLE_DEVICES" in os.environ:
        visible = os.environ["CUDA_VISIBLE_DEVICES"]
        print(f"CUDA_VISIBLE_DEVICES is set to '{visible}'")
    else:
        print("CUDA_VISIBLE_DEVICES not set")

    if torch.cuda.is_available():
        print("GPU available!")
        gpu_count = torch.cuda.device_count()
        print(f"Found {gpu_count} GPUs")
        for i in range(gpu_count):
            print(torch.cuda.get_device_properties(i))
    else:
        print("No GPU found")