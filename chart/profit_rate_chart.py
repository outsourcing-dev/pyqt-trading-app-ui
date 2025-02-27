import pyqtgraph as pg
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QSizePolicy, QApplication, QMainWindow, QVBoxLayout, QWidget
import numpy as np
from datetime import datetime, timedelta
import sys

# ✅ NanumSquareOTF_acR 폰트 적용
app_font_name = "NanumSquareOTF_acR"

class TotalProfitChart:
    def __init__(self):
        self.chart_widget = self._setup_base_chart()
        self.daily_total_profits = []  # [(날짜, 수익률)] 형태로 저장
        
    def _setup_base_chart(self):
        """차트 기본 설정"""
        chart = pg.PlotWidget()
        chart.setBackground('#2f3b54')
        chart.showGrid(x=True, y=True, alpha=0.3)  # 그리드 투명도 추가
        chart.setMinimumSize(300, 290)  
        chart.setMaximumSize(300, 290)  
        chart.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  

        chart.hideButtons()  # 버튼 숨기기
        
        # ✅ 폰트 설정 (NanumSquareOTF_acR 적용)
        axis_font = QFont(app_font_name, 8)
        chart.getAxis('left').setTickFont(axis_font)
        chart.getAxis('bottom').setTickFont(axis_font)

        # ✅ 축 스타일 설정
        chart.getAxis('left').setPen(pg.mkPen(color='#4d5b7c', width=1))
        chart.getAxis('bottom').setPen(pg.mkPen(color='#4d5b7c', width=1))
        chart.getAxis('left').setTextPen('#e6e9ef')
        chart.getAxis('bottom').setTextPen('#e6e9ef')

        chart.getAxis('left').setWidth(30)  
        chart.getAxis('left').setStyle(showValues=True, tickTextOffset=2)

        chart.getAxis('left').setLabel('')  # Y축 레이블 제거
        
        # ✅ 타이틀 적용
        title_style = {'color': '#e6e9ef', 'size': '10pt', 'bold': True}
        chart.setTitle("전체 수익률 (%)", **title_style)

        # ✅ 기준선 (0%) 추가
        chart.addLine(y=0, pen=pg.mkPen(color='#666666', width=1.5, style=pg.QtCore.Qt.DashLine))

        chart.getAxis('bottom').setStyle(tickLength=3)  
        chart.getAxis('bottom').setHeight(20)  

        chart.getViewBox().setDefaultPadding(0.03)  
        chart.setContentsMargins(1, 1, 1, 1)  

        return chart

    def update_display(self):
        """✅ 꺾은선 그래프로 수익률 표시"""
        if not self.daily_total_profits:
            return

        self.chart_widget.clear()

        x = np.arange(len(self.daily_total_profits))
        profits = [data[1] for data in self.daily_total_profits]

        # ✅ X축 날짜 라벨 설정
        dates = [data[0] for data in self.daily_total_profits]
        self.chart_widget.getAxis('bottom').setTicks([list(enumerate(dates))])

        # ✅ Y축 범위 자동 조정
        min_val = min(profits) * 1.2 if profits else 0
        max_val = max(profits) * 1.2 if profits else 10
        self.chart_widget.setYRange(min_val, max_val, padding=0.1)

        # ✅ 꺾은선 그래프 그리기
        line_pen = pg.mkPen(color="#4CAF50", width=2)  # 초록색 (상승)
        line_pen_red = pg.mkPen(color="#FF5252", width=2)  # 빨간색 (하락)

        for i in range(len(profits) - 1):
            current_profit = profits[i]
            next_profit = profits[i + 1]

            pen = line_pen if next_profit >= current_profit else line_pen_red

            self.chart_widget.plot(
                [x[i], x[i + 1]], [current_profit, next_profit],
                pen=pen, antialias=True
            )

        # ✅ 마커 & 텍스트 추가
        offset = max_val * 0.03  
        for i, profit in enumerate(profits):
            marker_color = "#4CAF50" if profit >= 0 else "#FF5252"

            # 마커 추가 (동그라미)
            self.chart_widget.plot(
                [i], [profit],
                pen=pg.mkPen('#FFFFFF', width=0.5),
                symbol='o',
                symbolSize=5,
                symbolBrush=marker_color,
                symbolPen=pg.mkPen('#FFFFFF', width=0.5)
            )

            # ✅ 위/아래 정렬 유지
            text_y = profit + offset if profit >= 0 else profit - offset
            anchor_y = 1 if profit >= 0 else 0

            # ✅ NanumSquareOTF_acR 폰트 적용 & 박스 제거
            text_item = pg.TextItem(
                text=f'{profit:+.1f}%',
                color='#FFFFFF',
                anchor=(0.5, anchor_y)
            )
            text_item.setFont(QFont(app_font_name, 9))  # ✅ NanumSquareOTF_acR 적용
            text_item.setPos(i, text_y)
            self.chart_widget.addItem(text_item)

    def get_widget(self):
        """차트 위젯 반환"""
        return self.chart_widget
