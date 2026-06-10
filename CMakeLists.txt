cmake_minimum_required(VERSION 3.16)
project(SMTParse LANGUAGES CXX)

# 构建类型 -DCMAKE_BUILD_TYPE=Debug/Release, 默认 -DCMAKE_BUILD_TYPE=Debug
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Debug CACHE STRING "Build type" FORCE)
endif()

# 设置 C++ 标准
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 生成位置无关代码，因为可能需要编译成动态库
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# 输出目录
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# 核心库名称
set(SMTParse_LIB smtparse)

# CLPoly 外部库, 需要自己编译 clpoly
set(CLPoly_INCLUDE_DIR ${CMAKE_SOURCE_DIR}/CLPoly)
set(CLPoly_LIB ${CMAKE_SOURCE_DIR}/CLPoly/lib/clpoly/libclpoly.a)

add_library(clpoly_external STATIC IMPORTED)
set_target_properties(clpoly_external PROPERTIES
    IMPORTED_LOCATION "${CLPoly_LIB}"
    INTERFACE_INCLUDE_DIRECTORIES "${CLPoly_INCLUDE_DIR}"
    INTERFACE_LINK_LIBRARIES "gmpxx;gmp"
)

# 子目录
add_subdirectory(src)
add_subdirectory(app)
add_subdirectory(python)
add_subdirectory(test)
