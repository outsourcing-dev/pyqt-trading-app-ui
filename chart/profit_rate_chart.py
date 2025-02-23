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
        chart.getAxis('bottom').setStyle(tickLength=0)  # tick 선 제거
        
        return chart

    def update_display(self):
        """차트 표시 업데이트"""
        if not self.daily_total_profits:  # 데이터가 없으면 종료
            return
            
        # 차트 초기화
        self.chart_widget.clear()
        
        # 기준선 (0%) 다시 추가
        self.chart_widget.addLine(y=0, pen=pg.mkPen(color='#666666', style=pg.QtCore.Qt.DashLine))
        
        # 데이터 준비
        dates = [data[0] for data in self.daily_total_profits]
        profits = [data[1] for data in self.daily_total_profits]
        x = np.arange(len(dates))
        
        # x축 날짜 레이블 설정
        bottom_axis = self.chart_widget.getAxis('bottom')
        bottom_axis.setTicks([[(i, dates[i]) for i in range(len(dates)) if i % 2 == 0]])  # 2일 간격으로 표시
        
        # y축 범위 설정
        min_val = min(min(profits), 0)
        max_val = max(max(profits), 0)
        value_range = max_val - min_val
        padding = value_range * 0.2  # 20% 여유
        
        # 최소 범위 설정
        if value_range < 10:
            padding = 5  # 최소 ±5% 범위
            
        self.chart_widget.setYRange(min_val - padding, max_val + padding)
        
        # x축 범위 설정
        self.chart_widget.setXRange(-0.5, len(dates) - 0.5)
        
        # 선 그리기
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
            
            # 데이터 포인트 (원) 그리기
            self.chart_widget.plot(
                [i],
                [profits[i]],
                pen=None,
                symbol='o',
                symbolSize=8,
                symbolBrush='#4CAF50' if profits[i] >= 0 else '#FF5252'
            )
            
            # 수익률 텍스트 추가
            text_item = pg.TextItem(
                text=f'{profits[i]:+.1f}%',
                color='#ffffff',
                anchor=(0.5, 1) if profits[i] >= 0 else (0.5, 0)
            )
            text_item.setPos(i, profits[i])
            self.chart_widget.addItem(text_item)
    
    def get_widget(self):
        """차트 위젯 반환"""
        return self.chart_widget

    @classmethod
    def demo_basic_usage(cls):
        """기본 사용법 데모"""
        class DemoWindow(QMainWindow):
            def __init__(self):
                super().__init__()
                self.setWindowTitle('Profit Chart Demo')
                self.setGeometry(100, 100, 400, 300)
                
                # 메인 위젯 설정
                main_widget = QWidget()
                self.setCentralWidget(main_widget)
                layout = QVBoxLayout(main_widget)
                
                # 차트 생성 및 추가
                self.chart = TotalProfitChart()
                layout.addWidget(self.chart.get_widget())
                
                # 테스트를 위한 날짜 생성 (오늘부터 7일 전까지)
                base_date = datetime.now()
                dates = [(base_date - timedelta(days=i)).strftime('%m/%d') for i in range(6, -1, -1)]
                
                # 데모 데이터 추가
                test_data = [10.5, 15.2, -5.3, 8.7, 12.1, -3.2, 20.5]
                
                # 날짜와 수익률을 함께 업데이트
                for date, profit in zip(dates, test_data):
                    self.chart.daily_total_profits.append((date, profit))
                
                # 차트 업데이트
                self.chart.update_display()
        
        app = QApplication(sys.argv)
        window = DemoWindow()
        window.show()
        sys.exit(app.exec_())

if __name__ == '__main__':
    TotalProfitChart.demo_basic_usage()