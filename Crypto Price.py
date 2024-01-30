import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import QTimer
import requests

class CryptoPriceApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Crypto')

        # 創建5組輸入框和對應的標籤
        self.input_labels = []
        self.input_edits = []
        self.price_labels = []
        for i in range(5):
            input_label = QLabel('請輸入幣種:')
            input_edit = QLineEdit()
            price_label = QLabel('最新價格:')

            self.input_labels.append(input_label)
            self.input_edits.append(input_edit)
            self.price_labels.append(price_label)

        # 開始和停止按鈕
        self.start_button = QPushButton('開始')
        self.stop_button = QPushButton('停止')

        # 佈局設置
        vbox = QVBoxLayout()
        for i in range(5):
            hbox_input = QHBoxLayout()
            hbox_input.addWidget(self.input_labels[i])
            hbox_input.addWidget(self.input_edits[i])
            
            vbox.addLayout(hbox_input)
            vbox.addWidget(self.price_labels[i])

        hbox_buttons = QHBoxLayout()
        hbox_buttons.addWidget(self.start_button)
        hbox_buttons.addWidget(self.stop_button)

        vbox.addLayout(hbox_buttons)

        self.setLayout(vbox)

        # 設置計時器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_prices)

        # 連接按鈕的點擊事件
        self.start_button.clicked.connect(self.start_timer)
        self.stop_button.clicked.connect(self.stop_timer)

        self.show()

    def start_timer(self):
        # 開始計時器，每秒執行一次update_prices
        self.timer.start(200)

    def stop_timer(self):
        # 停止計時器
        self.timer.stop()

    def update_prices(self):
        # 同時獲取多個幣種的價格
        for i in range(5):
            symbol = self.input_edits[i].text().strip().upper()
            if symbol:
                try:
                    response = requests.get(f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}', timeout=5)
                    response.raise_for_status()
                    data = response.json()
                    price = data.get('price')
                    if price:
                        formatted_price = "{:.4f}".format(float(price))
                        self.price_labels[i].setText(f'最新價格: {formatted_price}')
                    else:
                        self.price_labels[i].setText('無法獲取價格資訊')
                except requests.exceptions.RequestException as e:
                    print(f'API請求錯誤: {e}')
                    self.price_labels[i].setText('無法獲取價格資訊')
                except Exception as e:
                    print(f'發生錯誤: {e}')
                    self.price_labels[i].setText('無法獲取價格資訊')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CryptoPriceApp()
    sys.exit(app.exec_())
