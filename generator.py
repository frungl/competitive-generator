import os
import sys
import re
import shutil

real_path = os.path.dirname(__file__) + '/'
default_smart = []
default_stupid = []
default_generator = []
default_checker = []
default_stress = []
default_input = []
default_config = []
default_problem_cmake = []


def init():
    global \
        default_smart, default_stupid, default_generator, \
        default_checker, default_stress, default_input, \
        default_config, default_problem_cmake

    default_smart = open(real_path + 'example/smart.cpp', 'r').readlines()
    default_stupid = open(real_path + 'example/stupid.cpp', 'r').readlines()
    default_generator = open(real_path + 'example/generator.cpp', 'r').readlines()
    default_checker = open(real_path + 'example/checker.cpp', 'r').readlines()
    default_stress = open(real_path + 'example/stress.py', 'r').readlines()
    default_input = open(real_path + 'example/input.in', 'r').readlines()
    default_config = open(real_path + 'example/config.ini', 'r').readlines()
    default_problem_cmake = open(real_path + 'example/problemCMakeLists.txt', 'r').readlines()


def add_to_cmake(problem_name):
    cmake = open('CMakeLists.txt', 'a')
    cmake.write(f'add_subdirectory({problem_name})\n')
    cmake.close()


def delete_from_cmake(problem_name):
    cmake = open('CMakeLists.txt', 'r')
    lines = cmake.readlines()
    cmake.close()
    pattern = f'add_subdirectory({problem_name}'
    cmake = open('CMakeLists.txt', 'w')
    for line in lines:
        if not line.startswith(pattern):
            cmake.write(line)
    cmake.close()


def init_problem(problem_name):
    now_smart = default_smart.copy()
    now_stupid = default_stupid.copy()
    now_generator = default_generator.copy()
    now_checker = default_checker.copy()
    now_stress = default_stress.copy()
    now_input = default_input.copy()
    now_config = default_config.copy()
    now_problem_cmake = default_problem_cmake.copy()
    os.mkdir(problem_name)
    now_smart = [line.replace('PROBLEM_NAME', problem_name) for line in now_smart]
    now_stupid = [line.replace('PROBLEM_NAME', problem_name) for line in now_stupid]
    now_stress = [line.replace('PROBLEM_NAME', problem_name) for line in now_stress]
    now_config = [line.replace('PROBLEM_NAME', problem_name) for line in now_config]
    now_problem_cmake = [line.replace('PROBLEM_NAME', problem_name) for line in now_problem_cmake]
    open(fr'{problem_name}/{problem_name}.cpp', 'w').writelines(now_smart)
    open(fr'{problem_name}/{problem_name}-stupid.cpp', 'w').writelines(now_stupid)
    open(fr'{problem_name}/{problem_name}-generator.cpp', 'w').writelines(now_generator)
    open(fr'{problem_name}/{problem_name}-checker.cpp', 'w').writelines(now_checker)
    open(fr'{problem_name}/{problem_name}-stress.py', 'w').writelines(now_stress)
    open(fr'{problem_name}/{problem_name}.in', 'w').writelines(now_input)
    open(fr'{problem_name}/{problem_name}-config.ini', 'w').writelines(now_config)
    open(fr'{problem_name}/CMakeLists.txt', 'w').writelines(now_problem_cmake)


ban_names = ['cmake-build-debug', 'venv', 'utils', 'CMakeLists.txt']


def create_problem(problem_name, reset=False):
    if problem_name in ban_names:
        print(f'Problem name \'{problem_name}\' is banned')
        exit(-1)

    if os.path.exists(problem_name):
        print(f'Problem \'{problem_name}\' already exist')
        exit(-1)

    init()
    init_problem(problem_name)
    add_to_cmake(problem_name)
    if not reset:
        print(f'Problem \'{problem_name}\' created successfully!')


def delete_problem(problem_name, reset=False):
    if problem_name in ban_names:
        print(f'Problem name \'{problem_name}\' is banned')
        exit(-1)

    if not os.path.exists(problem_name):
        print(f'Problem \'{problem_name}\' does not exist')
        exit(-1)

    sure = input(f'Are you sure you want to {"reset" if reset else "delete"} \'{problem_name}\'? (y/n) ')
    if sure != 'y':
        exit(0)
    shutil.rmtree(problem_name)
    delete_from_cmake(problem_name)
    if not reset:
        print(f'Problem \'{problem_name}\' deleted successfully!')


def reset_problem(problem_name):
    delete_problem(problem_name, reset=True)
    create_problem(problem_name, reset=True)
    print(f'Problem \'{problem_name}\' reset successfully!')


def gen_project(project_name, max_name):
    if os.path.exists('utils'):
        print('Project already exist')
        exit(-1)

    if not re.fullmatch(f'^[a-z]|{chr(0)}', max_name):
        print("Not a-z symbol")
        exit(-1)
    if os.path.exists('main.cpp'):
        os.remove('main.cpp')
    init()
    default_cmake = open(real_path + 'defaultCMakeLists.txt', 'r').readlines()
    default_cmake = [line.replace('PROJECT_NAME', project_name) for line in default_cmake]
    open('CMakeLists.txt', 'w').writelines(default_cmake)
    create_problem('main')
    name = 'a'
    while name <= max_name:
        create_problem(name)
        name = chr(ord(name) + 1)
    shutil.copytree(real_path + 'utils', 'utils')
    print(f'Project {project_name} created successfully!')


def main():
    flag = sys.argv[1]
    if flag == '-r':
        reset_problem(sys.argv[2])
    elif flag == '-d':
        delete_problem(sys.argv[2])
    elif flag == '-c':
        create_problem(sys.argv[2])
    elif flag == '-g':
        gen_project(sys.argv[2], (sys.argv[3] if len(sys.argv) > 3 else chr(0)))


if __name__ == "__main__":
    main()
