# test/CMakeLists.txt

# 遍历 test 目录下所有测试源文件
file(GLOB TEST_SOURCES CONFIGURE_DEPENDS *.cpp *.cc)

# 遍历每个测试源文件，生成对应可执行文件
foreach(TEST_SRC ${TEST_SOURCES})
    get_filename_component(TEST_NAME ${TEST_SRC} NAME_WE)

    add_executable(${TEST_NAME} ${TEST_SRC})

    # 链接 smtparse 静态库以及 CLPoly
    target_link_libraries(${TEST_NAME} PRIVATE ${SMTParse_LIB})

    # include 路径
    target_include_directories(${TEST_NAME} PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}
    )

    # 编译选项
    target_compile_options(${TEST_NAME} PRIVATE
        $<$<CONFIG:Debug>:-O0 -g -DDEBUG>
        $<$<CONFIG:Release>:-O3 -DNDEBUG -march=native>
    )

    set_target_properties(${TEST_NAME} PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin/test
    )
endforeach()

