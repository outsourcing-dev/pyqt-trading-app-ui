from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFontDatabase, QFont
import os

class TradeHistoryTable(QTableWidget):
    def __init__(self):
        super().__init__(1, 5)  # 1행 5열로 초기화
        self.load_custom_fonts()  # 폰트 로드
        self.setup_table()
        self.apply_modern_style()  # 현대적 스타일 적용

        # 초기 빈 행에도 배경색 적용
        self.initialize_empty_rows()
        
    def initialize_empty_rows(self):
        """빈 행에 기본 배경색 적용"""
        row_count = self.rowCount()
        col_count = self.columnCount()
        
        # 모든 셀에 기본 아이템 설정
        for row in range(row_count):
            for col in range(col_count):
                if self.item(row, col) is None:  # 셀이 비어있는 경우
                    item = QTableWidgetItem("")
                    item.setBackground(QColor("#1e222d"))  # 기본 배경색 설정
                    self.setItem(row, col, item)

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
        self.setRowCount(len(trade_data))
        if len(trade_data) == 0:
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
        """거래 내역 테이블에 현대적인 스타일 적용"""
        header_color = "#3d4760"
        row_color = "#1e222d"
        alt_row_color = "#252836"
        text_color = "#e6e9ef"
        border_color = "#4d5b7c"
        
        # 테이블 스타일 설정
        self.setStyleSheet(f"""
            QTableWidget {{
                background-color: {row_color};
                color: {text_color};
                gridline-color: #3d4760;  /* 그리드라인 색상 설정 */
                font-size: 13px;
                border: none;
                border-radius: 8px;
                font-family: '{self.app_font_name}';
            }}
            
            /* 모든 셀에 배경색 적용 - 빈 셀 포함 */
            QTableWidget::item:empty {{
                background-color: {row_color};
            }}
            
            QTableWidget::item {{
                border-bottom: 1px solid #313646;
                padding: 5px 10px;
                background-color: {row_color};
            }}
            
            QTableWidget::item:alternate {{
                background-color: {alt_row_color};
            }}
            
            QTableWidget::item:selected {{
                background-color: #3d4760;
                color: white;
            }}
            
            /* 헤더 스타일 - 아래 테두리 추가 */
            QHeaderView::section {{
                background-color: {header_color};
                color: {text_color};
                padding: 8px;
                border: none;
                border-bottom: 1px solid {border_color};  /* 헤더 아래 테두리 추가 */
                font-family: '{self.app_font_name}';
                font-size: 14px;
                font-weight: bold;  /* 명시적으로 normal 지정 */

            }}
            
            /* 수평 헤더 스타일 - 세로 구분선 명확하게 설정 */
            QHeaderView::section:horizontal {{
                border-right: 1px solid {border_color};  /* 세로 구분선 색상 강화 */
                border-left: none; /* 왼쪽 테두리 제거 (중복 방지) */
            }}
            
            /* 첫 번째 헤더 섹션에 왼쪽 테두리 추가 (선택사항) */
            QHeaderView::section:horizontal:first {{
                border-left: 1px solid {border_color};
            }}
            
            /* 행 번호 헤더 스타일 추가 */
            QHeaderView::section:vertical {{
                background-color: {header_color};
                color: {text_color};
                border-right: 1px solid {border_color};
                border-bottom: 1px solid {border_color};
            }}
            
            /* 테이블 코너 버튼 스타일 (왼쪽 최상단 버튼) */
            QTableCornerButton::section {{
                background-color: {header_color};
                border: 1px solid {border_color};
            }}
            
            /* 스크롤바 스타일 */
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
        
        # 추가: 행 번호 숨기기 또는 배경색 설정
        # self.verticalHeader().setVisible(False)  # 행 번호 숨기기
        # 또는 행 번호를 표시하고 싶다면 아래 코드 사용
        vheader = self.verticalHeader()
        vheader.setStyleSheet(f"background-color: {header_color}; color: {text_color};")
        
        # 그림자 효과 추가
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)
        
        # 교차 행 색상 설정 (줄무늬 효과)
        self.setAlternatingRowColors(True)
        
        # 헤더 설정
        header = self.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignCenter)
        header.setStretchLastSection(True)
        
        # 그리드 표시 설정
        self.setShowGrid(True)  # 그리드 보이기 활성화