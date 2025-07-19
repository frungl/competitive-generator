set(CMAKE_CXX_STANDARD 17)

add_executable(PROBLEM_NAME PROBLEM_NAME.cpp debug.h)
add_executable(PROBLEM_NAME-stupid PROBLEM_NAME-stupid.cpp debug.h)
target_compile_options(PROBLEM_NAME PRIVATE -DLOCAL)
target_compile_options(PROBLEM_NAME-stupid PRIVATE -DLOCAL)

add_executable(PROBLEM_NAME-generator PROBLEM_NAME-generator.cpp)
add_executable(PROBLEM_NAME-checker PROBLEM_NAME-checker.cpp)
