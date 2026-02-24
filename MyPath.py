import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCE = os.path.join(BASE_DIR, "resource")
LOG_FILE = os.path.join(BASE_DIR, 'app.log')
# input dir path
INPUT_DIR = os.path.join(RESOURCE, 'input')
# 中间文件目录
TEMP_DIR = os.path.join(RESOURCE, 'temp')
# 输出目录
OUTPUT_DIR = os.path.join(RESOURCE, 'output')