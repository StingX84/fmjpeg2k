cmake_minimum_required(VERSION 3.12)
project(test_package LANGUAGES CXX)

find_package(fmjpeg2k REQUIRED)

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} PRIVATE fmjpeg2k::fmjpeg2k)
target_compile_features(${PROJECT_NAME} PRIVATE cxx_std_17)
