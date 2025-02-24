import pyqtgraph as pg
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QSizePolicy, QApplication, QMainWindow, QVBoxLayout, QWidget
import numpy as np
from datetime import datetime, timedelta
import sys

class TotalProfitChart:
    def __init__(self):
        self.chart_widget = self._setup_base_chart()
        self.daily_total_profits = []  # [(날짜, 수익률)] 형태로 저장
        
    def _setup_base_chart(self):
        """차트 기본 설정"""
        chart = pg.PlotWidget()
        chart.setBackground('#2f3b54')
        chart.showGrid(x=True, y=True)
        chart.setMinimumSize(320, 300)
        chart.setMaximumSize(320, 300)
        chart.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        
        # 버튼 숨기기
        chart.hideButtons()
        
        # 폰트 설정
        axis_font = QFont('Mosk Normal 400', 8)
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
        
        # x축 스타일 설정
        chart.getAxis('bottom').setStyle(tickLength=0)
        
        return chart

    def update_display(self):
        """차트 표시 업데이트"""
        if not self.daily_total_profits:
            return
            
        self.chart_widget.clear()
        self.chart_widget.addLine(y=0, pen=pg.mkPen(color='#666666', style=pg.QtCore.Qt.DashLine))
        
        dates = [data[0] for data in self.daily_total_profits]
        profits = [data[1] for data in self.daily_total_profits]
        x = np.arange(len(dates))
        
        bottom_axis = self.chart_widget.getAxis('bottom')
        bottom_axis.setTicks([[(i, dates[i]) for i in range(len(dates)) if i % 2 == 0]])
        
        # 데이터 플롯
        for i in range(len(profits)):
            if i > 0:
                prev_profit = profits[i-1]
                current_profit = profits[i]
                color = '#4CAF50' if current_profit >= prev_profit else '#FF5252'
                self.chart_widget.plot(
                    [i-1, i],
                    [prev_profit, current_profit],
                    pen=pg.mkPen(color=color, width=2)
                )
            
            self.chart_widget.plot(
                [i],
                [profits[i]],
                pen=None,
                symbol='o',
                symbolSize=8,
                symbolBrush='#4CAF50' if profits[i] >= 0 else '#FF5252'
            )
            
            text_item = pg.TextItem(
                text=f'{profits[i]:+.1f}%',
                color='#ffffff',
                anchor=(0.5, 1) if profits[i] >= 0 else (0.5, 0)
            )
            text_item.setPos(i, profits[i])
            self.chart_widget.addItem(text_item)

        # 자동 범위 설정 (패딩 포함)
        min_val = min(min(profits), 0)
        max_val = max(max(profits), 0)
        value_range = max_val - min_val
        padding = max(value_range * 0.2, 5)  # 최소 5% 패딩
        
        self.chart_widget.setYRange(min_val - padding, max_val + padding, padding=0)
        self.chart_widget.setXRange(-0.5, len(dates) - 0.5, padding=0)
        
        # ViewBox 설정으로 자동 범위 조정 활성화
        self.chart_widget.getViewBox().enableAutoRange()
    
    def get_widget(self):
        """차트 위젯 반환"""
        return self.chart_widget