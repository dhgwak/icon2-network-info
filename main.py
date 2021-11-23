#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from lib.s3_manager import S3Manager
from lib.base import (
    os_env, load_yaml, dump_yaml,
    web_config, service_name, make_readme,
    compare_obj, dump, kvPrint,
    cPrint, banner
)


import os


class InitConfig:

    def __init__(self, ):
        self.env = load_yaml("info.yml")
        self.s3m = S3Manager(
            os_env(self.env['git_env']['aws_access_key_id']),
            os_env(self.env['git_env']['aws_secret_access_key'])
        )
        self.to_be = dict()
        self.as_is = dict()
        self.is_upload = False

    def run(self, ):
        banner(self.env['version'])
        for service in self.env['network_list']:
            cPrint("-" * os.get_terminal_size().columns)
            _service = service_name(service)
            kvPrint(service, _service)
            web_url = f"{self.env['web_url']}/{_service}/default_configure.yml"
            self.as_is[_service] = web_config(web_url)
            self.to_be[_service] = load_yaml("icon2/base_configure.yml")
            self.to_be[_service]['version'] = self.env[_service].get('version', None)
            self.to_be[_service]['settings']['env']['SERVICE'] = _service
            self.to_be[_service]['settings']['env']['CID'] = self.env[_service]['env'].get('CID', None)
            self.to_be[_service]['settings']['env']['NID'] = self.env[_service]['env'].get('NID', None)
            self.to_be[_service]['settings']['env']['ENDPOINT'] = self.env[_service]['env'].get('ENDPOINT', None)
            self.to_be[_service]['settings']['genesis'] = self.env[_service].get('genesis', None)
            self.to_be[_service]['settings']['iiss'] = self.env[_service].get('iiss', None)
            config_file = f"icon2/{_service}/default_configure.yml"
            dump_yaml(config_file, self.to_be[_service])
            compare_result = compare_obj(self.as_is[_service], self.to_be[_service])
            dump(compare_result)
            if self.as_is[_service] != self.to_be[_service] and compare_result:
                self.is_upload = True
                self.s3m.upload(
                    os_env(self.env['git_env']['aws_bucket']),
                    config_file,
                    config_file
                )
        if self.is_upload:
            self.s3m.cf_re_caching(os_env(self.env['git_env']['aws_cf_id']))
        make_readme("README.md", self.env)
        cPrint("-" * os.get_terminal_size().columns)


if __name__ == '__main__':
    IC = InitConfig()
    IC.run()
