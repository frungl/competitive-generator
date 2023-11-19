import os
import sys
import datetime
import configparser
import shutil
import timeit

from utils import config as cfg
from utils.config import (
    TEMP_PATH,
    SAVE_TEST_PATH,
    INPUT_FILE,
    SMART_ANS,
    STUPID_ANS,
    RESULT_FILE,
    ERROR_FILE,
    SMART_EXE_FILE,
    STUPID_EXE_FILE,
    CHECKER_EXE_FILE,
    GENERATOR_EXE_FILE
)

SMART = ''
STUPID = ''
CHECKER = ''
GENERATOR = ''
CPP_STANDARD = ''
COUNT = 0
STEP = 0


def error(message):
    print(message, file=sys.stderr)
    sys.exit(1)


def validate_path(path):
    if len(path) == 0 or not os.path.exists(path):
        error(f'Path does not exist: {path}')


def validate_file(file_path):
    validate_path(file_path)
    for language in cfg.languages:
        if file_path.endswith(language):
            return
    error(f'Unsupported language: {file_path}')


def read_config(config_file):
    global SMART, STUPID, CHECKER, GENERATOR, CPP_STANDARD, COUNT, STEP
    config = configparser.ConfigParser()
    config.read(config_file)
    for key in config['STRESS']:
        value = config['STRESS'][key]
        match key:
            case 'smart':
                SMART = value
            case 'stupid':
                STUPID = value
            case 'checker':
                if value in cfg.checkers:
                    CHECKER = f'../utils/checkers/{value}'
                else:
                    CHECKER = value
            case 'generator':
                GENERATOR = value
            case 'cpp_standard':
                CPP_STANDARD = value
            case 'count':
                COUNT = int(value)
            case 'step':
                STEP = int(value)

    validate_file(GENERATOR)
    validate_file(SMART)
    validate_file(STUPID)
    validate_file(CHECKER)

    if CPP_STANDARD not in cfg.cpp_standards:
        error(f'Unsupported c++ standard: {CPP_STANDARD}')


def need_update(file_path, exe_path):
    file_time = os.path.getmtime(file_path)
    exe_time = os.path.getmtime(exe_path)
    return file_time > exe_time


def do_cpp(cpp_std, file_path, exe_path):
    os.system(f'g++ -std=c++{cpp_std} -O2 {file_path} -o {exe_path}')


def prepare_cpp(cpp_std, file_path, exe_path):
    exe_path = TEMP_PATH + exe_path
    validate_path(file_path)

    if not os.path.exists(exe_path):
        print(f'Compile : {file_path}')
        do_cpp(cpp_std, file_path, exe_path)
        return

    if need_update(file_path, exe_path):
        print(f'Recompile : {file_path}')
        do_cpp(cpp_std, file_path, exe_path)


def do_python(file_path, exe_path):
    shutil.copyfile(file_path, exe_path)


def prepare_python(file_path, exe_path):
    exe_path = TEMP_PATH + exe_path + '.py'
    validate_path(file_path)

    if not os.path.exists(exe_path):
        print(f'Copy : {file_path}')
        shutil.copyfile(file_path, exe_path)
        return

    if need_update(file_path, exe_path):
        print(f'Recopy : {file_path}')
        shutil.copyfile(file_path, exe_path)


def prepare_runnable(file_path, exe_path):
    if file_path.endswith('.cpp'):
        prepare_cpp(CPP_STANDARD, file_path, exe_path)
    elif file_path.endswith('.py'):
        prepare_python(file_path, exe_path)


def prepare(config_file):
    if not os.path.exists(TEMP_PATH):
        os.mkdir(TEMP_PATH)
    if not os.path.exists(SAVE_TEST_PATH):
        os.mkdir(SAVE_TEST_PATH)
    read_config(config_file)

    prepare_runnable(CHECKER, 'checker')
    prepare_runnable(GENERATOR, 'generator')
    prepare_runnable(SMART, 'smart')
    prepare_runnable(STUPID, 'stupid')


def get_executable(exe_path):
    return exe_path


def get_interpretable(inter_path, exe_path):
    return f'{inter_path} {exe_path}'


def run(file_path, exe_path, args='', input_file='', output_file='', error_file=''):
    command = ''
    if file_path.endswith('.cpp'):
        command += get_executable(exe_path)
    elif file_path.endswith('.py'):
        command += get_interpretable(file_path, exe_path)
    if len(args) > 0:
        command += ' ' + args
    if len(input_file) > 0:
        command += f' < {input_file}'
    if len(output_file) > 0:
        command += f' > {output_file}'
    if len(error_file) > 0:
        command += f' 2> {error_file}'
    time = timeit.timeit(lambda: os.system(command), number=1)
    return time


def gen_input(file_name):
    return run(
        GENERATOR,
        GENERATOR_EXE_FILE,
        output_file=file_name
    )


def run_smart(file_name, smart_ans):
    return run(
        SMART,
        SMART_EXE_FILE,
        input_file=file_name,
        output_file=smart_ans
    )


def run_stupid(file_name, stupid_ans):
    return run(
        STUPID,
        STUPID_EXE_FILE,
        input_file=file_name,
        output_file=stupid_ans
    )


def run_checker(smart_ans, stupid_ans, result_file, error_file):
    return run(
        CHECKER,
        CHECKER_EXE_FILE,
        args=f'{INPUT_FILE} {stupid_ans} {smart_ans}',
        output_file=result_file,
        error_file=error_file
    )


divider_width = 100
global_divider = '=' * divider_width
local_divider = '-' * divider_width


def to_ms(time):
    return f'{round(time * 1000)} ms'


def log(buffer, line, end=''):
    print(line, end=end)
    buffer.append(line + end)


def log_block(buffer, name, file_path, time):
    log(buffer, name, '\n')
    log(buffer, open(file_path).read())
    log(buffer, f'\nTime: {to_ms(time)}', '\n')


def stress():
    step_counter = 0
    print('Start stressing')
    print(global_divider)
    for i in range(1, COUNT + 1):
        step_counter += 1
        if step_counter == STEP:
            print('Running test', i)
            step_counter = 0

        gen_time = gen_input(INPUT_FILE)
        smart_time = run_smart(INPUT_FILE, SMART_ANS)
        stupid_time = run_stupid(INPUT_FILE, STUPID_ANS)
        checker_time = run_checker(SMART_ANS, STUPID_ANS, RESULT_FILE, ERROR_FILE)

        result = open(RESULT_FILE).read().strip()

        if result == 'ERROR':
            error('Checker error:\n' + open(ERROR_FILE).read())

        if result == 'WA':
            file_name = datetime.datetime.now().strftime('%Y-%m-%d %H\'%M\'%S') + '.txt'
            buffer = []

            log(buffer, global_divider, '\n')
            log_block(buffer, 'Checker message:', ERROR_FILE, checker_time)
            log(buffer, local_divider, '\n')
            log_block(buffer, 'Input:', INPUT_FILE, gen_time)
            log(buffer, local_divider, '\n')
            log_block(buffer, 'Stupid answer:', STUPID_ANS, stupid_time)
            log(buffer, local_divider, '\n')
            log_block(buffer, 'Smart answer:', SMART_ANS, smart_time)
            log(buffer, global_divider, '\n')

            open(f'{SAVE_TEST_PATH}/{file_name}', 'w').write(''.join(buffer))
            sys.exit()
    print('All tests passed')


def main(config_file):
    prepare(config_file)
    stress()
