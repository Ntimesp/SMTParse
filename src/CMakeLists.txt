# src/CMakeLists.txt

# 自动收集 src 源文件
# GLOB_RECURSE 递归找子目录的文件
# CONFIGURE_DEPENDS 文件新增/删除是否自动触发重新配置
file(GLOB_RECURSE SRC_SOURCES CONFIGURE_DEPENDS
    ${CMAKE_CURRENT_SOURCE_DIR}/*.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/*.cc
    ${CMAKE_CURRENT_SOURCE_DIR}/*.c
)

# 核心静态库 smtparse
add_library(${SMTParse_LIB} STATIC ${SRC_SOURCES})

# include
# PUBLIC 所有链接 smtparse 的 target 也自动继承这个 include 路径
target_include_directories(${SMTParse_LIB} PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CLPoly_INCLUDE_DIR}
)

# 编译选项
target_compile_options(${SMTParse_LIB} PRIVATE
    $<$<CONFIG:Debug>:-O0 -g -DDEBUG>
    $<$<CONFIG:Release>:-O3 -DNDEBUG -march=native>
)

# 链接 CLPoly
target_link_libraries(${SMTParse_LIB} PUBLIC clpoly_external)