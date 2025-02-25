import ccxt
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

class DataFetcher:
    def __init__(self):
        # Binance 거래소 객체 생성
        self.exchange = ccxt.binance()

    def fetch_ohlcv(self, symbol='BTC/USDT', timeframe='1m', limit=300):
        """
        Binance에서 OHLCV(시가/고가/저가/종가/거래량) 데이터를 가져옵니다
        기본값: BTC/USDT, 1시간봉, 100개 봉
        """
        try:
            # 캔들 데이터 가져오기
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            
            # 데이터프레임으로 변환
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            
            # 타임스탬프를 읽기 쉬운 날짜형식으로 변환
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            
            # 캔들스틱 차트용 배열 생성
            candle_data = np.column_stack((
                np.arange(len(df)),  # x축 인덱스
                df['open'].values,   # 시가
                df['high'].values,   # 고가
                df['low'].values,    # 저가
                df['close'].values   # 종가
            ))
            
            return candle_data, df
        except Exception as e:
            print(f"데이터 가져오기 실패: {e}")
            return None, None

    def get_current_price(self, symbol='BTC/USDT'):
        """
        특정 코인의 현재가를 가져옵니다
        기본값: BTC/USDT
        """
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return ticker['last']  # 최근 거래가 반환
        except Exception as e:
            print(f"현재가 가져오기 실패: {e}")
            return None
