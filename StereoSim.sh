#!/bin/bash
# StereoSim.sh

# 1. 获取当前脚本所在的绝对路径（即项目根目录）
# 无论你是在根目录运行 ./StereoSim.sh 还是在其他目录运行 /path/to/StereoSim.sh，它都能正确解析
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

export isaac_sim_package_path="/home/goodmansun/isaacsim/_build/linux-x86_64/release"
# 2. 将 main_py_path 设置为基于项目根目录的相对路径
export main_py_path="$PROJECT_ROOT/main.py"

# 3. 启动前清空 output 文件夹
OUTPUT_DIR="$PROJECT_ROOT/output"
echo "Cleaning output directory at: $OUTPUT_DIR"
# 删除整个 output 文件夹并重新创建，这比直接 rm -rf output/* 更安全，能避免文件夹不存在或包含隐藏文件时的报错
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

# 4. 运行 Isaac Sim 的 Python 环境
# 修复：将 "$main_py_path" 作为第一个参数传给 python.sh，"$@" 接收你在命令行传入的其他附加参数
$isaac_sim_package_path/python.sh "$main_py_path" "$@"