"""
salary-calculator 桌面应用程序入口
使用 PyQt5 构建 GUI 界面
"""
import sys
import os
import logging.config

# ============================================================
# 修复 venv 环境下 PyQt5 找不到 Qt platform plugin 的问题
# 在导入任何 PyQt5 模块之前，动态定位 plugins 目录并写入环境变量
# ============================================================
def _fix_qt_plugin_path():
    """
    在 venv 环境中，PyQt5 的 Qt plugins 目录可能不在默认搜索路径中。
    此函数自动查找 PyQt5 安装位置下的 plugins 目录，并通过
    QT_PLUGIN_PATH 环境变量告知 Qt 正确的插件位置。
    """
    try:
        import PyQt5
        pyqt5_dir = os.path.dirname(PyQt5.__file__)
        # PyQt5 的 plugins 通常位于以下路径之一
        candidates = [
            os.path.join(pyqt5_dir, "Qt5", "plugins"),       # Windows / pip 安装
            os.path.join(pyqt5_dir, "Qt", "plugins"),         # 部分版本
            os.path.join(pyqt5_dir, "plugins"),               # 旧版本布局
        ]
        for path in candidates:
            if os.path.isdir(path):
                os.environ["QT_PLUGIN_PATH"] = path
                return
    except Exception:
        pass

_fix_qt_plugin_path()
# ============================================================

# 確保項目根目錄在 Python 路徑中
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from gui.main_window import MainWindow
from GlobalExceptionHandler import GlobalExceptionHandler
import LogConfig

# 配置日誌
logging.config.dictConfig(LogConfig.LOGGING_CONFIG)
logger = logging.getLogger(__name__)


def main():
    """應用程式主入口"""
    GlobalExceptionHandler.install()
    logger.info("salary-calculator GUI 应用启动")

    # 啟用高 DPI 支持
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setApplicationName("salary-calculator")

    window = MainWindow()
    window.show()

    logger.info("主窗口已显示")
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
