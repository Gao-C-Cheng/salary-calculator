"""
salary-calculator 桌面 GUI 主窗口
使用 PyQt5 構建，左側菜單欄佔 30%，右側功能區佔 70%。
"""
import sys
import os

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QStackedWidget,
    QApplication, QSizePolicy
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QColor, QPalette

# 確保能導入同級模組
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gui.pages.pre_data_page import PreDataPage
from gui.pages.placeholder_page import PlaceholderPage


class MainWindow(QMainWindow):
    """主窗口：左側菜單 + 右側功能區"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("salary-calculator")
        self.setMinimumSize(1100, 700)
        self.resize(1200, 750)

        # 設定全局字體
        app_font = QFont("Microsoft YaHei", 10)
        QApplication.setFont(app_font)

        self._setup_ui()
        self._apply_styles()

    # ------------------------------------------------------------------ UI
    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ---- 左側菜單欄 (30%) ----
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        # Logo + 系統名稱
        header = QWidget()
        header.setObjectName("sidebarHeader")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(24, 28, 24, 20)
        header_layout.setSpacing(6)

        logo_label = QLabel("SC")
        logo_label.setObjectName("logoLabel")
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setFixedSize(56, 56)
        header_layout.addWidget(logo_label, alignment=Qt.AlignCenter)

        title_label = QLabel("salary-calculator")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title_label)

        sidebar_layout.addWidget(header)

        # 分隔線
        sep = QWidget()
        sep.setFixedHeight(1)
        sep.setObjectName("separator")
        sidebar_layout.addWidget(sep)

        # 菜單列表
        self.menu_list = QListWidget()
        self.menu_list.setObjectName("menuList")
        self.menu_list.setSpacing(4)
        self.menu_list.setIconSize(QSize(20, 20))

        menus = [
            ("前置数据处理", "📋"),
            ("汇总数据处理", "📊"),
            ("明细数据处理", "📄"),
        ]
        for text, icon_char in menus:
            item = QListWidgetItem(f"  {icon_char}  {text}")
            item.setSizeHint(QSize(0, 48))
            self.menu_list.addItem(item)

        self.menu_list.setCurrentRow(0)
        self.menu_list.currentRowChanged.connect(self._on_menu_changed)
        sidebar_layout.addWidget(self.menu_list)

        # 底部版本信息
        version_label = QLabel("v1.0.0")
        version_label.setObjectName("versionLabel")
        version_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(version_label)

        # ---- 右側功能區 (70%) ----
        self.stack = QStackedWidget()
        self.stack.setObjectName("contentStack")

        # 頁面
        self.pre_data_page = PreDataPage()
        self.summary_page = PlaceholderPage(
            "汇总数据处理",
            "此功能尚未开发，待「前置数据处理」完成后再进行开发。\n请联系开发者获取更多信息。"
        )
        self.detail_page = PlaceholderPage(
            "明细数据处理",
            "此功能尚未开发，待「前置数据处理」完成后再进行开发。\n请联系开发者获取更多信息。"
        )

        self.stack.addWidget(self.pre_data_page)
        self.stack.addWidget(self.summary_page)
        self.stack.addWidget(self.detail_page)

        # 佈局比例 30:70
        main_layout.addWidget(sidebar, 30)
        main_layout.addWidget(self.stack, 70)

    # ------------------------------------------------------------ 事件
    def _on_menu_changed(self, index: int):
        self.stack.setCurrentIndex(index)

    # ------------------------------------------------------------ 樣式
    def _apply_styles(self):
        self.setStyleSheet("""
            /* 全局 */
            QMainWindow {
                background-color: #f5f7fa;
            }

            /* 側邊欄 */
            #sidebar {
                background-color: #1e293b;
            }

            #sidebarHeader {
                background-color: #1e293b;
            }

            #logoLabel {
                background-color: #3b82f6;
                color: white;
                font-size: 22px;
                font-weight: bold;
                border-radius: 12px;
            }

            #titleLabel {
                color: #f1f5f9;
                font-size: 16px;
                font-weight: bold;
                padding-top: 4px;
            }

            #separator {
                background-color: #334155;
                margin-left: 16px;
                margin-right: 16px;
            }

            /* 菜單列表 */
            #menuList {
                background-color: #1e293b;
                border: none;
                padding: 8px 12px;
                outline: none;
            }
            #menuList::item {
                color: #94a3b8;
                border-radius: 8px;
                padding: 6px 12px;
                font-size: 14px;
            }
            #menuList::item:selected {
                background-color: #334155;
                color: #f1f5f9;
            }
            #menuList::item:hover:!selected {
                background-color: #2a3a50;
                color: #cbd5e1;
            }

            #versionLabel {
                color: #475569;
                font-size: 11px;
                padding: 12px;
            }

            /* 右側功能區 */
            #contentStack {
                background-color: #f5f7fa;
            }
        """)
