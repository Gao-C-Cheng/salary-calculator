# salary-calculator

基于 PyQt5 的薪资数据处理桌面应用程序，用于处理 Excel 数据文件的转换和管理。

## 功能概览

本应用提供三个核心功能模块：

| 模块 | 功能 | 状态 |
|------|------|------|
| 前置数据处理 | 拆分预算单位归集表为单位机构表、数财对应指标表等 | ✅ 已完成 |
| 汇总数据处理 | 生成工资发放汇总表和工资汇总单 | 🚧 待开发 |
| 明细数据处理 | 生成个人工资明细表和车改住改补贴明细表 | 🚧 待开发 |

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行应用

```bash
python app.py
```

## 打包为 exe

使用以下任一方式打包：

```bash
# 方式一：使用打包脚本
python build.py

# 方式二：使用 spec 文件
pyinstaller salary-calculator.spec
```

打包完成后，可执行文件位于 `dist/salary-calculator.exe`。

## 项目结构

```
salary-calculator/
├── app.py                    # 应用入口
├── build.py                  # PyInstaller 打包脚本
├── salary-calculator.spec    # PyInstaller spec 配置
├── requirements.txt          # Python 依赖
├── MyPath.py                 # 路径配置
├── LogConfig.py              # 日志配置
├── GlobalExceptionHandler.py # 全局异常处理
├── gui/                      # GUI 界面模块
│   ├── main_window.py        # 主窗口（侧边栏 + 功能区）
│   └── pages/
│       ├── pre_data_page.py      # 前置数据处理页面
│       └── placeholder_page.py   # 占位页面
├── logic/                    # 业务逻辑
│   ├── PreDataLogic.py       # 前置数据处理逻辑
│   ├── OverAllDataLogic.py   # 汇总数据处理逻辑
│   └── PersonalDataLogic.py  # 明细数据处理逻辑
├── util/                     # 工具类
│   ├── FileUtil.py
│   ├── SalaryDetailUtil.py
│   └── SalaryPersonalDetailUtil.py
└── resource/                 # 资源目录
    ├── input/                # 输入文件
    ├── temp/                 # 中间文件
    └── output/               # 输出文件
```

## 使用说明

### 前置数据处理

1. 启动应用后，左侧菜单默认选中「前置数据处理」
2. 将 Excel 文件拖拽到上传区域，或点击「选择文件」按钮浏览选择
3. 支持 `.xlsx` 和 `.xls` 格式
4. 点击「选择输出路径」按钮设置输出目录（默认为当前工作目录）
5. 点击「开始转换」按钮执行数据拆分
6. 处理完成后会显示成功/失败状态及生成的文件列表
