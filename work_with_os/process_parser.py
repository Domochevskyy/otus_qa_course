from itertools import groupby
from subprocess import PIPE, run
from time import gmtime, strftime


def run_command(command: list[str]) -> list[str]:
    ps_output = run(command, stdout=PIPE, text=True).stdout.splitlines()
    return ps_output


def parse_result(result: list[str]) -> str:
    lines = tuple((map(lambda x: x.split(), result[1:])))
    number_processes = len(lines)
    users = {splitted_line[0] for splitted_line in lines}

    memories = tuple(map(float, (line[3] for line in lines)))
    memories_sum = round(sum(memories), 3)
    max_memory_process = max(lines, key=lambda line: line[3])[10][:20]

    cpus = tuple(map(float, (splitted_line[2] for splitted_line in lines)))
    cpus_sum = round(sum(cpus), 3)
    max_cpu_process = max(lines, key=lambda line: line[2])[10][:20]

    users_with_processes = ((splitted_line[0], ' '.join(splitted_line[10:])) for splitted_line in lines)
    sorted_users_with_processes = sorted(users_with_processes, key=lambda x: x[0])
    grouped_usr_and_processed = tuple(
        (user, len(tuple(group))) for user, group in
        groupby(sorted_users_with_processes, key=lambda process: process[0])
    )
    newline = '\n'
    tab = '\t'
    result = f"""Отчёт о состоянии системы.
    Пользователи системы: {", ".join(users)}
    Процессов запущено: {number_processes}
    Пользовательских процессов:
    {f'{tab}'.join(f'{process[0]}: {process[1]}{newline}' for process in grouped_usr_and_processed)}
    Всего памяти используется: {memories_sum}%
    Всего CPU используется: {cpus_sum}%
    Больше всего памяти использует: {max_memory_process}
    Больше всего CPU использует: {max_cpu_process}
    """
    return result


def write_to_file(report: str) -> None:
    with open(f'{strftime("%d-%m-%Y-%H:%M:%S", gmtime())}-scan.txt', 'w', encoding='utf-8') as file:
        file.write(report)


if __name__ == '__main__':
    command = ['ps', 'aux']
    result = run_command(command)
    report = parse_result(result)
    print(report)
    write_to_file(report)
