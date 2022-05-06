import json
import os
import re
from collections import defaultdict

import click as click


class ParseLogsException(BaseException):

    def __init__(self, path: str):
        self.path = path

    def __str__(self):
        return f'{self.__class__}\nCheck path to log file or directory with path {self.path} or credentials.'


def parse_logs(log_file):
    with open(log_file, 'r') as file:
        method_pattern = r'(POST|GET|PUT|DELETE|HEAD|OPTIONS)\b'
        remote_host_pattern = r'^(?:\d{1,3}\.){3}\d{1,3}'
        duration_pattern = r'\s\d+\n'
        date_pattern = r'\[[\w\s/:+-]*\]'
        url_pattern = r'\"https?://(\S*)\"'
        requests_number = 0
        methods_dict = {"GET": 0, "POST": 0, "PUT": 0, "DELETE": 0, "HEAD": 0, "OPTIONS": 0}
        all_requests = []
        dict_ip_requests = defaultdict(lambda: {"requests_number": 0})

        for line in file:
            method = re.search(method_pattern, line).group(0)
            remote_host = re.search(remote_host_pattern, line).group(0)
            request_duration = re.search(duration_pattern, line).group(0).replace('\n', '')
            date = re.search(date_pattern, line).group(0)
            is_url = re.search(url_pattern, line)
            url = is_url.group(0)[1:-1] if is_url else '-'
            request_info = {
                'method': method,
                'ip': remote_host,
                'duration': int(request_duration),
                'date': date,
                'url': url,
            }
            all_requests.append(request_info)
            requests_number += 1
            methods_dict[method] += 1
            dict_ip_requests[request_info['ip']]["requests_number"] += 1
        top_ips = dict(sorted(dict_ip_requests.items(), key=lambda x: x[1]["requests_number"], reverse=True)[0:3])
        top_durations = sorted(all_requests, key=lambda x: x['duration'], reverse=True)[0:3]

        result = {
            'top_ips': {k: v['requests_number'] for k, v in top_ips.items()},
            'top_longest': top_durations,
            'total_stat': methods_dict,
            'total_requests': len(all_requests),
        }
        with open(f'{log_file}.json', 'w', encoding="utf-8") as json_file:
            result = json.dumps(result, indent=4)
            json_file.write(result)


@click.command()
@click.option('--log_file', help='Path to log file or its name.')
def main(log_file):
    if os.path.isdir(log_file):
        for file in os.listdir(log_file):
            if file.endswith(".log") and os.access(file, os.R_OK):
                path_to_logfile = os.path.join(log_file, file)
                parse_logs(path_to_logfile)
    elif os.path.isfile(log_file) and os.access(log_file, os.R_OK):
        parse_logs(log_file)

    else:
        raise ParseLogsException(log_file)


if __name__ == '__main__':
    main()
