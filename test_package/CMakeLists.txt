project(test_package)
cmake_minimum_required(VERSION 2.8.11)

set(CMAKE_VERBOSE_MAKEFILE TRUE)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

file(GLOB SOURCE_FILES *.c)
set(CMAKE_VERBOSE_MAKEFILE ON)

add_executable(${CMAKE_PROJECT_NAME} ${SOURCE_FILES})

IF(WIN32)
	set(OS_LINK_LIBS crypt32 ws2_32 secur32 advapi32 ncrypt winhttp)
ENDIF(WIN32)

target_link_libraries(${CMAKE_PROJECT_NAME} ${CONAN_LIBS} ${OS_LINK_LIBS} )


