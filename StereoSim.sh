#!/bin/bash
# StereoSim.sh

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

export isaac_sim_package_path="/home/goodmansun/isaacsim/_build/linux-x86_64/release"
export main_py_path="$PROJECT_ROOT/main.py"

OUTPUT_DIR="$PROJECT_ROOT/output"
echo "Cleaning output directory at: $OUTPUT_DIR"
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

$isaac_sim_package_path/python.sh "$main_py_path" "$@"