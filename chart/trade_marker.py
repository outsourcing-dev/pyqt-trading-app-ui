import pyqtgraph as pg

class TradeMarker(pg.ScatterPlotItem):
    def __init__(self):
        super().__init__()
        # 마커의 테두리 선 없애기 
        self.setPen(pg.mkPen(None))

    def add_trade(self, x, y, trade_type):
        """
        차트에 매매 표시 마커를 추가합니다
        trade_type 형식: "{LONG/SHORT}_{OPEN/CLOSE}"
        (예: "LONG_OPEN", "SHORT_CLOSE" 등)
        """
        position, action = trade_type.split('_')

        # 롱 포지션일 때
        if position == 'LONG':
            if action == 'OPEN':
                symbol = 't1'  # 위쪽 삼각형 (롱 진입)
                brush = pg.mkBrush('g')  # 초록색
            else:  # CLOSE
                symbol = 'h'  # 육각형 (롱 청산)
                brush = pg.mkBrush((144, 238, 144))  # 연한 초록색

        # 숏 포지션일 때
        else:  # SHORT
            if action == 'OPEN':
                symbol = 't'  # 아래쪽 삼각형 (숏 진입)
                brush = pg.mkBrush('r')  # 빨간색
            else:  # CLOSE
                symbol = 'h'  # 육각형 (숏 청산)
                brush = pg.mkBrush((255, 182, 193))  # 연한 빨간색

        # 설정한 모양과 색상으로 포인트 추가
        self.addPoints([{
            'pos': (x, y),    # 위치 좌표
            'symbol': symbol,  # 마커 모양
            'brush': brush,   # 마커 색상
            'size': 15        # 마커 크기
        }])
