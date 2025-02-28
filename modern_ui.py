import os
from PyQt5.QtWidgets import QFrame, QGraphicsDropShadowEffect, QVBoxLayout,QComboBox , QPushButton, QGraphicsOpacityEffect
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize, QTimer, QSequentialAnimationGroup, QParallelAnimationGroup, QAbstractAnimation
from PyQt5.QtGui import QColor, QPainter, QPainterPath, QLinearGradient, QPalette

# 둥근 모서리를 가진 프레임 클래스
class RoundedFrame(QFrame):
    def __init__(self, parent=None, radius=10, bg_color="#1e222d"):
        super().__init__(parent)
        self.radius = radius
        self.bg_color = bg_color
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 둥근 사각형 경로 생성
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), self.radius, self.radius)
        
        # 배경색으로 채우기
        painter.fillPath(path, QColor(self.bg_color))

# 차트에 현대적인 스타일 적용하기
def modernize_chart(chart_widget):
    """
    차트 위젯에 둥근 모서리와 그림자 효과를 적용합니다.
    """
    # 차트의 부모 위젯 찾기
    parent = chart_widget.parent()
    
    # 먼저 차트 자체의 색상을 설정
    chart_widget.setBackground('#1e222d')  # 메인 테마에 맞는 어두운 배경색
    
    # 차트를 담을 컨테이너 생성
    container = RoundedFrame(parent, radius=10, bg_color="#1e222d")  
    
    # 컨테이너에 레이아웃 생성
    container_layout = QVBoxLayout(container)
    container_layout.setContentsMargins(5, 5, 5, 5)
    
    # 차트를 원래 레이아웃에서 제거하고 컨테이너에 추가
    if parent and parent.layout():
        layout = parent.layout()
        index = layout.indexOf(chart_widget)
        if index >= 0:
            layout.removeWidget(chart_widget)
            container_layout.addWidget(chart_widget)
            layout.insertWidget(index, container)
    
    # 그림자 효과 추가
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(15)
    shadow.setColor(QColor(0, 0, 0, 80))
    shadow.setOffset(0, 4)
    container.setGraphicsEffect(shadow)
    
    # 차트 축 스타일 설정
    chart_widget.getAxis('left').setPen(QColor('#6d7b9c'))
    chart_widget.getAxis('bottom').setPen(QColor('#6d7b9c'))
    chart_widget.getAxis('left').setTextPen(QColor('#e6e9ef'))
    chart_widget.getAxis('bottom').setTextPen(QColor('#e6e9ef'))

# 현대적인 콤보박스 스타일 적용
def modernize_combobox(combobox, app_font_name='NanumSquare'):
    """
    콤보박스에 현대적인 스타일을 적용합니다.
    """
    combobox.setStyleSheet(f"""
        QComboBox {{
            background-color: #3d4760;
            color: white;
            padding: 8px 12px;
            border: 1px solid #4d5b7c;
            border-radius: 6px;
            font-size: 13px;
            min-height: 20px;
            font-family: '{app_font_name}';
        }}
        QComboBox:hover {{
            background-color: #4d5b7c;
            border: 1px solid #5d6b8c;
        }}
        QComboBox:focus {{
            border: 1px solid #6d7b9c;
        }}
        QComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px;
            border-left: 1px solid #4d5b7c;
            border-top-right-radius: 4px;
            border-bottom-right-radius: 4px;
        }}
        QComboBox QAbstractItemView {{
            background-color: #3d4760;
            color: white;
            selection-background-color: #4d5b7c;
            selection-color: white;
            border: none;
            outline: none;
            border-radius: 5px;
            padding: 4px;
            margin-top: 4px;
            font-family: '{app_font_name}';
        }}
        QComboBox QAbstractItemView::item {{
            min-height: 24px;
            padding: 4px 8px;
            border-radius: 3px;
        }}
        QComboBox QAbstractItemView::item:hover {{
            background-color: #4d5b7c;
        }}
        QComboBox QAbstractItemView::item:selected {{
            background-color: #5d6b8c;
        }}
    """)
    
    # 그림자 효과 추가
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(10)
    shadow.setColor(QColor(0, 0, 0, 50))
    shadow.setOffset(0, 2)
    combobox.setGraphicsEffect(shadow)

    # 더 세련된 테이블 스타일 적용
