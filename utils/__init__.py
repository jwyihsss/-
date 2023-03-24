# -*- coding: utf-8 -*-
from utils.path import root
from utils.models import Config
from utils.read_yaml_control import HandleYaml

config_data = HandleYaml(root / 'config.yml').read_yaml()
config = Config(**config_data)