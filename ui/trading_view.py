from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
    QTableWidgetItem, QLabel, QComboBox, QHeaderView, QSizePolicy, QSplitter, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, QTimer, QEvent  
from PyQt5.QtGui import QColor, QFontDatabase, QFont
import pyqtgraph as pg
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta
import os
from datetime import datetime, timedelta

# 차트 관련 클래스들 임포트
from chart.candlestick import CandlestickItem
from chart.candlestick import apply_matching_neon_style
from chart.trade_marker import TradeMarker
from data.data_fetcher import DataFetcher
from utils.naver_time import NaverTimeFetcher
from chart.profit_rate_chart import TotalProfitChart
from ui.components.trade_history_table import TradeHistoryTable
from ui.components.profit_rate_table import ProfitRateTable
from ui.styles import apply_soft_neon_style  # 공통 스타일 함수 임포트

# 글로벌 변수로 app_font_name 선언
app_font_name = "NanumSquare"  # 기본값

def load_nanum_font():
    """NanumSquareOTF_acR 폰트를 로드하고 기본 폰트로 설정"""
    global app_font_name  # 글로벌 변수 사용
    
    font_dir = os.path.join("assets", "fonts")  # 폰트가 저장된 폴더 위치
    font_path = os.path.join(font_dir, "NanumSquareOTF_acR.otf")  # 사용할 폰트
    
    if os.path.exists(font_path):
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_families = QFontDatabase.applicationFontFamilies(font_id)
            if font_families:
                print(f"✅ 로드된 폰트: {font_families[0]}")
                app_font_name = font_families[0]  # 글로벌 변수 업데이트
                return app_font_name
    
    print("⚠️ NanumSquareOTF_acR 폰트 로드 실패")
    return app_font_name  # 기본 폰트 (예비용)

# QApplication 실행 전에 폰트 로드
app_font_name = load_nanum_font()

