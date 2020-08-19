#!/usr/bin/env bash
#之前的文件坏了.所以是.2
wget https://www.rarlab.com/rar/rarlinux-x64-5.5.0.tar.gz
tar zxvf rarlinux-x64-5.5.0.tar.gz
cd rar
make
make install
cd ..
pip install -r requirements.txt
echo 成功安装环境


