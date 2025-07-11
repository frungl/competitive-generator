import os
import sys
import re
import shutil
from getkey import getkey, keys

real_path = os.path.dirname(__file__) + '/'
default_debug = []
default_smart = []
default_stupid = []
default_grader = []
default_generator = []
default_checker = []
default_stress = []
default_input = []
default_config = []
default_problem_cmake = []


def init(theme):
    global \
        default_debug, default_smart, default_stupid, default_grader, \
        default_generator, default_checker, default_stress, \
        default_input, default_config, default_problem_cmake

    if os.path.exists(real_path + fr'themes/{theme}') is False:
        print(f'Theme \'{theme}\' does not exist')
        exit(-1)

    default_debug = open(real_path + fr'themes/{theme}/debug.h', 'r').readlines()
    default_smart = open(real_path + fr'themes/{theme}/smart.cpp', 'r').readlines()
    if theme == 'grader':
        default_grader = open(real_path + fr'themes/{theme}/main.cpp', 'r').readlines()
    default_stupid = open(real_path + fr'themes/{theme}/stupid.cpp', 'r').readlines()
    default_generator = open(real_path + fr'themes/{theme}/generator.cpp', 'r').readlines()
    default_checker = open(real_path + fr'themes/{theme}/checker.cpp', 'r').readlines()
    default_stress = open(real_path + fr'themes/{theme}/stress.py', 'r').readlines()
    default_input = open(real_path + fr'themes/{theme}/input.in', 'r').readlines()
    default_config = open(real_path + fr'themes/{theme}/config.ini', 'r').readlines()
    default_problem_cmake = open(real_path + fr'themes/{theme}/problemCMakeLists.txt', 'r').readlines()


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
    now_grader = default_grader.copy()
    now_generator = default_generator.copy()
    now_checker = default_checker.copy()
    now_stress = default_stress.copy()
    now_input = default_input.copy()
    now_config = default_config.copy()
    now_problem_cmake = default_problem_cmake.copy()
    os.mkdir(problem_name)
    now_smart = [line.replace('PROBLEM_NAME', problem_name) for line in now_smart]
    now_stupid = [line.replace('PROBLEM_NAME', problem_name) for line in now_stupid]
    now_grader = [line.replace('PROBLEM_NAME', problem_name) for line in now_grader]
    now_stress = [line.replace('PROBLEM_NAME', problem_name) for line in now_stress]
    now_config = [line.replace('PROBLEM_NAME', problem_name) for line in now_config]
    now_problem_cmake = [line.replace('PROBLEM_NAME', problem_name) for line in now_problem_cmake]
    open(fr'{problem_name}/debug.h', 'w').writelines(default_debug)
    open(fr'{problem_name}/{problem_name}.cpp', 'w').writelines(now_smart)
    open(fr'{problem_name}/{problem_name}-stupid.cpp', 'w').writelines(now_stupid)
    if now_grader:
        open(fr'{problem_name}/{problem_name}-main.cpp', 'w').writelines(now_grader)
    open(fr'{problem_name}/{problem_name}-generator.cpp', 'w').writelines(now_generator)
    open(fr'{problem_name}/{problem_name}-checker.cpp', 'w').writelines(now_checker)
    open(fr'{problem_name}/{problem_name}-stress.py', 'w').writelines(now_stress)
    open(fr'{problem_name}/{problem_name}.in', 'w').writelines(now_input)
    open(fr'{problem_name}/{problem_name}-config.ini', 'w').writelines(now_config)
    open(fr'{problem_name}/CMakeLists.txt', 'w').writelines(now_problem_cmake)


ban_names = ['cmake-build-debug', '.idea', '.venv', 'utils', 'CMakeLists.txt']


def create_problem(problem_name, reset=False, theme='default'):
    if problem_name in ban_names:
        print(f'Problem name \'{problem_name}\' is banned')
        exit(-1)

    if os.path.exists(problem_name):
        print(f'Problem \'{problem_name}\' already exist')
        exit(-1)

    init(theme)
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

    print(f'Are you sure you want to {"reset" if reset else "delete"} \'{problem_name}\'? (y/n) ')
    sure = getkey()
    if sure != 'y' and sure != keys.ENTER:
        exit(0)
    shutil.rmtree(problem_name)
    delete_from_cmake(problem_name)
    if not reset:
        print(f'Problem \'{problem_name}\' deleted successfully!')


def reset_problem(problem_name, theme='default'):
    delete_problem(problem_name, reset=True)
    create_problem(problem_name, reset=True, theme=theme)
    print(f'Problem \'{problem_name}\' reset successfully!')


def gen_project(project_name, max_name, theme='default'):
    if os.path.exists('utils'):
        print('Project already exist')
        exit(-1)

    if re.fullmatch(r'\d+', max_name) and 0 <= int(max_name) <= 26:
        match max_name:
            case '0':
                max_name = chr(0)
            case _:
                max_name = chr(ord('a') + int(max_name) - 1)

    if not re.fullmatch(rf'^[a-z]|{chr(0)}', max_name):
        print("Not a-z symbol or 0-26 number")
        exit(-1)
    if os.path.exists('main.cpp'):
        os.remove('main.cpp')
    init(theme)
    default_cmake = open(real_path + 'themes/defaultCMakeLists.txt', 'r').readlines()
    default_cmake = [line.replace('PROJECT_NAME', project_name) for line in default_cmake]
    open('CMakeLists.txt', 'w').writelines(default_cmake)
    create_problem('main', theme=theme)
    name = 'a'
    while name <= max_name:
        create_problem(name, theme=theme)
        name = chr(ord(name) + 1)
    shutil.copytree(real_path + 'utils', 'utils')
    print(f'Project {project_name} created successfully!')


def main():
    theme = 'default'
    pos = 1
    flag = sys.argv[pos]
    if flag == '-t' or flag == '--theme':
        theme = sys.argv[pos + 1]
        pos += 2
    flag = sys.argv[pos]
    if flag == '-r' or flag == '--reset':
        reset_problem(sys.argv[pos + 1], theme=theme)
        pos += 2
    elif flag == '-d' or flag == '--delete':
        delete_problem(sys.argv[pos + 1])
        pos += 2
    elif flag == '-c' or flag == '--create':
        create_problem(sys.argv[pos + 1], theme=theme)
        pos += 2
    elif flag == '-g' or flag == '--gen':
        gen_project(sys.argv[pos + 1], sys.argv[pos + 2], theme=theme)
        pos += 3
    else:
        print('Unknown flag')
        exit(-1)


if __name__ == "__main__":
    main()