def apply_modern_table_style(table, header_color="#1e222d", row_color="#1e222d", 
                        alt_row_color="#252836", text_color="#e6e9ef", app_font_name='NanumSquare'):
    """
    테이블에 더 세련된 현대적 스타일을 적용합니다.
    """
    # 테이블 스타일 설정
    table.setStyleSheet(f"""
        QTableWidget {{
            background-color: {row_color};
            color: {text_color};
            gridline-color: transparent;
            font-size: 13px;
            border: none;
            border-radius: 8px;
            font-family: '{app_font_name}';
        }}
        
        QTableWidget::item {{
            border-bottom: 1px solid #313646;
            padding: 5px 10px;
            background-color: {row_color};  /* 명시적인 배경색 지정 */
        }}
        
        QTableWidget::item:alternate {{
            background-color: {alt_row_color};  /* 교차 행 배경색 */
        }}
        
        QTableWidget::item:selected {{
            background-color: #3d4760;
            color: white;
        }}
        
        /* 헤더 스타일 */
        QHeaderView::section {{
            background-color: {header_color};
            color: {text_color};
            padding: 8px;
            border: none;
            font-weight: bold;
            font-family: '{app_font_name}';
        }}
        
        QHeaderView::section:horizontal {{
            border-right: 1px solid #3d4760;
        }}
        
        QHeaderView::section:vertical {{
            border-bottom: 1px solid #3d4760;
        }}
        
        /* 스크롤바 스타일 */
        QScrollBar:vertical {{
            background: {row_color};
            width: 8px;
            margin: 0px;
        }}
        
        QScrollBar::handle:vertical {{
            background: #4d5b7c;
            min-height: 20px;
            border-radius: 4px;
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        
        QScrollBar:horizontal {{
            background: {row_color};
            height: 8px;
            margin: 0px;
        }}
        
        QScrollBar::handle:horizontal {{
            background: #4d5b7c;
            min-width: 20px;
            border-radius: 4px;
        }}
        
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0px;
        }}
        
        /* 위젯 자체의 배경색도 명시적으로 설정 */
        {table.objectName()} {{
            background-color: {row_color};
        }}
    """)
    
    # 그림자 효과 추가
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(15)
    shadow.setColor(QColor(0, 0, 0, 80))
    shadow.setOffset(0, 4)
    table.setGraphicsEffect(shadow)
    
    # 교차 행 색상 설정 (줄무늬 효과)
    table.setAlternatingRowColors(True)
    
    # 헤더 설정
    header = table.horizontalHeader()
    header.setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
    header.setStretchLastSection(True)
    
    # 테이블 셀 설정
    table.setShowGrid(False)  # 그리드 라인 제거

# 전체 앱에 통일된 스타일 적용
def apply_unified_style(app, app_font_name='NanumSquare'):
    """
    앱 전체에 통일된 현대적 스타일을 적용합니다.
    """
    app.setStyleSheet(f"""
        QMainWindow, QDialog {{
            background-color: #1a1d2d;
            color: #e6e9ef;
        }}
        
        QWidget {{
            color: #e6e9ef;
            font-family: '{app_font_name}', Arial;
        }}
        
        QLabel {{
            color: #e6e9ef;
            font-size: 8px;
        }}
        
        QLabel#program_name {{
            font-size: 18px;
            font-weight: bold;
            color: white;
        }}
        
        QComboBox {{
            background-color: #2a3447;
            color: white;
            padding: 6px 10px;
            border: none;
            border-radius: 4px;
        }}
        
        QComboBox:hover {{
            background-color: #3d4760;
        }}
        
        QComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: center right;
            width: 20px;
            border: none;
        }}
        
        QComboBox QAbstractItemView {{
            background-color: #2a3447;
            color: white;
            selection-background-color: #3d4760;
            selection-color: white;
            border: none;
            outline: none;
        }}
    """)

def add_price_update_effect(label):
    """가격 레이블에 값이 변경될 때 강조 효과 추가"""
    def animate_color():
        # 가격 변화를 표시하는 애니메이션 시퀀스
        effect = QGraphicsOpacityEffect(label)
        label.setGraphicsEffect(effect)
        
        # 깜빡이는 효과를 위한 애니메이션
        anim = QPropertyAnimation(effect, b"opacity")
        anim.setDuration(300)
        anim.setStartValue(1.0)
        anim.setEndValue(0.5)
        anim.setEasingCurve(QEasingCurve.OutQuad)
        
        anim2 = QPropertyAnimation(effect, b"opacity")
        anim2.setDuration(300)
        anim2.setStartValue(0.5)
        anim2.setEndValue(1.0)
        anim2.setEasingCurve(QEasingCurve.InQuad)
        
        # 애니메이션 그룹 생성
        group = QSequentialAnimationGroup()
        group.addAnimation(anim)
        group.addAnimation(anim2)
        group.start(QAbstractAnimation.DeleteWhenStopped)
    
    # 기존 setText 메서드 저장
    original_setText = label.setText
    
    # setText 오버라이드하여 값 변경 시 애니메이션 효과 적용
    def custom_setText(text):
        if label.text() != text:  # 텍스트가 변경된 경우에만
            original_setText(text)
            animate_color()
    
    # 메서드 변경
    label.setText = custom_setText
    return label

