import pyqtgraph as pg
from PyQt5.QtGui import QPainter

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
