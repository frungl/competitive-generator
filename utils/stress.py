import configparser
import datetime
import os
import shutil
import sys
import threading
import timeit
from collections.abc import generator
from multiprocessing import Value

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
GRADER = ''
CHECKER = ''
GENERATOR = ''
CPP_STANDARD = ''
THREADS = 0
COUNT = 0
STEP = 0

print_lock = threading.Lock()

def atomic_print(*args, **kwargs):
    with print_lock:
        print(*args, **kwargs)


def error(message):
    atomic_print(message, file=sys.stderr)
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
    global SMART, STUPID, GRADER, CHECKER, GENERATOR, CPP_STANDARD, THREADS, COUNT, STEP
    config = configparser.ConfigParser()
    config.read(config_file)
    for key in config['STRESS']:
        value = config['STRESS'][key]
        match key:
            case 'smart':
                SMART = value
            case 'stupid':
                STUPID = value
            case 'grader':
                GRADER = value
            case 'checker':
                if value in cfg.checkers:
                    CHECKER = f'../utils/checkers/{value}'
                else:
                    CHECKER = value
            case 'generator':
                GENERATOR = value
            case 'cpp_standard':
                CPP_STANDARD = value
            case 'threads':
                THREADS = int(value)
            case 'count':
                COUNT = int(value)
            case 'step':
                STEP = int(value)

    validate_file(GENERATOR)
    validate_file(SMART)
    if GRADER != '':
        validate_file(GRADER)
    validate_file(STUPID)
    validate_file(CHECKER)

    if CPP_STANDARD not in cfg.cpp_standards:
        error(f'Unsupported c++ standard: {CPP_STANDARD}')


def need_update(file_path, exe_path):
    file_time = os.path.getmtime(file_path)
    exe_time = os.path.getmtime(exe_path)
    return file_time > exe_time


def do_cpp(cpp_std, file_path, grader_path, exe_path):
    os.system(f'g++ -std=c++{cpp_std} -O2 {file_path} {grader_path} -o {exe_path}')


def prepare_cpp(cpp_std, file_path, grader_path, exe_path):
    exe_path = TEMP_PATH + exe_path
    validate_path(file_path)

    if not os.path.exists(exe_path):
        atomic_print(f'Compile : {file_path}')
        do_cpp(cpp_std, file_path, grader_path, exe_path)
        return

    if need_update(file_path, exe_path):
        atomic_print(f'Recompile : {file_path}')
        do_cpp(cpp_std, file_path, grader_path, exe_path)


def do_python(file_path, exe_path):
    shutil.copyfile(file_path, exe_path)


def prepare_python(file_path, exe_path):
    exe_path = TEMP_PATH + exe_path + '.py'
    validate_path(file_path)

    if not os.path.exists(exe_path):
        atomic_print(f'Copy : {file_path}')
        shutil.copyfile(file_path, exe_path)
        return

    if need_update(file_path, exe_path):
        atomic_print(f'Recopy : {file_path}')
        shutil.copyfile(file_path, exe_path)


def prepare_runnable(file_path, grader_path, exe_path):
    if file_path.endswith('.cpp'):
        prepare_cpp(CPP_STANDARD, file_path, grader_path, exe_path)
    elif file_path.endswith('.py'):
        prepare_python(file_path, exe_path)


def prepare(config_file):
    if not os.path.exists(TEMP_PATH):
        os.mkdir(TEMP_PATH)
    if not os.path.exists(SAVE_TEST_PATH):
        os.mkdir(SAVE_TEST_PATH)
    read_config(config_file)

    checker_runner = threading.Thread(target=prepare_runnable, args=(CHECKER, '', 'checker'))
    generator_runner = threading.Thread(target=prepare_runnable, args=(GENERATOR, '', 'generator'))
    smart_runner = threading.Thread(target=prepare_runnable, args=(SMART, GRADER, 'smart'))
    stupid_runner = threading.Thread(target=prepare_runnable, args=(STUPID, GRADER, 'stupid'))

    all_runners = [
        checker_runner,
        generator_runner,
        smart_runner,
        stupid_runner
    ]

    for runner in all_runners:
        if not runner.is_alive():
            runner.start()

    for runner in all_runners:
        if runner.is_alive():
            runner.join()

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