class TradingView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Trading Platform')
        self.total_profit_rate = 0.0
        
        # 컴포넌트 초기화
        self.profit_chart = TotalProfitChart()
        self.data_fetcher = DataFetcher()
        self.trades = []
        self.open_positions = {}
        
        # UI 초기화 및 설정
        self.initialize_ui()
    
    def initialize_ui(self):
        """UI 초기화 및 설정을 위한 통합 메서드"""
        # 기본 설정
        self.load_fonts()
        self.setGeometry(200, 200, 1280, 720)
        
        # UI 기본 요소 설정
        self.setup_ui()
        
        # 이벤트 처리 및 포커스 정책 설정
        self.setup_focus_policy()
        
        # 스타일 및 시각적 효과 적용 - 그래픽 효과 중복 방지를 위해 순서 중요
        self.apply_styles()  
        
        # 타이머 설정 및 초기 데이터 로드
        self.setup_timers()
        self.update_data()
        
        # modern UI 효과는 가장 마지막에 적용 (다른 스타일 설정 후)
        self.apply_modern_ui()
    
    def load_fonts(self):
        """모든 필요한 폰트를 로드하는 메서드"""
        # 나눔 폰트는 이미 글로벌로 로드되었으므로 추가 폰트만 로드
        self.load_additional_fonts()
    
    def load_additional_fonts(self):
        """추가 커스텀 폰트 로드"""
        fonts_dir = os.path.join('assets', 'fonts')
        font_families = []
        
        # 폰트 파일들을 QFontDatabase에 등록
        if os.path.exists(fonts_dir):
            for font_file in os.listdir(fonts_dir):
                if font_file.endswith('.ttf') or font_file.endswith('.otf'):
                    font_path = os.path.join(fonts_dir, font_file)
                    if os.path.exists(font_path):
                        font_id = QFontDatabase.addApplicationFont(font_path)
                        if font_id != -1:
                            font_families.extend(QFontDatabase.applicationFontFamilies(font_id))
        
        return font_families
    
    def setup_ui(self):
        """UI 레이아웃 및 컴포넌트 설정"""
        # 메인 윈도우 설정
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)  # 여백 축소

        # 1. 프로그램 이름
        self.setup_header(main_layout)
        
        # 프로그램 메인 레이아웃
        body_layout = QHBoxLayout()
        body_layout.setSpacing(5)  # 컴포넌트 간 간격 축소
        main_layout.addLayout(body_layout)

        # 레이아웃 분할
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)  # 여백 제거
        
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)  # 여백 제거
        
        # 레이아웃 비율 조정 (왼쪽:오른쪽 = 5:3)
        body_layout.addLayout(left_layout, 5)
        body_layout.addLayout(right_layout, 3)

        # 왼쪽 영역 구성
        self.setup_left_area(left_layout)
        
        # 오른쪽 영역 구성
        self.setup_right_area(right_layout)
        
        # 테스트 데이터 로드
        self.load_test_data()
    
    def setup_header(self, parent_layout):
        """헤더 영역 설정 (프로그램 이름)"""
        program_name_layout = QHBoxLayout()
        self.program_name = QLabel('Program Name')
        self.program_name.setObjectName("program_name")
        self.program_name.setStyleSheet('font-size: 16px; font-weight: bold; color: white;')
        program_name_layout.addWidget(self.program_name)
        parent_layout.addLayout(program_name_layout)
    
    def setup_left_area(self, parent_layout):
        """왼쪽 영역 설정 (차트, 정보, 테이블)"""
        # 1. 상단 정보 섹션
        self.setup_top_info(parent_layout)
        
        # 2. 차트 영역 설정
        self.setup_chart(parent_layout)
        
        # 3. 거래 기록 테이블
        self.left_table = TradeHistoryTable()
        parent_layout.addWidget(self.left_table)
    
    def setup_top_info(self, parent_layout):
        """상단 정보 영역 설정 (가격, 차트 타입, 시간)"""
        left_top_info = QHBoxLayout()
        left_top_info.setContentsMargins(0, 0, 0, 2)  # 여백 최소화
        left_top_info.setSpacing(5)  # 컴포넌트 간 간격 축소
        
        # 현재가 표시 라벨
        self.price_label = QLabel()
        self.price_label.setObjectName("price_label")  # 객체 이름 설정
        self.price_label.setStyleSheet('font-size: 16px; font-weight: bold; color: white;')

        # 차트 타입 선택 콤보박스 (캔들/라인)
        self.chart_type = QComboBox()
        self.chart_type.addItems(['Candle', 'Line'])
        self.chart_type.setStyleSheet('background-color: #2a2f3a; color: white; padding: 5px;')
        self.chart_type.currentTextChanged.connect(self.update_chart)
        self.chart_type.setMaximumWidth(80)  # 콤보박스 너비 제한

        # 네이버 시간 표시 라벨
        self.time_label = QLabel()
        self.time_label.setObjectName("time_label")  # CSS 스타일 적용을 위한 객체 이름 설정
        self.time_label.setStyleSheet(f'''
            color: #e6e9ef;
            font-family: '{app_font_name}';
            font-size: 14px;
            padding: 5px;
        ''')

        left_top_info.addWidget(self.price_label)
        left_top_info.addWidget(self.chart_type)
        left_top_info.addStretch()  # 왼쪽 요소들과 시간 사이 공간
        left_top_info.addWidget(self.time_label)
        parent_layout.addLayout(left_top_info)
    
    def setup_chart(self, parent_layout):
        """차트 설정"""
        # 차트 위젯 생성
        self.left_chart_widget = pg.PlotWidget()
        self.left_chart_widget.setBackground('black')
        self.left_chart_widget.showGrid(x=True, y=True)
        self.left_chart_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # 캔들스틱과 라인차트 아이템 생성
        self.candlestick_item = CandlestickItem()
        self.left_chart_widget.addItem(self.candlestick_item)

        # 라인 차트 초기화
        self.line_plot = None
        
        # 매매 표시 마커
        self.trade_markers = TradeMarker()
        self.left_chart_widget.addItem(self.trade_markers)

        # 레이아웃에 차트 추가
        parent_layout.addWidget(self.left_chart_widget)
    
    def setup_right_area(self, parent_layout):
        """오른쪽 영역 설정 (위젯, 차트, 수익률 표)"""
        # 1. 오른쪽 상단 빈 공간
        right_empty_widget = QWidget()
        right_empty_widget.setObjectName("right_empty_widget")
        right_empty_widget.setMinimumWidth(300)
        right_empty_widget.setMaximumSize(300, 150)

        # 소프트한 네온 색상 정의
        dark_bg = "#0F0326"     # 매우 어두운 보라색 배경
        soft_pink = "#AA0A80"   # 부드러운 핑크 테두리
        soft_purple = "#5E1387" # 부드러운 보라색

        # 스타일시트 적용
        right_empty_widget.setStyleSheet(f'''
            background-color: {dark_bg};
            border: 2px solid {soft_pink};
            border-radius: 10px;
        ''')

        # 부드러운 네온 효과 추가
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(15)  # 부드러운 블러
        glow.setColor(QColor(soft_purple))
        glow.setOffset(0, 0)
        right_empty_widget.setGraphicsEffect(glow)

        parent_layout.addWidget(right_empty_widget, stretch=1)

        # 2. 수익률 차트
        profit_chart_widget = self.profit_chart.get_widget()
        parent_layout.addWidget(profit_chart_widget)

        # 3. 수익률 표시 영역
        self.right_table = ProfitRateTable()
        self.right_table.setMinimumWidth(300)
        self.right_table.setMaximumWidth(300)
        parent_layout.addWidget(self.right_table)
    
    def load_test_data(self):
        """테스트용 데이터 로드"""
        # 거래 기록 테스트 데이터
        test_trades = [
            {
                "coin": "BTC",
                "quantity": 0.1234,
                "liq_price": 50000.0,
                "unrealized_pl": 5.2,
                "realized_pl": 100.5
            }
        ]
        self.left_table.update_trade_history(test_trades)
        
        # 수익률 표 테스트용 데이터
        test_profit_data = {
            'my_rate': -5.2,
            'daily': 1.5,
            'weekly': 4.2,
            'monthly': 15.7,
            'yearly': 45.2,
            'total': -25.5
        }
        self.right_table.update_profit_rates(test_profit_data)
        
        # 수익률 차트 테스트 데이터
        # 기존 데이터 초기화 (중복 방지)
        self.profit_chart.daily_total_profits = []
        
        # 테스트 데이터 생성
        base_date = datetime.now()
        dates = [(base_date - timedelta(days=i)).strftime('%m/%d') for i in range(6, -1, -1)]
        test_data = [10.5, 15.2, -54.3, 8.7, 12.1, -3.2, 150.5]
        
        for date, profit in zip(dates, test_data):
            self.profit_chart.daily_total_profits.append((date, profit))
        
        # 차트 업데이트
        self.profit_chart.update_display()
    
    def setup_focus_policy(self):
        """테이블 포커스 정책 설정"""
        # 테이블 위젯에 이벤트 필터 설치
        self.left_table.installEventFilter(self)
        self.right_table.installEventFilter(self)
        
        # 전체 윈도우에도 이벤트 필터 설치
        self.centralWidget().installEventFilter(self)
        
        # 테이블 클릭 이벤트 연결
        self.left_table.clicked.connect(lambda: self.handle_table_click(self.left_table))
        self.right_table.clicked.connect(lambda: self.handle_table_click(self.right_table))
    
    def eventFilter(self, obj, event):
        """이벤트 필터"""
        if event.type() == QEvent.MouseButtonPress:
            # 클릭된 객체가 테이블이 아닌 경우 모든 테이블의 선택 해제
            if not isinstance(obj, QTableWidget):
                self.left_table.clearSelection()
                self.right_table.clearSelection()
                self.left_table.setCurrentItem(None)
                self.right_table.setCurrentItem(None)
                return False
            
            # 테이블 내 클릭 처리
            if isinstance(obj, QTableWidget):
                pos = event.pos()
                item = obj.itemAt(pos)
                if item is None:  # 빈 공간 클릭
                    obj.clearSelection()
                    obj.setCurrentItem(None)
                    # 다른 테이블의 선택도 해제
                    other_table = self.right_table if obj == self.left_table else self.left_table
                    other_table.clearSelection()
                    other_table.setCurrentItem(None)
        
        return super().eventFilter(obj, event)
    
    def handle_table_click(self, clicked_table):
        """테이블 클릭 처리"""
        # 다른 테이블의 선택 해제
        other_table = self.right_table if clicked_table == self.left_table else self.left_table
        other_table.clearSelection()
        other_table.setCurrentItem(None)
    
    def setup_timers(self):
        """모든 타이머 설정"""
        # 차트 데이터 업데이트 (1분)
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_data)
        self.update_timer.start(1000)  # 1초마다 업데이트 (테스트 용도)
        
        # 시간 표시 업데이트 (1초)
        self.time_timer = QTimer()
        self.time_timer.timeout.connect(self.update_time)
        self.time_timer.start(1000)
    
    def update_data(self):
        """데이터 업데이트"""
        # 현재가 업데이트
        current_price = self.data_fetcher.get_current_price()
        if current_price:
            self.price_label.setText(f'BTC/USDT: {current_price:,.1f}')

        # 차트 데이터 업데이트
        candle_data, df = self.data_fetcher.fetch_ohlcv()
        if candle_data is not None:
            self.update_chart_data(candle_data, df)
    
    def update_chart_data(self, candle_data, df):
        """차트 데이터 업데이트 처리"""
        # UTC 시간을 한국 시간(KST)으로 변환 (UTC+9)
        if 'timestamp' in df.columns:
            df['timestamp'] = df['timestamp'].dt.tz_localize('UTC').dt.tz_convert('Asia/Seoul')
        
        # x축 레이블 설정 - 30분 단위만 표시
        ticks = []
        for i, ts in enumerate(df['timestamp']):
            # 정각(00분)이나 30분인 경우에만 레이블 추가
            if ts.minute in [0, 30]:
                time_str = ts.strftime('%H:%M')
                ticks.append((i, time_str))
            
        self.left_chart_widget.getAxis('bottom').setTicks([ticks])
        
        # 캔들스틱 데이터 설정
        self.candlestick_item.set_data(candle_data)

        # 라인차트 데이터 설정
        if self.line_plot is None:
            self.line_plot = self.left_chart_widget.plot(
                np.arange(len(df)), 
                df['close'].values,
                pen='w'
            )
        else:
            self.line_plot.setData(
                np.arange(len(df)), 
                df['close'].values
            )
        # 기본적으로 라인차트 숨김 (차트 타입에 따라 표시 결정)
        self.line_plot.hide()
    
    def update_time(self):
        """네이버 서버 시간을 가져와서 업데이트"""
        kr_time = NaverTimeFetcher.get_naver_time()
        weekday = ['월', '화', '수', '목', '금', '토', '일'][kr_time.weekday()]
        time_str = kr_time.strftime(f'%Y-%m-%d({weekday}) %H:%M:%S')
        self.time_label.setText(time_str)
    
    def update_chart(self, chart_type):
        """차트 타입에 따라 보여줄 차트 선택"""
        if chart_type == 'Candle':
            self.candlestick_item.show()
            self.line_plot.hide()
        else:
            self.candlestick_item.hide()
            self.line_plot.show()
    
    def apply_styles(self):
        """UI 스타일 적용"""
        # 기본 UI 스타일
        self.apply_ui_styles()
        
        # 차트 스타일 - 기존 효과 중복 방지를 위해 그래픽 효과 제거 먼저 수행
        self.remove_graphics_effects()
        self.apply_chart_styles(self.left_chart_widget)
        
        # 프로그램 이름 설정
        self.program_name.setText("Neon Crypto Trader ✨")
    
    def remove_graphics_effects(self):
        """기존 그래픽 효과 제거 - 중복 방지"""
        # 차트 위젯의 그래픽 효과 제거
        if self.left_chart_widget.graphicsEffect():
            self.left_chart_widget.setGraphicsEffect(None)
            
        # 수익률 차트 위젯의 그래픽 효과 제거
        profit_chart_widget = self.profit_chart.get_widget()
        if profit_chart_widget.graphicsEffect():
            profit_chart_widget.setGraphicsEffect(None)
    
    def apply_ui_styles(self):
        """UI 스타일 적용 - 몽환적인 네온 테마"""
        # 기본 색상 정의
        dark_bg = "#0F0326"  # 매우 어두운 보라색 배경
        neon_pink = "#FF10F0"  # 형광 핑크
        neon_purple = "#B026FF"  # 형광 보라색
        neon_cyan = "#0AFFE6"  # 형광 청록색
        neon_yellow = "#FFFF33"  # 형광 노랑
        
        self.setStyleSheet(f'''
            QMainWindow {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                        stop:0 {dark_bg}, stop:1 #200A40);
                color: #ffffff;
                font-family: "{app_font_name}";
            }}
            
            QLabel, QTableWidget, QPushButton {{
                font-family: "{app_font_name}";
                font-size: 13px;
            }}
            
            QLabel#program_name {{
                font-family: "{app_font_name}";
                font-size: 24px;
                font-weight: bold;
                color: {neon_cyan};
                padding: 5px;
            }}
            
            QHeaderView::section {{
                font-family: "{app_font_name}";
                font-size: 14px;
                font-weight: bold;
            }}
            
            /* 콤보박스 스타일 */
            QComboBox {{
                background-color: {dark_bg};
                color: {neon_cyan};
                border: 2px solid {neon_purple};
                border-radius: 5px;
                padding: 5px;
                min-width: 80px;
                font-weight: bold;
            }}
            
            QComboBox:hover {{
                border: 2px solid {neon_cyan};
            }}
            
            QComboBox::drop-down {{
                border: none;
                background: {neon_purple};
                width: 20px;
            }}
            
            QComboBox QAbstractItemView {{
                background-color: {dark_bg};
                color: {neon_cyan};
                border: 2px solid {neon_purple};
                selection-background-color: {neon_purple};
                selection-color: {neon_cyan};
            }}
            
            /* 시간 표시 라벨 */
            #time_label {{
                color: {neon_cyan};
                font-size: 14px;
                padding: 5px;
                border: 1px solid {neon_pink};
                border-radius: 5px;
                background-color: {dark_bg};
            }}
            
            /* 가격 라벨 */
            #price_label {{
                color: {neon_purple};
                font-size: 18px;
                font-weight: bold;
            }}
            
            /* 오른쪽 상단 위젯 스타일 */
            #right_empty_widget {{
                background-color: {dark_bg};
                border: 2px solid {neon_pink};
                border-radius: 8px;
            }}
        ''')
    
    def apply_chart_styles(self, chart_widget):
        """차트 스타일 통합 적용 - 그래픽 효과 중복 방지"""
        # 네온 스타일 색상
        dark_bg = "#0F0326"
        neon_pink = "#FF10F0"
        neon_purple = "#B026FF"
        neon_cyan = "#0AFFE6"
        
        # 차트 배경색 설정
        chart_widget.setBackground(QColor(dark_bg))
        
        # 차트 축 폰트 설정
        axis_font = QFont(app_font_name, 10)
        
        # 축 색상 및 폰트 설정
        for axis in [chart_widget.getAxis('left'), chart_widget.getAxis('bottom')]:
            axis.setTickFont(axis_font)
            axis.setPen(QColor(neon_pink))
            axis.setTextPen(QColor(neon_cyan))
        
        # 그리드 설정
        grid_color = QColor(neon_purple)
        grid_color.setAlpha(77)  # 30% 투명도
        grid_pen = pg.mkPen(color=grid_color, width=1, style=Qt.DotLine)
        chart_widget.showGrid(x=True, y=True)
        
        # 네온 효과 그림자 추가 (기존 효과가 없는 경우에만)
        if not chart_widget.graphicsEffect():
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(20)
            shadow.setColor(QColor(neon_purple))
            shadow.setOffset(0, 0)
            chart_widget.setGraphicsEffect(shadow)
    
    def apply_modern_ui(self):
        """현대적인 UI 요소 적용 - 그래픽 효과 중복 방지"""
        try:
            # modern_ui 모듈 가져오기
            from modern_ui import (add_price_update_effect, add_smooth_chart_updates, 
                                add_animated_background, add_table_row_animation)
                    
            # 애니메이션 효과 추가 (차트 효과는 제외 - 이미 적용됨)
            add_price_update_effect(self.price_label)  # 가격 변화 시 깜빡임 효과
            add_table_row_animation(self.left_table)  # 테이블 행 추가 애니메이션
            add_animated_background(self)  # 배경 그라데이션 애니메이션
            
            # 오른쪽 상단 위젯에 네온 효과 추가
            right_empty_widget = self.findChild(QWidget, "right_empty_widget")
            if right_empty_widget and not right_empty_widget.graphicsEffect():
                shadow = QGraphicsDropShadowEffect()
                shadow.setBlurRadius(15)
                shadow.setColor(QColor("#FF10F0"))  # 네온 핑크 그림자
                shadow.setOffset(0, 0)
                right_empty_widget.setGraphicsEffect(shadow)
            
            # 차트 관련 모던 UI 효과는 중복 방지를 위해 주석 처리
            # add_smooth_chart_updates(self.left_chart_widget)
            
            # 네온 스타일 적용 - 중복 방지를 위해 modernize_chart 호출 제외
            # 대신 마지막에 overall 스타일만 적용
            apply_matching_neon_style(self)
            
        except Exception as e:
            print(f"현대적 UI 적용 실패: {e}")
            # 기본 스타일 폴백
            self.setStyleSheet(f"""
                QMainWindow {{
                    background-color: #1a1d2d;
                }}
                
                QLabel#program_name {{
                    font-size: 18px;
                    font-weight: bold;
                    color: white;
                    font-family: "{app_font_name}";
                }}
            """)
            
        # 프로그램 이름을 맨 앞으로 가져오기 - 그래픽 효과 적용 후
        self.program_name.raise_()