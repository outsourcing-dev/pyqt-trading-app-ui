import pyqtgraph as pg
from PyQt5.QtGui import QPainter,QColor, QFont
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt
\

class CandlestickItem(pg.GraphicsObject):
    def __init__(self):
        pg.GraphicsObject.__init__(self)
        self.picture = None
        self.data = None
        self.time_axis = None

    def set_data(self, data, timestamps=None):
        """
        캔들스틱 차트의 데이터를 설정합니다
        Args:
            data: [시간, 시가, 고가, 저가, 종가] 배열
            timestamps: 시간 데이터 배열
        """
        self.data = data
        self.time_axis = timestamps
        self.generate_picture()
        self.informViewBoundsChanged()

    def generate_picture(self):
        if self.data is None:
            return

        # 봉의 너비 설정 (시간 간격의 60%)
        w = 0.6
        self.picture = pg.QtGui.QPicture()
        p = QPainter(self.picture)

        for i, (t, open, high, low, close) in enumerate(self.data):
            if close >= open:
                p.setBrush(pg.mkBrush('g'))
                p.setPen(pg.mkPen('g'))
            else:
                p.setBrush(pg.mkBrush('r'))
                p.setPen(pg.mkPen('r'))

            p.drawLine(pg.QtCore.QPointF(i, low), pg.QtCore.QPointF(i, high))
            p.drawRect(pg.QtCore.QRectF(i - w/2, open, w, close - open))

        p.end()

    def paint(self, p, *args):
        # 캔들스틱 실제로 화면에 그리기
        if self.picture is not None:
            self.picture.play(p)

    def boundingRect(self):
        # 그래프 영역 계산
        # 데이터 없으면 빈 영역 반환
        if self.data is None:
            return pg.QtCore.QRectF()
        # 전체 데이터 범위에 맞게 영역 계산해서 반환
        return pg.QtCore.QRectF(
            self.data[:, 0].min(),
            self.data[:, 3].min(),
            self.data[:, 0].max() - self.data[:, 0].min(),
            self.data[:, 2].max() - self.data[:, 3].min()
        )

def apply_matching_neon_style(trading_view):
    """수익률 차트와 동일한 네온 스타일을 캔들스틱 차트에 적용 - 부드러운 테두리"""
    
    # 전역 app_font_name을 가져오기 시도
    try:
        # 모듈에서 가져오기 시도
        from ui.trading_view import app_font_name
    except ImportError:
        # 가져오기 실패 시 기본값 사용
        app_font_name = "NanumSquareOTF_acR"  
    
    # 소프트한 네온 색상 정의 (더 어둡고 덜 눈아픈 버전)
    dark_bg = "#0F0326"              # 매우 어두운 보라색 배경
    soft_pink = "#AA0A80"            # 부드러운 핑크 테두리 (더 어두움)
    soft_purple = "#5E1387"          # 부드러운 보라색 (더 어두움)
    soft_cyan = "#077A8F"            # 부드러운 청록색 (더 어두움)
    soft_yellow = "#B3AD33"          # 부드러운 노랑색 (더 어두움)
    
    # 캔들스틱 차트 스타일 설정
    trading_view.left_chart_widget.setBackground(QColor(dark_bg))
    
    # 축 스타일 설정 - 부드러운 색상으로 변경
    trading_view.left_chart_widget.getAxis('left').setPen(pg.mkPen(color=soft_pink, width=2))
    trading_view.left_chart_widget.getAxis('bottom').setPen(pg.mkPen(color=soft_pink, width=2))
    trading_view.left_chart_widget.getAxis('left').setTextPen(soft_cyan)
    trading_view.left_chart_widget.getAxis('bottom').setTextPen(soft_cyan)
    
    # 축 라벨 폰트 설정
    axis_font = QFont(app_font_name, 8)
    trading_view.left_chart_widget.getAxis('left').setTickFont(axis_font)
    trading_view.left_chart_widget.getAxis('bottom').setTickFont(axis_font)
    
    # 그리드 설정 - 부드러운 보라색 점선
    grid_color = QColor(soft_purple)
    grid_color.setAlpha(77)  # 30% 투명도
    grid_pen = pg.mkPen(color=grid_color, width=1, style=Qt.DotLine)
    trading_view.left_chart_widget.showGrid(x=True, y=True, alpha=0.3)
    
    # 테두리 설정 - 더 부드러운 색상과 투명도 적용
    trading_view.left_chart_widget.setStyleSheet(f'''
        border: 2px solid {soft_pink};
        border-radius: 10px;
    ''')
    
    # 부드러운 네온 효과 추가 - 더 낮은 블러와 더 낮은 투명도
    glow = QGraphicsDropShadowEffect()
    glow.setBlurRadius(15)  # 블러 줄임
    glow.setColor(QColor(soft_purple))
    glow.setOffset(0, 0)
    trading_view.left_chart_widget.setGraphicsEffect(glow)

# TotalProfitChart에도 같은 스타일 적용하는 함수
def apply_soft_neon_to_profit_chart(profit_chart):
    """수익률 차트에 부드러운 네온 스타일 적용"""
    from PyQt5.QtGui import QColor, QFont, QGraphicsDropShadowEffect
    from PyQt5.QtCore import Qt
    import pyqtgraph as pg
    
    # 전역 app_font_name 기본값
    app_font_name = "NanumSquareOTF_acR"
    
    # 소프트한 네온 색상 정의
    dark_bg = "#0F0326"              # 매우 어두운 보라색 배경
    soft_pink = "#AA0A80"            # 부드러운 핑크 테두리
    soft_purple = "#5E1387"          # 부드러운 보라색
    soft_cyan = "#077A8F"            # 부드러운 청록색
    soft_yellow = "#B3AD33"          # 부드러운 노랑색
    
    chart_widget = profit_chart.get_widget()
    
    # 배경색 설정
    chart_widget.setBackground(QColor(dark_bg))
    
    # 축 스타일 설정
    chart_widget.getAxis('left').setPen(pg.mkPen(color=soft_pink, width=2))
    chart_widget.getAxis('bottom').setPen(pg.mkPen(color=soft_pink, width=2))
    chart_widget.getAxis('left').setTextPen(soft_cyan)
    chart_widget.getAxis('bottom').setTextPen(soft_cyan)
    
    # 테두리 설정
    chart_widget.setStyleSheet(f'''
        border: 2px solid {soft_pink};
        border-radius: 10px;
    ''')
    
    # 부드러운 네온 효과 추가
    glow = QGraphicsDropShadowEffect()
    glow.setBlurRadius(15)
    glow.setColor(QColor(soft_purple))
    glow.setOffset(0, 0)
    chart_widget.setGraphicsEffect(glow)
    
    # 차트 업데이트하여 변경사항 적용
    profit_chart.update_display()