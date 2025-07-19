# cpgen

cpgen is a command-line tool that simplifies managing CMake projects for competitive programming. It helps you create, delete, and reset problems easily, configure and run stress tests.

## Features

- **Problem and project managament**: create/delete/reset projects and problems with one command
- **Stress-testing**: configure problem with conf file and launch python-based stress test (supports graders)

## Usage
To create a project named 1000div2 with problems labeled from 'a' to 'f':
```bash
python generator.py -g 1000div2 f
```

To create a new problem
```bash
python generator.py -c
```

## Options/Flags

- `-t`, `--template <template_name>`: choose the problem template (available: c++23(default), c++20, c++17, grader)
- `-c`, `--create <problem_name>`: create a new problem
- `-d`, `--delete <problem_name>`: delete an existing problem
- `-r`, `--reset <problem_name>`: reset a problem
- `-g`, `--gen <project_name> <problem_count/problem_letter>`: create a project with a specified number of problems (problem_count: number of problems | `problem_letter`: ended with a given letter (starting from 'a')).
- `-u`, `--update`: update utils files (checkers, config, stress)

# License
This project is licensed under the free [Unlicense](LICENSE)