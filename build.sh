#!/usr/bin/env bash
set -e

# 默认构建类型
BUILD_TYPE=${1:-Debug}   # 参数：Debug 或 Release
ACTION=${2:-build}       # 参数：build / clean

# 构建目录
BUILD_DIR=build/${BUILD_TYPE,,}  # build/debug 或 build/release

# 清理构建目录
if [ "$ACTION" == "clean" ]; then
    echo "Cleaning $BUILD_DIR ..."
    rm -rf "$BUILD_DIR"
    echo "Done."
    exit 0
fi

# 生成构建系统
mkdir -p "$BUILD_DIR"
cmake -B"$BUILD_DIR" -H. -DCMAKE_BUILD_TYPE="$BUILD_TYPE"

# 编译所有
cmake --build "$BUILD_DIR" -j$(nproc)

echo ""
echo "Build finished!"
echo "App executables   -> $BUILD_DIR/bin/app/"
echo "Test executables  -> $BUILD_DIR/bin/test/"
echo "Libraries/Python  -> $BUILD_DIR/lib/"

# Debug 增量编译（默认）./build.sh 
# ./build.sh Release
# ./build.sh Debug clean
# ./build.sh Release clean


