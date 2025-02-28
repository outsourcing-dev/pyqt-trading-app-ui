from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
import pyqtgraph as pg

def apply_soft_neon_style(table_widget):
    """테이블에 부드러운 네온 스타일 적용"""
    # 소프트한 네온 색상 정의
    dark_bg = "#0F0326"              # 매우 어두운 보라색 배경
    soft_pink = "#AA0A80"            # 부드러운 핑크 테두리 (더 어두움)
    soft_purple = "#5E1387"          # 부드러운 보라색 (더 어두움)
    soft_cyan = "#077A8F"            # 부드러운 청록색 (더 어두움)
    soft_yellow = "#B3AD33"          # 부드러운 노랑색 (더 어두움)
    row_color = dark_bg              # 행 배경색
    alt_row_color = "#1A082E"        # 약간 밝은 보라색 배경
    text_color = "#E2E0FF"           # 밝은 라벤더 텍스트
    
    # 양수/음수 색상 (밝기 유지)
    positive_color = "#39FF14"       # 형광 연두색
    negative_color = "#FF2D2D"       # 형광 빨간색
    
    # app_font_name 속성 확인
    app_font_name = getattr(table_widget, 'app_font_name', 'NanumSquareOTF_acR')
    
    table_widget.setStyleSheet(f"""
        QTableWidget {{
            background-color: {row_color};
            color: {text_color};
            gridline-color: {soft_purple};
            font-size: 13px;
            border: 2px solid {soft_pink};
            border-radius: 8px;
            font-family: '{app_font_name}';
        }}
        
        QTableWidget::item {{
            border-bottom: 1px solid {soft_purple};
            padding: 8px 12px;
            background-color: {row_color};
            font-family: '{app_font_name}';
            font-weight: bold;
        }}
        
        /* 빈 셀에 배경색 적용 */
        QTableWidget::item:empty {{
            background-color: {row_color};
        }}

        QTableWidget::item:alternate {{
            background-color: {alt_row_color};
        }}
        
        /* 빈 셀이면서 alternate 행일 때 배경색 처리 */
        QTableWidget::item:alternate:empty {{
            background-color: {alt_row_color};
        }}
        

        QTableWidget::item:selected {{
            background-color: {soft_purple};
            color: {soft_yellow};
        }}
        
        QHeaderView::section {{
            background-color: {dark_bg};
            color: {soft_cyan};
            padding: 8px;
            border: none;
            border-bottom: 1px solid {soft_pink};
            font-family: '{app_font_name}';
            text-align: center;
            font-size: 14px;
            font-weight: bold;
        }}
        
        QHeaderView::section:vertical {{
            border-right: 1px solid {soft_pink};
            border-bottom: 1px solid {soft_pink};
            text-align: center;
        }}
        
        /* 왼쪽 상단 코너 버튼 스타일 */
        QTableCornerButton::section {{
            background-color: {dark_bg};
            border: 1px solid {soft_pink};
        }}

        QScrollBar:vertical {{
            background: {row_color};
            width: 8px;
            margin: 0px;
            border-radius: 4px;
        }}
        
        QScrollBar::handle:vertical {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 {negative_color}, stop:0.5 {soft_purple}, stop:1 {positive_color});
            min-height: 20px;
            border-radius: 4px;
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
    """)
    
    # 부드러운 네온 효과 추가
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(15)  # 부드러운 블러
    shadow.setColor(QColor(soft_purple))
    shadow.setOffset(0, 0)
    table_widget.setGraphicsEffect(shadow)
    
    table_widget.setAlternatingRowColors(True)
    table_widget.setShowGrid(True)

def apply_soft_neon_to_chart(chart_widget, app_font_name='NanumSquareOTF_acR'):
    """차트에 부드러운 네온 스타일 적용"""
    # 소프트한 네온 색상 정의
    dark_bg = "#0F0326"              # 매우 어두운 보라색 배경
    soft_pink = "#AA0A80"            # 부드러운 핑크 테두리
    soft_purple = "#5E1387"          # 부드러운 보라색
    soft_cyan = "#077A8F"            # 부드러운 청록색
    soft_yellow = "#B3AD33"          # 부드러운 노랑색
    
    # 배경색 설정
    chart_widget.setBackground(QColor(dark_bg))
    
    # 축 스타일 설정
    chart_widget.getAxis('left').setPen(pg.mkPen(color=soft_pink, width=2))
    chart_widget.getAxis('bottom').setPen(pg.mkPen(color=soft_pink, width=2))
    chart_widget.getAxis('left').setTextPen(soft_cyan)
    chart_widget.getAxis('bottom').setTextPen(soft_cyan)
    
    # 축 라벨 폰트 설정
    axis_font = QFont(app_font_name, 8)
    chart_widget.getAxis('left').setTickFont(axis_font)
    chart_widget.getAxis('bottom').setTickFont(axis_font)
    
    # 그리드 설정 - 부드러운 보라색 점선
    grid_color = QColor(soft_purple)
    grid_color.setAlpha(77)  # 30% 투명도
    grid_pen = pg.mkPen(color=grid_color, width=1, style=Qt.DotLine)
    chart_widget.showGrid(x=True, y=True, alpha=0.3)
    
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