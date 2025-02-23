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

# 차트 관련 클래스들 임포트
from chart.candlestick import CandlestickItem
from chart.trade_marker import TradeMarker
from data.data_fetcher import DataFetcher
from utils.naver_time import NaverTimeFetcher
from chart.profit_rate_chart import TotalProfitChart

class TradingView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Trading Platform')

        #폰트 로드
        self.load_custom_fonts()

        # 윈도우 크기 설정 (16:9 비율인 1280x720 크기)
        self.setGeometry(200, 200, 1280, 720)
        
        self.profit_chart = TotalProfitChart()  # 차트 인스턴스 생성

        # 데이터 가져오기 객체와 거래 기록 초기화
        self.data_fetcher = DataFetcher()
        self.trades = []  # 전체 거래 기록
        self.open_positions = {}  # 현재 열린 포지션 추적

        self.setup_ui()  # UI 구성 함수 호출
        self.setup_focus_policy()  # 포커스 정책 설정 추가

        self.setup_data_update_timer()  # 데이터 자동 업데이트 타이머 설정
        
        # 시간 업데이트 타이머 설정
        self.time_timer = QTimer()
        self.time_timer.timeout.connect(self.update_time)
        self.time_timer.start(1000)  # 1초마다 업데이트
        

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

        # 본체 레이아웃
        body_layout = QHBoxLayout()
        main_layout.addLayout(body_layout)

        # 왼쪽 레이아웃
        left_layout = QVBoxLayout()
        body_layout.addLayout(left_layout)

        # 2. 상단 정보 섹션
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
        row_count = 1
        self.left_table = QTableWidget(row_count, 5)
        self.left_table.setHorizontalHeaderLabels([
            'Coin Name', 'Quantity', 'Liquidation Price', 'Unrealized P/L (Profit Rate)', 'Realized P/L'
        ])
        self.left_table.setVerticalHeaderLabels([''])
        self.left_table.setStyleSheet('background-color: #1e222d; color: white;')
        self.left_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.left_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        left_layout.addWidget(self.left_table)

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
        # now = datetime.datetime.now()
        # y = np.array([1, 2, 3, 4])  # numpy 배열로 변환
        # x = np.array(range(len(y)))  # x축도 numpy 배열로 생성

        # # 날짜 레이블용 문자열 배열 따로 생성
        # date_labels = []
        # for i in range(len(y)):
        #     date = now - relativedelta(days=i)
        #     date_labels.append(date.strftime('%m-%d'))
        # date_labels.reverse()

        # right_chart_widget = pg.PlotWidget()
        # right_chart_widget.setBackground('BLACK')
        # right_chart_widget.showGrid(x=True, y=True)
        # right_chart_widget.setMinimumSize(320, 200)
        # right_chart_widget.setMaximumSize(320, 200)
        # right_chart_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        # # x축 눈금 레이블 설정
        # axis = right_chart_widget.getAxis('bottom')
        # axis.setTicks([[(i, date_labels[i]) for i in range(len(date_labels))]])

        # # 숫자 배열로 플롯
        # right_chart_widget.plot(x, y)
        # right_layout.addWidget(right_chart_widget)

        # 6. 오른쪽 수익률 표시 영역
        self.right_table = QTableWidget(6, 1)
        self.right_table.setMinimumWidth(320)
        self.right_table.setMaximumWidth(320)
        self.right_table.setHorizontalHeaderLabels([''])
        self.right_table.setVerticalHeaderLabels(['My Profit Rate', 'Daily', 'Weekly', 'Monthly', 'Yearly', 'Total Profit Rate'])
        self.right_table.setStyleSheet('background-color: #1e222d; color: white;')
        self.right_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.right_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.right_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        right_layout.addWidget(self.right_table)

        self.apply_styles()  # UI 스타일 적용
        self.update_data()   # 초기 데이터 로드

    def setup_data_update_timer(self):
        # 1분마다 데이터 자동 업데이트
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_data)
        self.update_timer.start(60000)  # 60초마다

    def update_data(self):
        # 현재가 업데이트
        current_price = self.data_fetcher.get_current_price()
        if current_price:
            self.price_label.setText(f'BTC/USDT: {current_price:,.1f}')

        # 차트 데이터 업데이트
        candle_data, df = self.data_fetcher.fetch_ohlcv()
        if candle_data is not None:
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
            self.line_plot.hide()  # 기본적으로 라인차트 숨김
    
    def update_time(self):
        """네이버 서버 시간을 가져와서 업데이트"""
        kr_time = NaverTimeFetcher.get_naver_time()
        weekday = ['월', '화', '수', '목', '금', '토', '일'][kr_time.weekday()]
        time_str = kr_time.strftime(f'%Y-%m-%d({weekday}) %H:%M:%S')
        self.time_label.setText(time_str)

    def update_chart(self, chart_type):
        # 차트 타입에 따라 보여줄 차트 선택
        if chart_type == '캔들스틱':
            self.candlestick_item.show()
            self.line_plot.hide()
        else:
            self.candlestick_item.hide()
            self.line_plot.show()

    def apply_styles(self):
        # 전체적인 UI 스타일 적용
        self.setStyleSheet('''
            QMainWindow {
                background-color: #2a3447;
                color: #ffffff;
                font-family: 'Mosk Normal 400';
            }
            QTableWidget {
                gridline-color: #3d4760;
                border: none;
                background-color: #2f3b54;
                font-family: 'Mosk Normal 400';
                font-size: 13px;
            }
            QTableWidget::item {
                padding: 5px;
                color: #e6e9ef;
            }
            /* 선택된 셀의 스타일 통일 */
            QTableWidget::item:selected {
                background-color: #3d4760;
                color: #ffffff;
            }
            /* 포커스되지 않은 선택 셀의 스타일도 통일 */
            QTableWidget::item:selected:!active {
                background-color: #3d4760;
                color: #ffffff;
            }
            QHeaderView::section {
                background-color: #3d4760;
                color: #ffffff;
                padding: 5px;
                border: 1px solid #2a3447;
                font-family: 'Mosk Medium 500';
                font-size: 14px;
            }
            QTableCornerButton::section {
                background-color: #3d4760;
                border: 1px solid #2a3447;
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
