# Python Boost
execute_process(
    COMMAND python3 -c "import sys; print(f'{sys.version_info[0]}{sys.version_info[1]}')"
    OUTPUT_VARIABLE PY_ABI
    OUTPUT_STRIP_TRAILING_WHITESPACE
)

find_package(Python3 COMPONENTS Development REQUIRED)
find_package(Boost REQUIRED COMPONENTS python${PY_ABI})

# Python 扩展模块
# 一般用 MODULE 而不是 SHARED
add_library(NRA_op MODULE ${CMAKE_CURRENT_SOURCE_DIR}/NRA_op.cc)

# include
target_include_directories(NRA_op PRIVATE
    ${Python3_INCLUDE_DIRS}
    ${Boost_INCLUDE_DIRS}
)

# 链接 smtparse 和 Boost.Python
target_link_libraries(NRA_op PRIVATE
    ${SMTParse_LIB}
    ${Boost_LIBRARIES}
)

target_compile_options(NRA_op PRIVATE
    $<$<CONFIG:Debug>:-O0 -g -DDEBUG>
    $<$<CONFIG:Release>:-O3 -DNDEBUG -march=native>
)

# 输出目录, 去掉 lib 前缀
set_target_properties(NRA_op PROPERTIES
    PREFIX ""
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib
)