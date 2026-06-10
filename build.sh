#!/usr/bin/env bash
set -e

BUILD_TYPE="Debug"
ACTION="build"
TARGET=""
BUILD_DIR=""

show_help() {
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  -D, --debug            Use Debug build type"
    echo "  -R, --release          Use Release build type"
    echo "  -b, --build[=TARGET]   Build (default), optionally specify target"
    echo "  -t, --target TARGET    Build only a specific target"
    echo "  -c, --clean            Clean build directory"
    echo "  -h, --help             Show help"
    echo ""
    echo "Examples:"
    echo "  $0 --debug --build                      # Debug build (all)"
    echo "  $0 --release -b -t app                  # Release, build only target 'app'"
    echo "  $0 -D -c                                 # Clean Debug directory"
    echo "  $0 -R --build=solver                     # Only build target solver"
    echo ""
}

# ---- Parse arguments ----
while [[ $# -gt 0 ]]; do
    case "$1" in
        -D|--debug)
            BUILD_TYPE="Debug"
            shift
            ;;
        -R|--release)
            BUILD_TYPE="Release"
            shift
            ;;
        -b|--build)
            ACTION="build"
            # optional: --build=target
            if [[ "$1" == *=* ]]; then
                TARGET="${1#*=}"
            fi
            shift
            ;;
        -t|--target)
            TARGET="$2"
            ACTION="build"
            shift 2
            ;;
        -c|--clean)
            ACTION="clean"
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# lowercase build directory
BUILD_DIR="build/${BUILD_TYPE,,}"

# ---- Perform actions ----

if [[ "$ACTION" == "clean" ]]; then
    echo "Cleaning $BUILD_DIR ..."
    rm -rf "$BUILD_DIR"
    echo "Done."
    exit 0
fi

mkdir -p "$BUILD_DIR"

echo "Config:   $BUILD_TYPE"
echo "Action:   $ACTION"
echo "Target:   ${TARGET:-<all>}"
echo "Dir:      $BUILD_DIR"
echo ""

# CMake configure
cmake -B"$BUILD_DIR" -S. -DCMAKE_BUILD_TYPE="$BUILD_TYPE"

# Build logic
if [[ -z "$TARGET" ]]; then
    cmake --build "$BUILD_DIR" -j"$(nproc)"
else
    cmake --build "$BUILD_DIR" --target "$TARGET" -j"$(nproc)"
fi

echo ""
echo "Build finished."
echo "App executables   -> $BUILD_DIR/bin/app/"
echo "Test executables  -> $BUILD_DIR/bin/test/"
