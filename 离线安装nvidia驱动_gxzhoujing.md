## 添加离线源

```sh
cd ~/ai/offline_gcc
echo "deb file:///home/gx/ai/offline_gcc/" | sudo tee /etc/apt/offline-repo.list
# [sudo] password for gx:
# deb file:///home/gx/ai/offline_gcc  archive/

cat /etc/apt/offline-repo.list
# deb file:///home/gx/ai/offline_gcc/
```

## 更新源

```sh
sudo apt-get update
```

## 安装所有下载的软件包

```sh
cd /home/gx/ai/offline_gcc/
sudo dpkg -i *.deb
```

查看安装结果

```sh
gcc --version
g++ --version
make --version
 
# gcc (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0
# Copyright (C) 2019 Free Software Foundation, Inc.
# This is free software; see the source for copying conditions.  
# There is NO warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
```

## 安装驱动



```sh
cd /home/gx/ai

sudo chmod +x NVIDIA-Linux-x86_64-535.54.03.run
sudo ./NVIDIA-Linux-x86_64-535.54.03.run
```



## 报错： 

the nouveau kernel driver is currently in use by your system.....

## 解决办法：

禁用 nouveau 

```shell
vim /etc/modprobe.d/blacklist-nouveau.conf
写入一下内容

blacklist nouveau
options nouveau modeset=0
```

更新使其生效

```sh
sudo update-initramfs -u
```

重启,**最好重启下**

```
sudo reboot
```

# 重新安装驱动

```sh
cd /home/gx/ai
sudo ./NVIDIA-Linux-x86_64-535.54.03.run
```
1. 一路默认确认
2. 查看安装结果：

```sh
gx@gx:~/ai$ nvidia-smi

Fri Oct 18 09:09:04 2024       
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 525.147.05   Driver Version: 525.147.05   CUDA Version: 12.0     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  NVIDIA GeForce ...  Off  | 00000000:03:00.0  On |                  N/A |
| 31%   29C    P8    19W / 250W |   5427MiB / 22528MiB |     11%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
                                                                               
+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
+-----------------------------------------------------------------------------+
```

# 离线安装nvidia-docker
1. 先确认是否安装docker
2. 下载安装包
```shell
https://mirror.cs.uchicago.edu/nvidia-docker/libnvidia-container/stable/ubuntu20.04/amd64/
```
3. 离线安装
```shell
sudo dpkg -i libnvidia-container1_1.12.0-1_amd64.deb
sudo dpkg -i libnvidia-container-tools_1.12.0-1_amd64.deb
sudo dpkg -i nvidia-container-runtime_3.12.0-1_all.deb
sudo dpkg -i nvidia-container-toolkit-base_1.12.0-1_amd64.deb
sudo dpkg -i nvidia-container-toolkit_1.12.0-1_amd64.deb
sudo dpkg -i nvidia-docker2_2.12.0-1_all.deb
```
4.测试结果
```shell
docker run --rm --gpus=all portia-app nvidia-smi

# 以下输出测试
Fri Oct 18 09:09:04 2024       
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 525.147.05   Driver Version: 525.147.05   CUDA Version: 12.0     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  NVIDIA GeForce ...  Off  | 00000000:03:00.0  On |                  N/A |
| 31%   29C    P8    19W / 250W |   5427MiB / 22528MiB |     11%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
                                                                               
+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
+-----------------------------------------------------------------------------+

```
