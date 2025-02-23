import pyqtgraph as pg
from PyQt5.QtGui import QPainter

class CandlestickItem(pg.GraphicsObject):
    def __init__(self):
        pg.GraphicsObject.__init__(self)
        self.picture = None
        self.data = None

    def set_data(self, data):
        """
        # 캔들스틱 차트의 데이터를 설정합니다
        # 데이터 형식: [시간, 시가, 고가, 저가, 종가] 배열
        """
        self.data = data
        self.generate_picture()
        self.informViewBoundsChanged()

    def generate_picture(self):
        # 데이터가 없으면 그냥 리턴
        if self.data is None:
            return

        # 봉의 너비 설정 (시간 간격의 60%)
        w = (self.data[1][0] - self.data[0][0]) * 0.6
        self.picture = pg.QtGui.QPicture()
        p = QPainter(self.picture)

        for t, open, high, low, close in self.data:
            # 주가 상승/하락에 따라 색상 지정
            # 종가가 시가보다 높거나 같으면 초록색(상승)
            if close >= open:
                p.setBrush(pg.mkBrush('g'))
                p.setPen(pg.mkPen('g'))
            # 종가가 시가보다 낮으면 빨간색(하락)
            else:
                p.setBrush(pg.mkBrush('r'))
                p.setPen(pg.mkPen('r'))

            # 캔들스틱 그리기
            # 꼬리 그리기 (고가-저가 선)
            p.drawLine(pg.QtCore.QPointF(t, low), pg.QtCore.QPointF(t, high))
            # 몸통 그리기 (시가-종가 직사각형)
            p.drawRect(pg.QtCore.QRectF(t - w / 2, open, w, close - open))

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
