project(test_package)
cmake_minimum_required(VERSION 2.8.11)

set(CMAKE_VERBOSE_MAKEFILE TRUE)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

file(GLOB SOURCE_FILES *.c)
set(CMAKE_VERBOSE_MAKEFILE ON)

add_executable(${CMAKE_PROJECT_NAME} ${SOURCE_FILES})
set_property(TARGET ${CMAKE_PROJECT_NAME} PROPERTY C_STANDARD 99)
target_link_libraries(${CMAKE_PROJECT_NAME} 
	crypt32 ws2_32 secur32 advapi32 ncrypt winhttp
	${CONAN_LIBS})

#IF(WIN32)
#    add_definitions(-D_CRT_SECURE_NO_WARNINGS)
#    add_definitions(-DGB_MEASURE_MEMORY_FOR_THIS -DGB_DEBUG_ALLOC)
#ENDIF(WIN32)

