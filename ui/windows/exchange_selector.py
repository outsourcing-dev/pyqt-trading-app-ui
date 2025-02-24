from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                            QComboBox, QLabel, QPushButton, QApplication)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import json
import sys

class ExchangeSelector(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('거래소 선택창')
        self.setFixedSize(350, 170)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        
        title_label = QLabel('거래소')
        title_label.setAlignment(Qt.AlignLeft)
        
        self.exchange_combo = QComboBox()
        self.exchange_combo.setMaxVisibleItems(3)
        self.exchange_combo.addItems(['바이낸스', '바이비트', '비트겟'])
        self.exchange_combo.setStyle(self.style())
        
        self.confirm_button = QPushButton('선택 완료')
        self.confirm_button.clicked.connect(self.on_confirm_clicked)
        self.confirm_button.setCursor(Qt.PointingHandCursor)
        
        layout.addWidget(title_label)
        layout.addWidget(self.exchange_combo)
        layout.addWidget(self.confirm_button)
        layout.addStretch()
        
        self.apply_styles()

    def save_exchange_config(self, exchange):
        """선택된 거래소를 config.json에 저장"""
        try:
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump({'exchange': exchange}, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"설정 저장 중 오류 발생: {e}")
            return False

    def on_confirm_clicked(self):
        """선택 완료 버튼 클릭시 호출되는 함수"""
        exchange = self.exchange_combo.currentText()
        
        # config.json에 저장
        if self.save_exchange_config(exchange):
            print(f"선택된 거래소 {exchange} 저장 완료")
            
            # TODO: 다음 화면으로 전환
            from ui.trading_view import TradingView
            self.trading_view = TradingView()
            self.trading_view.show()
            self.close()
        else:
            print("설정 저장 실패")

    def apply_styles(self):
        self.setStyleSheet('''
            QMainWindow {
                background-color: #2a3447;
            }
            QLabel {
                color: white;
                font-size: 14px;
                font-weight: bold;
                margin-bottom: 5px;
            }
            QComboBox {
                background-color: #3d4760;
                color: white;
                padding: 8px;
                padding-right: 25px;
                border: 2px solid #4d5b7c;
                border-radius: 5px;
                font-size: 13px;
                min-height: 20px;
            }
            QComboBox:hover {
                background-color: #4d5b7c;
                border: 2px solid #5d6b8c;
            }
            QComboBox QAbstractItemView {
                background-color: #3d4760;
                color: white;
                selection-background-color: #4d5b7c;
                selection-color: white;
                border: none;
                outline: none;
                border-radius: 5px;
                padding: 0px;
                margin: 0px;
                spacing: 2px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 15px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                min-height: 20px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        ''')