def add_smooth_chart_updates(chart_widget):
    """차트에 부드러운 업데이트 효과 적용"""
    # 기존 데이터 업데이트 함수 저장
    if hasattr(chart_widget, 'candlestick_item'):
        original_set_data = chart_widget.candlestick_item.set_data
        
        def animated_set_data(data):
            # 부드러운 업데이트를 위한 효과
            effect = QGraphicsOpacityEffect(chart_widget)
            chart_widget.setGraphicsEffect(effect)
            
            # 페이드아웃-업데이트-페이드인 애니메이션
            fade_out = QPropertyAnimation(effect, b"opacity")
            fade_out.setDuration(200)
            fade_out.setStartValue(1.0)
            fade_out.setEndValue(0.7)
            fade_out.setEasingCurve(QEasingCurve.OutQuad)
            
            fade_in = QPropertyAnimation(effect, b"opacity")
            fade_in.setDuration(200)
            fade_in.setStartValue(0.7)
            fade_in.setEndValue(1.0)
            fade_in.setEasingCurve(QEasingCurve.InQuad)
            
            # 애니메이션 시퀀스 생성
            sequence = QSequentialAnimationGroup()
            sequence.addAnimation(fade_out)
            
            # 업데이트 함수 연결
            def update_data():
                original_set_data(data)
            
            # 업데이트 타이머 설정
            timer = QTimer()
            timer.singleShot(200, update_data)
            
            sequence.addAnimation(fade_in)
            sequence.start(QAbstractAnimation.DeleteWhenStopped)
        
        # 메서드 교체
        chart_widget.candlestick_item.set_data = animated_set_data

def add_animated_background(widget):
    """배경에 미묘한 그라데이션 애니메이션 효과 추가"""
    # 그라데이션 객체 생성
    gradient = QLinearGradient(0, 0, widget.width(), widget.height())
    gradient.setColorAt(0, QColor("#1a1d2d"))
    gradient.setColorAt(1, QColor("#2a3041"))
    
    # 팔레트에 그라데이션 설정
    palette = widget.palette()
    palette.setBrush(QPalette.Window, gradient)
    widget.setPalette(palette)
    widget.setAutoFillBackground(True)
    
    # 그라데이션 애니메이션
    def animate_gradient():
        animation = QPropertyAnimation()
        animation.setDuration(10000)  # 10초
        animation.setLoopCount(-1)    # 무한 반복
        
        def update_gradient(value):
            new_gradient = QLinearGradient(0, 0, widget.width(), widget.height())
            
            # 값에 따라 색상 약간 변경
            color1 = QColor("#1a1d2d")
            color2 = QColor("#2a3041")
            
            # 미묘한 색상 변화
            h1, s1, v1, _ = color1.getHsv()
            h2, s2, v2, _ = color2.getHsv()
            
            # 색조와 채도 약간 변경 (값의 5% 정도)
            mod_value = value * 0.05
            color1.setHsv(h1, max(0, min(255, s1 + int(mod_value))), v1)
            color2.setHsv(h2, max(0, min(255, s2 - int(mod_value))), v2)
            
            new_gradient.setColorAt(0, color1)
            new_gradient.setColorAt(1, color2)
            
            palette = widget.palette()
            palette.setBrush(QPalette.Window, new_gradient)
            widget.setPalette(palette)
        
        animation.valueChanged.connect(update_gradient)
        animation.start(QAbstractAnimation.DeleteWhenStopped)
    
    # 애니메이션 시작
    QTimer.singleShot(500, animate_gradient)
    
def add_table_row_animation(table):
    """테이블에 새 행이 추가될 때 애니메이션 효과"""
    # 원래 insertRow 메서드 저장
    original_insertRow = table.insertRow
    
    def animated_insertRow(row):
        # 먼저 행 삽입
        original_insertRow(row)
        
        # 새 행의 모든 셀에 애니메이션 적용
        for col in range(table.columnCount()):
            item = table.item(row, col)
            if item:
                # 초기에는 투명하게
                effect = QGraphicsOpacityEffect()
                effect.setOpacity(0)
                table.setCellWidget(row, col, effect)
                
                # 페이드인 애니메이션
                anim = QPropertyAnimation(effect, b"opacity")
                anim.setDuration(500)
                anim.setStartValue(0.0)
                anim.setEndValue(1.0)
                anim.setEasingCurve(QEasingCurve.InOutQuad)
                anim.start(QAbstractAnimation.DeleteWhenStopped)
    
    # 메서드 교체
    table.insertRow = animated_insertRow