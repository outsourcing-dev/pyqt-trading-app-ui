from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFontDatabase
import os

class ProfitRateTable(QTableWidget):
    def __init__(self):
        super().__init__(6, 1)  # 6행 1열로 초기화 (수익률 종류별로 6개 행)
        self.load_custom_fonts()
        self.setup_table()
        
    def load_custom_fonts(self):
        """커스텀 폰트 로드"""
        fonts_dir = os.path.join('assets', 'fonts')
        loaded_fonts = []
        
        for font_file in os.listdir(fonts_dir):
            if font_file.endswith('.ttf'):
                font_path = os.path.join(fonts_dir, font_file)
                font_id = QFontDatabase.addApplicationFont(font_path)
                if font_id != -1:
                    families = QFontDatabase.applicationFontFamilies(font_id)
                    loaded_fonts.extend(families)
        
    def setup_table(self):
        """테이블 기본 설정"""
        # 수직 헤더 레이블 설정
        self.setVerticalHeaderLabels([
            'My Profit Rate', 'Daily', 'Weekly', 
            'Monthly', 'Yearly', 'Total Profit Rate'
        ])
        
        # 수평 헤더 숨기기 (빈 열이므로)
        self.horizontalHeader().setVisible(False)
        
        # 테이블 크기 설정
        self.setMinimumWidth(320)
        self.setMaximumWidth(320)
        
        # 기본 설정
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
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
                font-family: 'Mosk Medium 500';
                font-size: 14px;
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
        
    def update_profit_rates(self, profit_data):
        rates = [
            profit_data.get('my_rate', 0),
            profit_data.get('daily', 0),
            profit_data.get('weekly', 0),
            profit_data.get('monthly', 0),
            profit_data.get('yearly', 0),
            profit_data.get('total', 0)
        ]
        
        # 각 행의 수익률 업데이트
        for row, rate in enumerate(rates):
            item = QTableWidgetItem(f'{rate:+.2f}%')
            item.setTextAlignment(Qt.AlignCenter)
            
            # 수익률에 따라 색상 설정
            color = '#4CAF50' if rate >= 0 else '#FF5252'
            item.setForeground(QColor(color))
            
            self.setItem(row, 0, item)
            
    def update_single_rate(self, rate_type, value):
        """
        단일 수익률 업데이트
        Args:
            rate_type: 수익률 종류 ('my_rate', 'daily', 'weekly', 'monthly', 'yearly', 'total')
            value: 수익률 값
        """
        row_map = {
            'my_rate': 0,
            'daily': 1,
            'weekly': 2,
            'monthly': 3,
            'yearly': 4,
            'total': 5
        }
        
        if rate_type in row_map:
            row = row_map[rate_type]
            item = QTableWidgetItem(f'{value:+.2f}%')
            item.setTextAlignment(Qt.AlignCenter)
            
            color = '#4CAF50' if value >= 0 else '#FF5252'
            item.setForeground(QColor(color))
            
            self.setItem(row, 0, item)