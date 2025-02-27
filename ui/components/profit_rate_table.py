from PyQt5.QtWidgets import QTableWidget, QHeaderView, QGraphicsDropShadowEffect, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFontDatabase
import os

class ProfitRateTable(QTableWidget):
    def __init__(self):
        super().__init__(6, 1)  # 6행 1열로 초기화 (수익률 종류별로 6개 행)
        self.load_custom_fonts()
        self.setup_table()
        self.apply_modern_style()
    
    def load_custom_fonts(self):
        """NanumSquareOTF_acR 폰트 로드"""
        fonts_dir = os.path.join('assets', 'fonts')
        font_path = os.path.join(fonts_dir, "NanumSquareOTF_acR.otf")
        self.app_font_name = "NanumSquareOTF_acR"  # 기본값
        
        if os.path.exists(font_path):
            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id != -1:
                font_families = QFontDatabase.applicationFontFamilies(font_id)
                if font_families:
                    self.app_font_name = font_families[0]
    
    def setup_table(self):
        """테이블 기본 설정"""
        headers = ['개인 수익률', '일간', '주간', '월간', '연간', '전체 수익률']
        self.setVerticalHeaderLabels(headers)
        
        # 세로 헤더 중앙 정렬 설정
        vheader = self.verticalHeader()
        vheader.setDefaultAlignment(Qt.AlignCenter)
        
        # 컬럼 헤더 숨기기
        self.horizontalHeader().setVisible(False)
        
        # 크기 조정 설정
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # 편집 비활성화
        self.setEditTriggers(QTableWidget.NoEditTriggers)
    
    def update_profit_rates(self, profit_data):
        """수익률 업데이트"""
        rates = [
            profit_data.get('my_rate', 0),
            profit_data.get('daily', 0),
            profit_data.get('weekly', 0),
            profit_data.get('monthly', 0),
            profit_data.get('yearly', 0),
            profit_data.get('total', 0)
        ]
        
        for row, rate in enumerate(rates):
            item = QTableWidgetItem(f'{rate:+.2f}%')
            item.setTextAlignment(Qt.AlignCenter)
            
            color = QColor('#4CAF50' if rate >= 0 else '#FF5252')
            item.setForeground(color)
            
            if abs(rate) > 10:
                bg_color = QColor(color)
                bg_color.setAlpha(40)
                item.setBackground(bg_color)
            
            self.setItem(row, 0, item)
    
    def apply_modern_style(self):
        """수익률 테이블에 현대적인 스타일 적용"""
        header_color = "#3d4760"
        row_color = "#1e222d"
        alt_row_color = "#252836"
        text_color = "#e6e9ef"
        
        self.setStyleSheet(f"""
            QTableWidget {{
                background-color: {row_color};
                color: {text_color};
                gridline-color: #3d4760;
                font-size: 13px;
                border: none;
                border-radius: 8px;
                font-family: '{self.app_font_name}';
            }}
            
            QTableWidget::item {{
                border-bottom: 1px solid #3d4760;
                padding: 5px 10px;
                background-color: {row_color};
                font-family: '{self.app_font_name}';
                font-weight: bold;
            }}
            
            QTableWidget::item:alternate {{
                background-color: {alt_row_color};
            }}
            
            QTableWidget::item:selected {{
                background-color: #3d4760;
                color: white;
            }}
            
            QHeaderView::section {{
                background-color: {header_color};
                color: {text_color};
                padding: 8px;
                border: none;
                border-bottom: 1px solid #4d5b7c;
                font-weight: normal;
                font-family: '{self.app_font_name}';
                text-align: center;
                font-size: 14px;
                font-weight: bold;  /* 명시적으로 normal 지정 */
            }}
            
            QHeaderView::section:vertical {{
                border-right: 1px solid #3d4760;
                border-bottom: 1px solid #4d5b7c;
                text-align: center;
            }}
            
            QScrollBar:vertical {{
                background: {row_color};
                width: 8px;
                margin: 0px;
            }}
            
            QScrollBar::handle:vertical {{
                background: #4d5b7c;
                min-height: 20px;
                border-radius: 4px;
            }}
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)
        
        self.setAlternatingRowColors(True)
        self.setShowGrid(True)