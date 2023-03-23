#!/usr/bin/env python3
import json
import statistics

from netmiko import ConnectHandler

env = json.load(open('env.json'))


def ping(host, ip):

    device = {
        "device_type": "cisco_ios",
        "host": f"{host}",
        "username": f"{env['USER']}",
        "password": f"{env['PASSWORD']}",
        "secret": f"{env['SECRET']}",
    }

    try:
        with ConnectHandler(**device, allow_auto_change=True) as net_connect:
            command = f'ping {ip}'

            multi_lines = ""f'{net_connect.send_command(command)}'""
            lines = multi_lines.splitlines()
            for line in lines[3:]:
                if "Success rate is 0 percent" not in line:
                    ping_time = statistics.median(line.split()[-2].split('/'))
                    return ping_time
                else:
                    return "fail"

    except Exception as e:
        return "fail"


if __name__ == "__main__":
    ping()
