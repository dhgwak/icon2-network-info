from lib.s3_manager import S3Manager
from lib.base import (
    os_env, load_yaml, dump_yaml,
    service_name, make_readme,
    compare_dict, kvPrint,
    cPrint, banner, dividing_line
)

import json
import argparse


def get_parser():
    parser = argparse.ArgumentParser(prog='CTX ENV Initializer')
    parser.add_argument('command', choices=[
        'config', 'upload', 'show', 'all'
    ], nargs="?", help='command', default="config")
    parser.add_argument('-s', '--service', type=str, help=f'Service')
    parser.add_argument('-u', '--upload', type=bool, help=f'Upload', default=False)
    return parser.parse_args()


class InitConfig:

    def __init__(self, args):
        self.args = args
        self.env = load_yaml("info.yml")
        self.s3m = None
        self.to_be = dict()
        self.as_is = dict()
        self.is_upload = False

    def config(self, ):
        if self.args.get("service"):
            self.env['network_list'] = self.args.get("service").split(',')
        for service in self.env['network_list']:
            dividing_line()
            _service = service_name(service)
            kvPrint(service, _service)
            as_is_file = f"icon2/{_service}/default_configure.yml"
            self.as_is[_service] = load_yaml(as_is_file)
            self.to_be[_service] = load_yaml(f"icon2/base_configure.yml")
            self.to_be[_service]['version'] = self.env[_service].get('version', None)
            self.to_be[_service]['settings']['env']['SERVICE'] = _service
            self.to_be[_service]['settings']['env']['CID'] = self.env[_service]['env'].get('CID', None)
            self.to_be[_service]['settings']['env']['NID'] = self.env[_service]['env'].get('NID', None)
            self.to_be[_service]['settings']['env']['ENDPOINT'] = self.env[_service]['env'].get('ENDPOINT', None)
            self.to_be[_service]['settings']['env']['GENESIS'] = self.env[_service]['env'].get('GENESIS', None)
            self.to_be[_service]['settings']['env']['IISS'] = self.env[_service]['env'].get('IISS', None)
            self.to_be[_service]['settings']['genesis'] = self.env[_service]['env'].get('GENESIS', None)
            self.to_be[_service]['settings']['iiss'] = self.env[_service]['env'].get('IISS', None)
            icon2_file = f"icon2/{_service}/default_configure.yml"
            dump_yaml(icon2_file, self.to_be[_service])
            compare_result = compare_dict(self.as_is[_service], self.to_be[_service])
            cPrint("- Compare Result:", "yellow")
            print(compare_result)
            cPrint("- To-Be Result:", "yellow")
            print(json.dumps(self.to_be[_service]['settings'], indent=4))
        make_readme("README.md", self.env)
        dividing_line()

    def upload(self, ):
        if self.args.get("service"):
            self.env['network_list'] = self.args.get("service").split(',')
        for service in self.env['network_list']:
            _service = service_name(service)
            s3_config_file = f"{self.env['web_url'].split('/')[-1]}/{_service}/default_configure.yml"
            s3_gs_file = f"{self.env['web_url'].split('/')[-1]}/{_service}/icon_genesis.zip"
            icon2_file = f"icon2/{_service}/default_configure.yml"
            genesis_file = f"icon2/{_service}/icon_genesis.zip"
            # self.s3m.upload(
            #     os_env(self.env['git_env']['aws_bucket']),
            #     s3_config_file,
            #     icon2_file
            # )
            self.s3m.upload(
                os_env(self.env['git_env']['aws_bucket']),
                s3_gs_file,
                genesis_file
            )
        self.s3m.cf_re_caching(os_env(self.env['git_env']['aws_cf_id']))

    def show_contents(self, ):
        kvPrint("S3 Contents", os_env(self.env['git_env']['aws_bucket']))
        bucket_name = os_env(self.env['git_env']['aws_bucket'])
        prefix = self.env['web_url'].split('/')[-1]
        for content in self.s3m.content_list(bucket_name, prefix):
            print(" - ", content)

    def run(self, ):
        banner(self.env['version'])
        dividing_line("=")
        if self.args['command'] == "all":
            cPrint("[CONFIG & UPLOAD]", "red")
            self.config()
            self.s3m = S3Manager(
                os_env(self.env['git_env']['aws_access_key_id']),
                os_env(self.env['git_env']['aws_secret_access_key']),
                os_env(self.env['git_env']['aws_default_region'])
            )
            self.upload()
            self.show_contents()
        elif self.args['command'] == "config":
            cPrint("[CONFIG]", "red")
            self.config()
        elif self.args['command'] == "upload":
            self.s3m = S3Manager(
                os_env(self.env['git_env']['aws_access_key_id']),
                os_env(self.env['git_env']['aws_secret_access_key'])
            )
            cPrint("[UPLOAD]", "red")
            self.upload()
            self.show_contents()
        elif self.args['command'] == "show":
            cPrint("[SHOW]", "red")
            self.show_contents()
        else:
            cPrint(f"[!] Please check command ( command={self.args['command']} )", "red")
        dividing_line("=")


if __name__ == '__main__':
    args = vars(get_parser())
    IC = InitConfig(args)
    IC.run()
