"""
占位页面 - 用于尚未开发的菜单功能
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt


class PlaceholderPage(QWidget):
    """通用占位页面，显示功能名称和提示信息"""

    def __init__(self, title: str, message: str):
        super().__init__()
        self._setup_ui(title, message)

    def _setup_ui(self, title: str, message: str):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(16)

        # 標題
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #1e293b;
        """)
        layout.addWidget(title_label)

        # 分隔
        layout.addSpacing(40)

        # 圖標
        icon_label = QLabel("🚧")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 64px;")
        layout.addWidget(icon_label)

        # 提示信息
        msg_label = QLabel(message)
        msg_label.setAlignment(Qt.AlignCenter)
        msg_label.setWordWrap(True)
        msg_label.setStyleSheet("""
            font-size: 14px;
            color: #64748b;
            line-height: 1.8;
            padding: 16px;
        """)
        layout.addWidget(msg_label)

        layout.addStretch()
