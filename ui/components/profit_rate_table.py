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
        """수익률 업데이트 - 양수는 형광 연두색, 음수는 형광 빨간색으로 단순화"""
        rates = [
            profit_data.get('my_rate', 0),
            profit_data.get('daily', 0),
            profit_data.get('weekly', 0),
            profit_data.get('monthly', 0),
            profit_data.get('yearly', 0),
            profit_data.get('total', 0)
        ]
        
        # 2가지 형광색만 사용
        neon_green = "#39FF14"  # 양수용 형광 연두색
        neon_red = "#FF2D2D"    # 음수용 형광 빨간색
        
        for row, rate in enumerate(rates):
            item = QTableWidgetItem(f'{rate:+.2f}%')
            item.setTextAlignment(Qt.AlignCenter)
            
            # 양수/음수에 따라 2가지 색상만 적용 (크기에 상관없이 동일한 색상)
            if rate >= 0:
                color = QColor(neon_green)  # 양수는 형광 연두색
            else:
                color = QColor(neon_red)    # 음수는 형광 빨간색
            
            item.setForeground(color)
            self.setItem(row, 0, item)
            
    def apply_modern_style(self):
        """수익률 테이블에 부드러운 네온 스타일 적용"""
        from ui.styles import apply_soft_neon_style  # 공통 스타일 함수 임포트
        apply_soft_neon_style(self)