import pyqtgraph as pg
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QSizePolicy, QApplication, QMainWindow, QVBoxLayout, QWidget, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt
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
        """차트 기본 설정 - 부드러운 네온 테마 적용"""
        # 부드러운 네온 색상 정의
        dark_bg = "#0F0326"              # 매우 어두운 보라색 배경
        soft_pink = "#AA0A80"            # 부드러운 핑크 테두리 (더 어두움)
        soft_purple = "#5E1387"          # 부드러운 보라색 (더 어두움)
        soft_cyan = "#077A8F"            # 부드러운 청록색 (더 어두움)
        soft_yellow = "#B3AD33"          # 부드러운 노랑색 (더 어두움)
        neon_green = "#39FF14"           # 형광 연두색 (이미 밝아서 그대로 유지)
        
        chart = pg.PlotWidget()
        chart.setBackground(QColor(dark_bg))  # 어두운 보라색 배경
        
        # 그리드 설정 - 부드러운 보라색 점선
        grid_color = QColor(soft_purple)
        grid_color.setAlpha(77)  # 30% 투명도
        grid_pen = pg.mkPen(color=grid_color, width=1, style=Qt.DotLine)
        chart.showGrid(x=True, y=True, alpha=0.3)
        
        chart.setMinimumSize(300, 290)  
        chart.setMaximumSize(300, 290)  
        chart.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  

        chart.hideButtons()  # 버튼 숨기기
        
        # ✅ 폰트 설정 (NanumSquareOTF_acR 적용)
        axis_font = QFont(app_font_name, 8)
        chart.getAxis('left').setTickFont(axis_font)
        chart.getAxis('bottom').setTickFont(axis_font)

        # ✅ 축 스타일 설정 - 부드러운 색상 적용
        chart.getAxis('left').setPen(pg.mkPen(color=soft_pink, width=2))
        chart.getAxis('bottom').setPen(pg.mkPen(color=soft_pink, width=2))
        chart.getAxis('left').setTextPen(soft_cyan)
        chart.getAxis('bottom').setTextPen(soft_cyan)

        chart.getAxis('left').setWidth(30)  
        chart.getAxis('left').setStyle(showValues=True, tickTextOffset=2)

        chart.getAxis('left').setLabel('')  # Y축 레이블 제거
        
        # ✅ 타이틀 적용 - 부드러운 노랑으로 변경
        title_style = {'color': soft_yellow, 'size': '10pt', 'bold': True}
        chart.setTitle("전체 수익률 (%)", **title_style)

        # ✅ 기준선 (0%) 추가 - 부드러운 보라색 대시 라인
        chart.addLine(y=0, pen=pg.mkPen(color=soft_purple, width=1.5, style=Qt.DashLine))

        chart.getAxis('bottom').setStyle(tickLength=3)  
        chart.getAxis('bottom').setHeight(20)  

        chart.getViewBox().setDefaultPadding(0.03)  
        chart.setContentsMargins(1, 1, 1, 1)  
        
        # 부드러운 네온 효과 추가
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(15)  # 조금 더 부드럽게
        glow.setColor(QColor(soft_purple))
        glow.setOffset(0, 0)
        chart.setGraphicsEffect(glow)
        
        # 테두리 설정 - 부드러운 핑크
        chart.setStyleSheet(f'''
            border: 2px solid {soft_pink};
            border-radius: 10px;
        ''')

        return chart

    def update_display(self):
        """✅ 꺾은선 그래프로 수익률 표시 - 형광색으로 업데이트"""
        if not self.daily_total_profits:
            return

        self.chart_widget.clear()
        
        # 네온 색상 정의
        neon_green = "#39FF14"   # 형광 연두색
        neon_red = "#FF2D2D"     # 형광 빨간색
        neon_purple = "#B026FF"  # 형광 보라색
        
        # 기준선 (0%) 다시 추가
        self.chart_widget.addLine(y=0, pen=pg.mkPen(color=neon_purple, width=1.5, style=Qt.DashLine))

        x = np.arange(len(self.daily_total_profits))
        profits = [data[1] for data in self.daily_total_profits]

        # ✅ X축 날짜 라벨 설정
        dates = [data[0] for data in self.daily_total_profits]
        self.chart_widget.getAxis('bottom').setTicks([list(enumerate(dates))])

        # ✅ Y축 범위 자동 조정
        min_val = min(profits) * 1.2 if min(profits) < 0 else -5
        max_val = max(profits) * 1.2 if profits else 10
        self.chart_widget.setYRange(min_val, max_val, padding=0.1)

        # ✅ 꺾은선 그래프 그리기 - 형광색 적용
        line_pen = pg.mkPen(color=neon_green, width=2)    # 형광 연두색 (상승)
        line_pen_red = pg.mkPen(color=neon_red, width=2)  # 형광 빨간색 (하락)

        for i in range(len(profits) - 1):
            current_profit = profits[i]
            next_profit = profits[i + 1]

            pen = line_pen if next_profit >= current_profit else line_pen_red

            self.chart_widget.plot(
                [x[i], x[i + 1]], [current_profit, next_profit],
                pen=pen, antialias=True
            )

        # ✅ 마커 & 텍스트 추가 - 형광색 적용
        offset = max_val * 0.03  
        for i, profit in enumerate(profits):
            marker_color = neon_green if profit >= 0 else neon_red

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

            # ✅ NanumSquareOTF_acR 폰트 적용 & 색상 변경
            text_color = neon_green if profit >= 0 else neon_red
            text_item = pg.TextItem(
                text=f'{profit:+.1f}%',
                color=text_color,
                anchor=(0.5, anchor_y)
            )
            text_item.setFont(QFont(app_font_name, 9))
            text_item.setPos(i, text_y)
            self.chart_widget.addItem(text_item)

    def get_widget(self):
        """차트 위젯 반환"""
        return self.chart_widget