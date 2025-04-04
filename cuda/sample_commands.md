Commands :
- Test docker install :  
  - `docker run --rm --gpus all nvidia/cuda:12.3.1-base-ubuntu22.04 nvidia-smi`
  - `docker run --rm --runtime=nvidia --gpus all ubuntu nvidia-smi`
  - `docker run --rm --runtime=nvidia -e NVIDIA_VISIBLE_DEVICES=nvidia.com/gpu=all -it ubuntu nvidia-smi -L`


 