divider_width = min(shutil.get_terminal_size().columns, 60)
global_divider = '=' * divider_width
local_divider = '-' * divider_width


def to_ms(time):
    return f'{round(time * 1000)} ms'


def log(buffer, line, end=''):
    atomic_print(line, end=end)
    buffer.append(line + end)


def log_block(buffer, name, file_path, time):
    log(buffer, name, '\n')
    log(buffer, open(file_path).read())
    log(buffer, f'\nTime: {to_ms(time)}', '\n')


test_counter = Value('i', 1)
test_found = Value('b', False)

def stress_worker(worker_id):
    directory = f'{TEMP_PATH}worker_{worker_id}/'
    worker_input_file = f'{directory}{INPUT_FILE}'
    worker_smart_ans = f'{directory}{SMART_ANS}'
    worker_stupid_ans = f'{directory}{STUPID_ANS}'
    worker_result_file = f'{directory}{RESULT_FILE}'
    worker_error_file = f'{directory}{ERROR_FILE}'
    if not os.path.exists(directory):
        os.mkdir(directory)
    while True:
        if test_found.value:
            break
        with test_counter.get_lock():
            if test_counter.value > COUNT:
                break
            test_num = test_counter.value
            test_counter.value += 1

        if test_num % STEP == 0:
            atomic_print(f'Worker {worker_id} running test {test_num}')

        gen_time = gen_input(worker_input_file)
        smart_time = run_smart(worker_input_file, worker_smart_ans)
        stupid_time = run_stupid(worker_input_file, worker_stupid_ans)
        checker_time = run_checker(worker_smart_ans, worker_stupid_ans, worker_result_file, worker_error_file)

        result = open(worker_result_file).read().strip()

        if result == 'ERROR':
            with test_found.get_lock():
                if not test_found.value:
                    atomic_print(f'Worker {worker_id} found a test with error', file=sys.stderr)
                    test_found.value = True
            break

        if result == 'WA':
            with test_found.get_lock():
                if not test_found.value:
                    test_found.value = True
                    file_name = datetime.datetime.now().strftime('%Y-%m-%d %H\'%M\'%S') + '.txt'
                    buffer = []

                    log(buffer, global_divider, '\n')
                    log_block(buffer, 'Checker message:', worker_error_file, checker_time)
                    log(buffer, local_divider, '\n')
                    log_block(buffer, 'Input:', worker_input_file, gen_time)
                    log(buffer, local_divider, '\n')
                    log_block(buffer, 'Stupid answer:', worker_stupid_ans, stupid_time)
                    log(buffer, local_divider, '\n')
                    log_block(buffer, 'Smart answer:', worker_smart_ans, smart_time)
                    log(buffer, global_divider, '\n')

                    open(f'{SAVE_TEST_PATH}/{file_name}', 'w').write(''.join(buffer))
            break
    if os.path.exists(directory):
        shutil.rmtree(directory)
    return

def stress():
    atomic_print('Start stressing')
    atomic_print(global_divider)

    workers = []
    for i in range(THREADS):
        worker = threading.Thread(target=stress_worker, args=(i,))
        workers.append(worker)
        worker.start()

    for worker in workers:
        worker.join()

    if test_found.value:
        atomic_print('Test found with WA or ERROR')
    else :
        atomic_print('All workers finished')

def main(config_file):
    start_time = timeit.default_timer()
    prepare(config_file)
    stress()
    end_time = timeit.default_timer()
    atomic_print(f'Total time: {to_ms(end_time - start_time)}')
