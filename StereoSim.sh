#!/bin/bash
# StereiSim.sh

export isaac_sim_package_path="/home/goodmansun/isaacsim/_build/linux-x86_64/release"
export main_py_path="/home/goodmansun/StereoSIm/src/main.py"
$isaac_sim_package_path/python.sh "$@"