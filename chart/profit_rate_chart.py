import pyqtgraph as pg
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QSizePolicy
import numpy as np
from datetime import datetime, timedelta

class TotalProfitChart:
    def __init__(self):
        self.chart_widget = self._setup_base_chart()
        self.profit_data = []  # 수익률 데이터 저장 (최근 7일)
        
    def _setup_base_chart(self):
        """차트 기본 설정"""
        chart = pg.PlotWidget()
        chart.setBackground('#2f3b54')
        chart.showGrid(x=True, y=True)
        chart.setMinimumSize(320, 200)
        chart.setMaximumSize(320, 200)
        chart.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        
        # 폰트 설정
        axis_font = QFont('Mosk Normal 400', 10)
        chart.getAxis('left').setTickFont(axis_font)
        chart.getAxis('bottom').setTickFont(axis_font)
        
        # 축 스타일 설정
        chart.getAxis('left').setPen('#4d5b7c')
        chart.getAxis('bottom').setPen('#4d5b7c')
        chart.getAxis('left').setTextPen('#e6e9ef')
        chart.getAxis('bottom').setTextPen('#e6e9ef')
        
        # Y축 레이블 설정
        chart.getAxis('left').setLabel('Total Profit Rate (%)')
        
        # 기준선 (0%) 추가
        chart.addLine(y=0, pen=pg.mkPen(color='#666666', style=pg.QtCore.Qt.DashLine))
        
        return chart
        
    def update_chart(self, total_profit):
        """총 수익률 데이터로 차트 업데이트"""
        # 새로운 수익률 데이터 추가
        self.profit_data.append(total_profit)
        
        # 최근 7일치 데이터만 유지
        if len(self.profit_data) > 7:
            self.profit_data.pop(0)
            
        x = np.arange(len(self.profit_data))
        
        # 날짜 레이블 생성 (최근 7일)
        now = datetime.now()
        dates = []
        for i in range(len(self.profit_data)):
            date = now - timedelta(days=len(self.profit_data)-1-i)
            dates.append(date.strftime('%m-%d'))
            
        # 차트 초기화
        self.chart_widget.clear()
        
        # 기준선 (0%) 다시 추가
        self.chart_widget.addLine(y=0, pen=pg.mkPen(color='#666666', style=pg.QtCore.Qt.DashLine))
        
        # x축 레이블 설정
        axis = self.chart_widget.getAxis('bottom')
        axis.setTicks([[(i, dates[i]) for i in range(len(dates))]])
        
        # 데이터 플로팅
        pen_color = '#4CAF50' if self.profit_data[-1] >= 0 else '#FF5252'
        self.chart_widget.plot(
            x, 
            self.profit_data,
            pen=pg.mkPen(color=pen_color, width=2),  # 양수면 녹색, 음수면 빨간색
            symbol='o',                              # 데이터 포인트 마커
            symbolSize=8,
            symbolBrush=pen_color                    # 마커 색상
        )
        
        # y축 범위 설정 (최소값과 최대값에 여유 추가)
        min_val = min(min(self.profit_data), 0)  # 0 포함
        max_val = max(max(self.profit_data), 0)  # 0 포함
        padding = (max_val - min_val) * 0.1  # 10% 여유
        self.chart_widget.setYRange(min_val - padding, max_val + padding)
    
    def get_widget(self):
        """차트 위젯 반환"""
        return self.chart_widget