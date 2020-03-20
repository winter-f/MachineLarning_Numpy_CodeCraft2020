# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/3/20 6:48
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmail.com
# ------------------------------------
import os
import re


PACKAGE_NAME = "Numpy-ML-CodeCraft"
ENCODING = "utf-8"

PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))

RELEASE_DIR = os.path.join(PROJECT_DIR, "release")
os.makedirs(RELEASE_DIR, exist_ok=True)
TARGET_MODEL_PATH = os.path.join(RELEASE_DIR, "Main.py")

CORED_DIR = os.path.join(PROJECT_DIR, "core")
ORDERED_CORE_PARTS = [
	'common',
	'functions',
	'dataloader',
	'models'
]


def del_relative_import(file_path):
    with open(file_path, 'r', encoding=ENCODING) as f:
        s = f.read()
        s = re.sub('from (?:Numpy-ML-CodeCraft)?\..*', '', s)
        s = re.sub('#.*', '', s)
        return s


def convert_model(model_path, target_path=TARGET_MODEL_PATH):
    text_converted = ""

    for core_part_name in ORDERED_CORE_PARTS:
        core_file_path = os.path.join(CORED_DIR, core_part_name+'.py')
        text_converted += del_relative_import(core_file_path)

    text_converted += del_relative_import(model_path)

    with open(target_path, "w", encoding=ENCODING) as f:
        f.write(text_converted)
        print("Successfully convert your model into file_path {}".format(target_path))


if __name__ == '__main__':
    model_path = os.path.join(RELEASE_DIR, "model_1_MBSGD.py")
    convert_model(model_path, target_path=TARGET_MODEL_PATH)
