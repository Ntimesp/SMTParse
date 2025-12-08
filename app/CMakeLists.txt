file(GLOB APP_SOURCES CONFIGURE_DEPENDS *.cpp *.cc)

foreach(APP_SRC IN LISTS APP_SOURCES)
    get_filename_component(APP_NAME ${APP_SRC} NAME_WE)

    add_executable(${APP_NAME} ${APP_SRC})

    target_link_libraries(${APP_NAME} PRIVATE ${SMTParse_LIB} clpoly_external)

    target_include_directories(${APP_NAME} PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}
    )

    target_compile_options(${APP_NAME} PRIVATE
        $<$<CONFIG:Debug>:-O0 -g -DDEBUG>
        $<$<CONFIG:Release>:-O3 -DNDEBUG -march=native>
    )

    set_target_properties(${APP_NAME} PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin/app
    )
endforeach()