from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
    QTableWidgetItem, QLabel, QComboBox, QHeaderView, QSizePolicy, QSplitter
)
from PyQt5.QtCore import Qt, QTimer, QEvent  
from PyQt5.QtGui import QColor, QFontDatabase,QFont
import pyqtgraph as pg
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta
import os
from datetime import datetime, timedelta

# 차트 관련 클래스들 임포트
from chart.candlestick import CandlestickItem
from chart.trade_marker import TradeMarker
from data.data_fetcher import DataFetcher
from utils.naver_time import NaverTimeFetcher
from chart.profit_rate_chart import TotalProfitChart
from ui.components.trade_history_table import TradeHistoryTable
from ui.components.profit_rate_table import ProfitRateTable

class TradingView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Trading Platform')
        self.total_profit_rate = 0.0
        
        # 기본 설정
        self.load_custom_fonts()
        self.setGeometry(200, 200, 1280, 720)
        
        # 컴포넌트 초기화
        self.profit_chart = TotalProfitChart()
        self.data_fetcher = DataFetcher()
        self.trades = []
        self.open_positions = {}

        # UI 설정
        self.setup_ui()
        self.setup_focus_policy()
        
        # 타이머 설정
        self.setup_timers()

    def setup_timers(self):
        """모든 타이머 설정"""
        # 차트 데이터 업데이트 (1분)
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_data)
        self.update_timer.start(60000)
        
        # 시간 표시 업데이트 (1초)
        self.time_timer = QTimer()
        self.time_timer.timeout.connect(self.update_time)
        self.time_timer.start(1000)
    
    def setup_chart_styles(self):
        """차트 스타일 설정"""
        # 차트 축 폰트 설정
        axis_font = QFont('Mosk Normal 400', 10)
        for axis in [self.left_chart_widget.getAxis('left'), 
                    self.left_chart_widget.getAxis('bottom')]:
            axis.setTickFont(axis_font)
            axis.setPen('#4d5b7c')
            axis.setTextPen('#e6e9ef')
        
        # 차트 배경 설정
        self.left_chart_widget.setBackground('#2f3b54')
        self.left_chart_widget.showGrid(x=True, y=True, alpha=0.3)
        
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

    def load_custom_fonts(self):
        """커스텀 폰트 로드"""
        fonts_dir = os.path.join('assets', 'fonts')
        font_families = []
        
        # 폰트 파일들을 QFontDatabase에 등록
        for font_file in os.listdir(fonts_dir):
            if font_file.endswith('.ttf'):
                font_path = os.path.join(fonts_dir, font_file)
                font_id = QFontDatabase.addApplicationFont(font_path)
                if font_id != -1:
                    font_families.extend(QFontDatabase.applicationFontFamilies(font_id))
                    
    def setup_ui(self):
        # 메인 윈도우 설정
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # 1. 프로그램 이름
        program_name = QHBoxLayout()
        self.program_name = QLabel('Program Name')
        self.program_name.setStyleSheet('font-size: 16px; font-weight: bold; color: white;')
        program_name.addWidget(self.program_name)
        main_layout.addLayout(program_name)

        # 프로그램 메인 레이아웃
        body_layout = QHBoxLayout()
        main_layout.addLayout(body_layout)

        # 왼쪽 레이아웃
        left_layout = QVBoxLayout()
        body_layout.addLayout(left_layout)

        # 1. 상단 정보 섹션
        left_top_info = QHBoxLayout()
        self.price_label = QLabel()  # 현재가 표시 라벨
        self.price_label.setStyleSheet('font-size: 16px; font-weight: bold; color: white;')

        # 2. 차트 타입 선택 콤보박스 (캔들/라인)
        self.chart_type = QComboBox()
        self.chart_type.addItems(['Candle', 'Line'])
        self.chart_type.setStyleSheet('background-color: #2a2f3a; color: white; padding: 5px;')
        self.chart_type.currentTextChanged.connect(self.update_chart)

        # 네이버 시간 표시 라벨 추가
        self.time_label = QLabel()
        self.time_label.setStyleSheet('''
            color: #e6e9ef;
            font-family: 'Mosk Normal 400';
            font-size: 14px;
            padding: 5px;
        ''')

        left_top_info.addWidget(self.price_label)
        left_top_info.addWidget(self.chart_type)
        left_top_info.addStretch()  # 왼쪽 요소들과 시간 사이 공간
        left_top_info.addWidget(self.time_label)
        left_layout.addLayout(left_top_info)

        # 2. 차트 영역 설정
        self.left_chart_widget = pg.PlotWidget()
        self.left_chart_widget.setBackground('black')
        self.left_chart_widget.showGrid(x=True, y=True)

        # 2. 캔들스틱과 라인차트 아이템 생성
        self.candlestick_item = CandlestickItem()
        self.left_chart_widget.addItem(self.candlestick_item)

        self.line_plot = None
        self.trade_markers = TradeMarker()  # 매매 표시 마커
        self.left_chart_widget.addItem(self.trade_markers)

        left_layout.addWidget(self.left_chart_widget)

        # 3. 거래 기록 테이블
        self.left_table = TradeHistoryTable()
        left_layout.addWidget(self.left_table)

        # 테스트용으로 데이터 넣어보기
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

        # 오른쪽 레이아웃
        right_layout = QVBoxLayout()
        body_layout.addLayout(right_layout)

        # 4. 오른쪽 빈 공간
        right_empty_widget = QWidget()
        right_empty_widget.setMinimumWidth(320)
        right_empty_widget.setMaximumSize(320, 150)
        right_empty_widget.setStyleSheet('background-color: #1e222d;')
        right_layout.addWidget(right_empty_widget, stretch=1)

        # 5. 오른쪽 차트 영역
        right_chart_widget = self.profit_chart.get_widget()
        right_layout.addWidget(right_chart_widget)

        #수익률 차트 테스트 데이터
        base_date = datetime.now()
        dates = [(base_date - timedelta(days=i)).strftime('%m/%d') for i in range(6, -1, -1)]
        test_data = [10.5, 15.2, -54.3, 8.7, 12.1, -3.2, 1055.5]
        for date, profit in zip(dates, test_data):
            self.profit_chart.daily_total_profits.append((date, profit))
        self.profit_chart.update_display()

        # 6. 오른쪽 수익률 표시 영역
        self.right_table = ProfitRateTable()
        right_layout.addWidget(self.right_table)
        
        #수익률 표 테스트용 데이터
        test_profit_data = {
            'my_rate': -5.2,
            'daily': 1.5,
            'weekly': 4.2,
            'monthly': 15.7,
            'yearly': 45.2,
            'total': -25.5
        }
        self.right_table.update_profit_rates(test_profit_data)

        self.apply_styles()  # UI 스타일 적용
        self.update_data()   # 초기 데이터 로드

    def setup_data_update_timer(self):
        # 1분마다 데이터 자동 업데이트
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_data)
        self.update_timer.start(1000)  # 60초마다
        
    def update_data(self):
        # 현재가 업데이트
        current_price = self.data_fetcher.get_current_price()
        if current_price:
            self.price_label.setText(f'BTC/USDT: {current_price:,.1f}')

        # 차트 데이터 업데이트
        candle_data, df = self.data_fetcher.fetch_ohlcv(timeframe='1h', limit=100)
        if candle_data is not None:
            # 캔들스틱 데이터 설정
            self.candlestick_item.set_data(candle_data)
            
            # 라인차트 데이터 갱신
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
            self.line_plot.hide()  # 기본적으로 라인차트 숨김
    
    def update_time(self):
        """네이버 서버 시간을 가져와서 업데이트"""
        kr_time = NaverTimeFetcher.get_naver_time()
        weekday = ['월', '화', '수', '목', '금', '토', '일'][kr_time.weekday()]
        time_str = kr_time.strftime(f'%Y-%m-%d({weekday}) %H:%M:%S')
        self.time_label.setText(time_str)

    def update_chart(self, chart_type):
        # 차트 타입에 따라 보여줄 차트 선택
        if chart_type == 'Candle':
            self.candlestick_item.show()
            self.line_plot.hide()
        else:
            self.candlestick_item.hide()
            self.line_plot.show()

    def apply_chart_styles(self, chart_widget):
        """차트 위젯에 공통 스타일 적용"""
        # 차트 축 폰트 설정
        axis_font = QFont('Mosk Normal 400', 10)
        chart_widget.getAxis('left').setTickFont(axis_font)
        chart_widget.getAxis('bottom').setTickFont(axis_font)
        
        # 차트 배경 및 그리드 색상 설정
        chart_widget.setBackground('#2f3b54')
        chart_widget.getAxis('left').setPen('#4d5b7c')
        chart_widget.getAxis('bottom').setPen('#4d5b7c')
        chart_widget.getAxis('left').setTextPen('#e6e9ef')
        chart_widget.getAxis('bottom').setTextPen('#e6e9ef')

    def apply_styles(self):
        """UI 스타일 적용"""
        self.setStyleSheet('''
            QMainWindow {
                background-color: #2a3447;
                color: #ffffff;
                font-family: 'Mosk Normal 400';
            }
            QComboBox {
                background-color: #3d4760;
                color: #ffffff;
                padding: 5px;
                border: 1px solid #4d5b7c;
                font-family: 'Mosk Normal 400';
                font-size: 13px;
            }
            QComboBox:hover {
                background-color: #4d5b7c;
            }
            QLabel {
                color: #e6e9ef;
                font-family: 'Mosk Normal 400';
                font-size: 13px;
            }
            QLabel#program_name {
                font-family: 'Mosk Bold 700';
                font-size: 16px;
            }
        ''')
        
        # 차트 축 폰트 설정
        axis_font = QFont('Mosk Normal 400', 10)
        self.left_chart_widget.getAxis('left').setTickFont(axis_font)
        self.left_chart_widget.getAxis('bottom').setTickFont(axis_font)
        
        # 차트 배경 및 그리드 색상 설정
        self.left_chart_widget.setBackground('#2f3b54')
        self.left_chart_widget.getAxis('left').setPen('#4d5b7c')
        self.left_chart_widget.getAxis('bottom').setPen('#4d5b7c')
        self.left_chart_widget.getAxis('left').setTextPen('#e6e9ef')
        self.left_chart_widget.getAxis('bottom').setTextPen('#e6e9ef')
        
        # 차트 축 폰트 설정
        axis_font = QFont('Mosk Normal 400', 10)
        self.left_chart_widget.getAxis('left').setTickFont(axis_font)
        self.left_chart_widget.getAxis('bottom').setTickFont(axis_font)
        
        # 차트 배경 및 그리드 색상 설정
        self.left_chart_widget.setBackground('#2f3b54')
        self.left_chart_widget.getAxis('left').setPen('#4d5b7c')
        self.left_chart_widget.getAxis('bottom').setPen('#4d5b7c')
        self.left_chart_widget.getAxis('left').setTextPen('#e6e9ef')
        self.left_chart_widget.getAxis('bottom').setTextPen('#e6e9ef')
