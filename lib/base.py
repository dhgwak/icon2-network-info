from datetime import datetime
from deepdiff import DeepDiff

import os
import sys
import yaml
import requests


class bcolors:
    red = "\033[91m"
    green = "\033[92m"
    yellow = "\033[93m"
    light_purple = "\033[94m"
    purple = "\033[95m"

    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def banner(version):
    print()
    print(f" ██████╗████████╗██╗  ██╗    ███████╗███╗   ██╗██╗   ██╗    ██╗███╗   ██╗██╗████████╗██╗ █████╗ ██╗     ██╗███████╗███████╗██████╗")
    print(f"██╔════╝╚══██╔══╝╚██╗██╔╝    ██╔════╝████╗  ██║██║   ██║    ██║████╗  ██║██║╚══██╔══╝██║██╔══██╗██║     ██║╚══███╔╝██╔════╝██╔══██╗")
    print(f"██║        ██║    ╚███╔╝     █████╗  ██╔██╗ ██║██║   ██║    ██║██╔██╗ ██║██║   ██║   ██║███████║██║     ██║  ███╔╝ █████╗  ██████╔╝")
    print(f"██║        ██║    ██╔██╗     ██╔══╝  ██║╚██╗██║╚██╗ ██╔╝    ██║██║╚██╗██║██║   ██║   ██║██╔══██║██║     ██║ ███╔╝  ██╔══╝  ██╔══██╗")
    print(f"╚██████╗   ██║   ██╔╝ ██╗    ███████╗██║ ╚████║ ╚████╔╝     ██║██║ ╚████║██║   ██║   ██║██║  ██║███████╗██║███████╗███████╗██║  ██║")
    print(f" ╚═════╝   ╚═╝   ╚═╝  ╚═╝    ╚══════╝╚═╝  ╚═══╝  ╚═══╝      ╚═╝╚═╝  ╚═══╝╚═╝   ╚═╝   ╚═╝╚═╝  ╚═╝╚══════╝╚═╝╚══════╝╚════ver.{version}")
    print()

def dump(obj, nested_level=0, output=sys.stdout):
    spacing = '   '
    def_spacing = '   '
    if type(obj) == dict:
        print('%s{' % (def_spacing + (nested_level) * spacing))
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print(bcolors.OKGREEN + '%s%s:' % (def_spacing + (nested_level + 1) * spacing, k) + bcolors.ENDC, end="")
                dump(v, nested_level + 1, output)
            else:
                # print >>  bcolors.OKGREEN + '%s%s: %s' % ( (nested_level + 1) * spacing, k, v) + bcolors.ENDC
                print(bcolors.OKGREEN + '%s%s:' % (def_spacing + (nested_level + 1) * spacing, k) + bcolors.WARNING + ' %s' % v + bcolors.ENDC,
                      file=output)
        print('%s}' % (def_spacing + nested_level * spacing), file=output)
    elif type(obj) == list:
        print('%s[' % (def_spacing + (nested_level) * spacing), file=output)
        for v in obj:
            if hasattr(v, '__iter__'):
                dump(v, nested_level + 1, output)
            else:
                print(bcolors.WARNING + '%s%s' % (def_spacing + (nested_level + 1) * spacing, v) + bcolors.ENDC, file=output)
        print('%s]' % (def_spacing + (nested_level) * spacing), file=output)
    else:
        print(bcolors.WARNING + '%s%s' % (def_spacing + nested_level * spacing, obj) + bcolors.ENDC)


def cPrint(msg, color="green"):
    print(getattr(bcolors, color) + "%s" % msg + bcolors.ENDC)


def kvPrint(key, value, value_check=False):
    class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

    key_width = 9
    key_value = 3

    is_print = True

    if value_check:
        is_print = False

        if value:
            is_print = True

    if is_print:
        print(bcolors.OKGREEN + "{:>{key_width}} : ".format(key, key_width=key_width) + bcolors.ENDC, end="")
        print(bcolors.WARNING + "{:>{key_value}} ".format(str(value), key_value=key_value) + bcolors.ENDC)


def service_name(service):
    return service.lower().rsplit('net', 1)[0].capitalize() + "Net"


def os_env(key):
    return os.getenv(key)


def load_yaml(file_name, ):
    with open(file_name, "r") as yml:
        yml_obj = yaml.load(yml, Loader=yaml.FullLoader)
    return yml_obj


def dump_yaml(file_name, data):
    with open(file_name, 'w') as yml:
        yaml.dump(data, yml)
    if os.path.exists(file_name):
        return True
    else:
        return False


def dump_file(file_name, data):
    with open(file_name, 'w') as f:
        f.write(data)
    if os.path.exists(file_name):
        return True
    else:
        return False


def web_config(url, ):
    res = requests.get(url)
    if res.status_code == 200:
        return yaml.load(res.text, Loader=yaml.FullLoader)
    else:
        return dict()


def compare_obj(as_is, to_be):
    return DeepDiff(as_is, to_be)


def make_readme(file_name, env):
    title = "## ICON2 Netwrok info\n"
    summary = f"```Describes information about the ICON2 network.```\n"
    gen_date = f"#### Update : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    main_contents = f"{title}{summary}{gen_date}"
    for service in env['network_list']:
        sub_title = f"### {service}\n"
        config_link = f"#### [{service} configuration]({env['web_url']}/{service}/default_configure.yml)\n"
        table_contents = "|key|value|\n"
        table_contents += "|-----|-----|\n"
        table_contents += f"|network_name|{service}|\n"
        table_contents += f"|cid|{env[service]['env']['CID']}|\n"
        table_contents += f"|nid|{env[service]['env']['NID']}|\n"
        for key, val in env[service]['info'].items():
            table_contents += f"|{key}|{val}|\n"
        main_contents += f"{sub_title}{config_link}{table_contents}"
    return dump_file(file_name, main_contents)
