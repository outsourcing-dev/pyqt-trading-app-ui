from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFontDatabase
import os

class TradeHistoryTable(QTableWidget):
    def __init__(self):
        super().__init__(1, 5)  # 1행 5열로 초기화
        self.load_custom_fonts()  # 폰트 로드 추가
        self.setup_table()
    
    def load_custom_fonts(self):
        """커스텀 폰트 로드"""
        fonts_dir = os.path.join('assets', 'fonts')
        font_families = []
        loaded_fonts = []

        # 폰트 파일들을 QFontDatabase에 등록
        for font_file in os.listdir(fonts_dir):
            if font_file.endswith('.ttf'):
                font_path = os.path.join(fonts_dir, font_file)
                font_id = QFontDatabase.addApplicationFont(font_path)
                if font_id != -1:
                    families = QFontDatabase.applicationFontFamilies(font_id)
                    # loaded_fonts.extend(families)
        # print(f"TradeHistoryTable에 로드된 폰트: {', '.join(loaded_fonts)}")

    def setup_table(self):
        """테이블 기본 설정"""
        # 헤더 설정
        headers = ['Coin Name', 'Quantity', 'Liquidation Price', 
                  'Unrealized P/L (Profit Rate)', 'Realized P/L']
        self.setHorizontalHeaderLabels(headers)
        
        # 기본 설정
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # 스타일 적용
        self.apply_styles()
        
    def apply_styles(self):
        """테이블 스타일 적용"""
        self.setStyleSheet('''
            QTableWidget {
                gridline-color: #3d4760;
                border: none;
                background-color: #1e222d; 
                font-size: 13px;
            }
            QTableWidget::item {
                padding: 5px;
                color: #e6e9ef;
            }
            QTableWidget::item:selected {
                background-color: #3d4760;
                color: #ffffff;
            }
            QTableWidget::item:selected:!active {
                background-color: #3d4760;
                color: #ffffff;
            }
            /* 가로 헤더 스타일 */
            QHeaderView::section:horizontal {
                background-color: #3d4760;
                color: #ffffff;
                padding: 5px;
                border: 1px solid #2a3447;
                font-family: 'Mosk Medium 500';
                font-size: 14px;
            }
            /* 세로 헤더 스타일 */
            QHeaderView::section:vertical {
                background-color: #3d4760;
                color: #ffffff;
                padding: 5px;
                border: 1px solid #2a3447;
            }
            /* 헤더 자체의 배경색 */
            QHeaderView {
                background-color: #3d4760;
            }
            QTableCornerButton::section {
                background-color: #3d4760;
                border: 1px solid #2a3447;
            }
        ''')
        
    def update_trade_history(self, trade_data):
        """
        거래 기록 테이블 업데이트
        Args:
            trade_data: 리스트 형태의 거래 데이터
                [
                    {
                        "coin": "BTC",          # 코인 이름
                        "quantity": 0.1,        # 수량
                        "liq_price": 50000.0,   # 청산가
                        "unrealized_pl": 5.2,   # 미실현 손익(%)
                        "realized_pl": 100.5    # 실현 손익
                    }
                ]
        """
        self.setRowCount(len(trade_data))
        
        for row, trade in enumerate(trade_data):
            # 코인명
            self.setItem(row, 0, QTableWidgetItem(trade['coin']))
            
            # 수량 (소수점 8자리까지)
            self.setItem(row, 1, QTableWidgetItem(f"{trade['quantity']:.8f}"))
            
            # 청산가 (소수점 2자리까지)
            self.setItem(row, 2, QTableWidgetItem(f"{trade['liq_price']:.2f}"))
            
            # 미실현 손익 (색상 적용)
            unrealized = QTableWidgetItem(f"{trade['unrealized_pl']:+.2f}%")
            unrealized.setForeground(
                QColor('#4CAF50' if trade['unrealized_pl'] >= 0 else '#FF5252')
            )
            self.setItem(row, 3, unrealized)
            
            # 실현 손익 (색상 적용)
            realized = QTableWidgetItem(f"{trade['realized_pl']:+.2f}")
            realized.setForeground(
                QColor('#4CAF50' if trade['realized_pl'] >= 0 else '#FF5252')
            )
            self.setItem(row, 4, realized)
            
    def add_trade(self, trade):
        """새로운 거래 데이터 한 줄 추가"""
        current_row = self.rowCount()
        self.setRowCount(current_row + 1)
        self.update_trade_history([trade])  # 마지막 줄에 새 데이터 추가