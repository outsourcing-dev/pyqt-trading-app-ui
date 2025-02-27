import sys
from PyQt5.QtWidgets import QApplication
from ui.exchange_selector import ExchangeSelector
from modern_ui import apply_unified_style

def main():
    # PyQt 애플리케이션 생성
    app = QApplication(sys.argv)
    
    # 전체 앱에 통일된 스타일 적용
    
    apply_unified_style(app)
    
    # 거래소 선택 창 표시
    selector = ExchangeSelector()
    selector.show()
    
    # 프로그램이 종료될 때까지 사용자 입력 대기
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()