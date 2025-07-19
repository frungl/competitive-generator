import os
import sys
import re
import shutil
from getkey import getkey, keys

from utils.config import DEFAULT_TEMPLATE

real_path = os.path.dirname(__file__) + '/'

default_files = []

def init(template):
    global default_files

    template_directory = real_path + fr'templates/{template}/'

    if not os.path.exists(template_directory):
        print(f'Template \'{template}\' does not exist')
        exit(-1)

    for file in os.listdir(template_directory):
        file_name = file
        file_content = open(template_directory + file, 'r').readlines()
        default_files.append((file_name, file_content))

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
    ignored_problem_name = ['CMakeLists.txt', 'debug.h']
    os.mkdir(problem_name)
    for file_name, file_content in default_files:
        current_content = file_content.copy()
        current_content = [line.replace('PROBLEM_NAME', problem_name) for line in current_content]
        current_name = file_name
        if file_name == 'smart.cpp':
            current_name = f'{problem_name}.cpp'
        elif file_name not in ignored_problem_name:
            current_name = f'{problem_name}-{file_name}'
        open(fr'{problem_name}/{current_name}', 'w').writelines(current_content)

ban_names = ['cmake-build-debug', '.idea', '.venv', 'utils', 'CMakeLists.txt']


def create_problem(problem_name, reset=False, template=DEFAULT_TEMPLATE):
    if problem_name in ban_names:
        print(f'Problem name \'{problem_name}\' is banned')
        exit(-1)

    if os.path.exists(problem_name):
        print(f'Problem \'{problem_name}\' already exist')
        exit(-1)

    init(template)
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


def reset_problem(problem_name, template=DEFAULT_TEMPLATE):
    delete_problem(problem_name, reset=True)
    create_problem(problem_name, reset=True, template=template)
    print(f'Problem \'{problem_name}\' reset successfully!')

def setup_utils():
    if os.path.exists('utils'):
        print('Utils already exist')
        exit(-1)
    shutil.copytree(real_path + 'utils', 'utils')

def update_utils():
    if not os.path.exists('utils'):
        print('Utils do not exist')
        exit(-1)
    shutil.rmtree('utils')
    setup_utils()
    print('Utils updated successfully!')

def gen_project(project_name, max_name, template=DEFAULT_TEMPLATE):
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
    init(template)
    main_cmake = open(real_path + 'templates/mainCMakeLists.txt', 'r').readlines()
    main_cmake = [line.replace('PROJECT_NAME', project_name) for line in main_cmake]
    open('CMakeLists.txt', 'w').writelines(main_cmake)
    create_problem('main', template=template)
    name = 'a'
    while name <= max_name:
        create_problem(name, template=template)
        name = chr(ord(name) + 1)
    setup_utils()
    print(f'Project {project_name} created successfully!')


def main():
    template = DEFAULT_TEMPLATE
    pos = 1
    flag = sys.argv[pos]
    if flag == '-t' or flag == '--template':
        template = sys.argv[pos + 1]
        pos += 2
    flag = sys.argv[pos]
    if flag == '-r' or flag == '--reset':
        reset_problem(sys.argv[pos + 1], template=template)
        pos += 2
    elif flag == '-d' or flag == '--delete':
        delete_problem(sys.argv[pos + 1])
        pos += 2
    elif flag == '-c' or flag == '--create':
        create_problem(sys.argv[pos + 1], template=template)
        pos += 2
    elif flag == '-g' or flag == '--gen':
        gen_project(sys.argv[pos + 1], sys.argv[pos + 2], template=template)
        pos += 3
    elif flag == '-u' or flag == '--update':
        update_utils()
        pos += 1
    else:
        print('Unknown flag')
        exit(-1)


if __name__ == "__main__":
    main()
