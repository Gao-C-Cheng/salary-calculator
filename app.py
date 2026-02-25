"""
salary-calculator 桌面应用程序入口
使用 PyQt5 构建 GUI 界面
"""
import sys
import os
import logging.config

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
