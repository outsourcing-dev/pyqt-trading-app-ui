import requests
from datetime import datetime
import email.utils
import pytz

class NaverTimeFetcher:
    @staticmethod
    def get_naver_time():
        """
        네이버 서버시간을 가져옵니다.
        Returns:
            datetime: 네이버 서버 시간을 한국 시간대로 변환한 datetime 객체
        """
        try:
            response = requests.head('https://www.naver.com')
            
            # 응답 헤더에서 date 정보 추출
            server_time_str = response.headers['date']
            
            # RFC 2822 형식의 시간을 datetime 객체로 변환
            server_time_tuple = email.utils.parsedate_tz(server_time_str)
            server_time_timestamp = email.utils.mktime_tz(server_time_tuple)
            server_time = datetime.fromtimestamp(server_time_timestamp)
            
            # 한국 시간대로 변환
            kr_timezone = pytz.timezone('Asia/Seoul')
            kr_time = server_time.astimezone(kr_timezone)
            
            return kr_time
            
        except Exception as e:
            print(f"네이버 시간 가져오기 실패: {e}")
            # 실패시 로컬 시간 반환
            return datetime.now(pytz.timezone('Asia/Seoul'))