from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFontDatabase, QFont
import os

class TradeHistoryTable(QTableWidget):
    def __init__(self):
        super().__init__(10, 5)  # 10행 5열로 초기화
        self.load_custom_fonts()  # 폰트 로드
        self.setup_table()
        self.apply_modern_style()  # 현대적 스타일 적용

        # 초기 빈 행에도 배경색 적용
        self.initialize_empty_rows()
        
    def initialize_empty_rows(self):
        """빈 행에 기본 배경색 적용 - 모든 행의 모든 셀에 적용"""
        row_count = self.rowCount()
        col_count = self.columnCount()
        
        # 어두운 보라색 배경 (styles.py와 동일한 색상 사용)
        dark_bg = "#0F0326"  # 매우 어두운 보라색 배경
        
        # 모든 셀에 기본 아이템 설정
        for row in range(row_count):
            for col in range(col_count):
                if self.item(row, col) is None:  # 셀이 비어있는 경우
                    item = QTableWidgetItem("")
                    item.setBackground(QColor(dark_bg))  # 기본 배경색 설정
                    self.setItem(row, col, item)
    
        # 세로 헤더(행 번호) 색상 설정
        vheader = self.verticalHeader()
        vheader.setStyleSheet(f"background-color: {dark_bg}; color: #077A8F;")  # 부드러운 청록색 텍스트

    def load_custom_fonts(self):
        """커스텀 폰트 로드"""
        fonts_dir = os.path.join('assets', 'fonts')
        app_font_name = "NanumSquare"  # 기본값 설정
        
        # 폰트 파일들을 QFontDatabase에 등록
        font_path = os.path.join(fonts_dir, "NanumSquareOTF_acR.otf")
        if os.path.exists(font_path):
            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id != -1:
                font_families = QFontDatabase.applicationFontFamilies(font_id)
                if font_families and font_families[0]:
                    app_font_name = font_families[0]
        
        self.app_font_name = app_font_name  # 인스턴스 변수로 저장

    def setup_table(self):
        """테이블 기본 설정 (헤더 중앙 정렬 적용)"""
        headers = ['코인명', '보유 수량', '청산 가격', 
                '미실현 손익(수익률)', '실현 손익']
        
        # 헤더 설정
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        
        # 개별 헤더 아이템을 생성하여 중앙 정렬 적용
        for col in range(len(headers)):
            item = QTableWidgetItem(headers[col])
            item.setTextAlignment(Qt.AlignCenter)
            self.setHorizontalHeaderItem(col, item)

        # 헤더 크기 조정
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # 편집 비활성화
        self.setEditTriggers(QTableWidget.NoEditTriggers)

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
        # 현재 테이블 행 수 저장
        current_rows = self.rowCount()
        
        # 데이터에 맞게 행 수 설정 (기존과 동일)
        self.setRowCount(len(trade_data))
        
        # 이미 있는 데이터 처리 (기존 코드 그대로)
        if len(trade_data) == 0:
            # 데이터가 없을 때도 10행은 유지
            self.setRowCount(10)
            self.initialize_empty_rows()
            return
        
        for row, trade in enumerate(trade_data):
            # 코인명 (중앙 정렬, 흰색)
            coin_item = QTableWidgetItem(trade['coin'])
            coin_item.setTextAlignment(Qt.AlignCenter)
            coin_item.setForeground(QColor('#ffffff'))
            self.setItem(row, 0, coin_item)
            
            # 수량 (소수점 8자리까지, 중앙 정렬, 흰색)
            quantity_item = QTableWidgetItem(f"{trade['quantity']:.8f}")
            quantity_item.setTextAlignment(Qt.AlignCenter)
            quantity_item.setForeground(QColor('#ffffff'))
            self.setItem(row, 1, quantity_item)
            
            # 청산가 (소수점 2자리까지, 중앙 정렬, 흰색)
            liq_price_item = QTableWidgetItem(f"{trade['liq_price']:.2f}")
            liq_price_item.setTextAlignment(Qt.AlignCenter)
            liq_price_item.setForeground(QColor('#ffffff'))
            self.setItem(row, 2, liq_price_item)
            
            # 미실현 손익 (색상 적용, 중앙 정렬)
            unrealized = QTableWidgetItem(f"{trade['unrealized_pl']:+.2f}%")
            unrealized.setTextAlignment(Qt.AlignCenter)
            unrealized.setForeground(
                QColor('#4CAF50' if trade['unrealized_pl'] >= 0 else '#FF5252')
            )
            self.setItem(row, 3, unrealized)
            
            # 실현 손익 (색상 적용, 중앙 정렬)
            realized = QTableWidgetItem(f"{trade['realized_pl']:+.2f}")
            realized.setTextAlignment(Qt.AlignCenter)
            realized.setForeground(
                QColor('#4CAF50' if trade['realized_pl'] >= 0 else '#FF5252')
            )
            self.setItem(row, 4, realized)
        
        # 데이터 업데이트 후, 남은 셀도 배경색 설정
        # 만약 데이터가 10개 미만이면 10행까지 채움
        if len(trade_data) < 10:
            self.setRowCount(10)
            # row_count부터 10까지 비어있는 행을 채움
            for row in range(len(trade_data), 10):
                for col in range(self.columnCount()):
                    item = QTableWidgetItem("")
                    item.setBackground(QColor("#0F0326"))  # 어두운 보라색 배경
                    self.setItem(row, col, item)
            
    def add_trade(self, trade):
        """새로운 거래 데이터 한 줄 추가"""
        current_row = self.rowCount()
        self.setRowCount(current_row + 1)
        
        # 마지막 행 인덱스와 trade 데이터를 사용하여 직접 행 업데이트
        row = current_row
        
        # 코인명 (중앙 정렬, 흰색)
        coin_item = QTableWidgetItem(trade['coin'])
        coin_item.setTextAlignment(Qt.AlignCenter)
        coin_item.setForeground(QColor('#ffffff'))
        self.setItem(row, 0, coin_item)
        
        # 수량 (소수점 8자리까지, 중앙 정렬, 흰색)
        quantity_item = QTableWidgetItem(f"{trade['quantity']:.8f}")
        quantity_item.setTextAlignment(Qt.AlignCenter)
        quantity_item.setForeground(QColor('#ffffff'))
        self.setItem(row, 1, quantity_item)
        
        # 청산가 (소수점 2자리까지, 중앙 정렬, 흰색)
        liq_price_item = QTableWidgetItem(f"{trade['liq_price']:.2f}")
        liq_price_item.setTextAlignment(Qt.AlignCenter)
        liq_price_item.setForeground(QColor('#ffffff'))
        self.setItem(row, 2, liq_price_item)
        
        # 미실현 손익 (색상 적용, 중앙 정렬)
        unrealized = QTableWidgetItem(f"{trade['unrealized_pl']:+.2f}%")
        unrealized.setTextAlignment(Qt.AlignCenter)
        unrealized.setForeground(
            QColor('#4CAF50' if trade['unrealized_pl'] >= 0 else '#FF5252')
        )
        self.setItem(row, 3, unrealized)
        
        # 실현 손익 (색상 적용, 중앙 정렬)
        realized = QTableWidgetItem(f"{trade['realized_pl']:+.2f}")
        realized.setTextAlignment(Qt.AlignCenter)
        realized.setForeground(
            QColor('#4CAF50' if trade['realized_pl'] >= 0 else '#FF5252')
        )
        self.setItem(row, 4, realized)


    def apply_modern_style(self):
        """거래 내역 테이블에 부드러운 네온 스타일 적용"""
        from ui.styles import apply_soft_neon_style  # 공통 스타일 함수 임포트
        apply_soft_neon_style(self)
        
        # 테이블 특정 설정 추가
        header = self.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignCenter)
        header.setStretchLastSection(True)
        
        # 세로 헤더(행 번호) 색상 적용
        dark_bg = "#0F0326"  # 어두운 보라색 배경
        soft_cyan = "#077A8F"  # 부드러운 청록색
        vheader = self.verticalHeader()
        vheader.setStyleSheet(f"background-color: {dark_bg}; color: {soft_cyan};")
        
        # 빈 셀에도 배경색을 적용하기 위해 한 번 더 모든 셀 초기화
        self.initialize_empty_rows()