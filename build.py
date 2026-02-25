"""
PyInstaller 打包脚本
运行方式: python build.py
将 salary-calculator GUI 应用打包为单个可执行文件
"""
import PyInstaller.__main__
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PyInstaller.__main__.run([
    os.path.join(BASE_DIR, 'app.py'),
    '--name=salary-calculator',
    '--onefile',
    '--windowed',
    # 添加數據文件
    f'--add-data={os.path.join(BASE_DIR, "logic")}' + os.pathsep + 'logic',
    f'--add-data={os.path.join(BASE_DIR, "util")}' + os.pathsep + 'util',
    f'--add-data={os.path.join(BASE_DIR, "gui")}' + os.pathsep + 'gui',
    # 隱藏導入
    '--hidden-import=logic',
    '--hidden-import=logic.PreDataLogic',
    '--hidden-import=logic.OverAllDataLogic',
    '--hidden-import=logic.PersonalDataLogic',
    '--hidden-import=util.FileUtil',
    '--hidden-import=util.SalaryDetailUtil',
    '--hidden-import=util.SalaryPersonalDetailUtil',
    '--hidden-import=openpyxl',
    '--hidden-import=pandas',
    '--hidden-import=xlrd',
    # 清理
    '--clean',
    '--noconfirm',
])
