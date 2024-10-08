from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6 import *
from window import InputDialog
import pandas as pd
import csv
import sys, random


class TableModel(QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])


class Scoreboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Таблица лидеров")
        self.index = []
        self.table = QTableView()
        self.data = []
        self.setFixedWidth(254)

        with open("newlb.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row["Name"]
                count = row["Count"]
                self.data.append([name, count])

        for i in range(len(self.data) - 1):
            for j in range(len(self.data) - 1 - i):
                if int(self.data[j][1]) < int(self.data[j + 1][1]):
                    self.data[j], self.data[j + 1] = self.data[j + 1], self.data[j]

        for i in range(1, len(self.data) + 1):
            self.index.append(f"{i} место")
        data = pd.DataFrame(self.data,
                            columns=['Имя', 'Очки'], index=self.index
                            )
        self.model = TableModel(data)
        self.table.setModel(self.model)
        self.setCentralWidget(self.table)


class helpWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setWindowTitle("Справка")
        self.label = QLabel("Пользователь должен назвать город начинающийся на последнюю букву."
                            "\nЕсли город оканчивается “ь”, “ъ” или “й” то учитывается предыдущая буква. "
                            "\nЗа каждое правильно отгаданное слово вы получаете 1 балл. "
                            "\nЗа 3 полученных балла у вас есть возможность пропустить заданное компьютером слово. "
                            "\nЕсли компьютер не может ответить на город игрока, то пользователь выиграл и наоборот."
                            "\nДоступно три ограничения времени: 30, 45 и 60 секунд."
                            "\nЗа каждое правильно отгаданное слово к оставшемуся времени прибавляется 15 секунд. "
                            "\nВ случае проигрыша вам будет предложено начать заново,показав ваш максимальный результат"
                            " с учетом пропуска .")
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.label.setStyleSheet("""
        font-size:15px;
        """)
        layout.addWidget(self.label)
        self.setLayout(layout)


class citys(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Города'
        self.setStyleSheet("background-color:#343155;")
        self.left = 50
        self.top = 50
        self.width = 350
        self.height = 540
        self.icon = ""
        self.currentRow = 0
        self.compWord = ""
        self.lastlet = ""
        self.count = 0
        self.value = False
        self.step = 30
        self.Label1 = QLabel()
        self.w = None
        self.a = None
        self.maxcount = 0
        self.usescity = list()
        self.initUI()

    def initUI(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(self.icon))
        self.getWord()


        input_dialog = InputDialog()
        input_dialog.show()
        if input_dialog.exec() == QDialog.DialogCode.Accepted:
            self.text = input_dialog.getText()
        else:
            self.text = "Неизвестный пользователь"
        menu_bar = self.menuBar()
        levels_menu = menu_bar.addMenu("Сложность")
        levels_menu4 = levels_menu.addAction(QIcon('#'), "30 секунд")
        levels_menu4.triggered.connect(self.btn30)

        levels_menu5 = levels_menu.addAction(QIcon('#'), "45 секунд")
        levels_menu5.triggered.connect(self.btn45)

        levels_menu6 = levels_menu.addAction(QIcon('#'), "60 секунд")
        levels_menu6.triggered.connect(self.btn60)

        score = menu_bar.addAction("Таблица")
        score.triggered.connect(self.table)

        self.setStatusBar(QStatusBar(self))
        menu_bar.setStyleSheet("""
        *{
        background-color:white;
        font-size:13px;
        font-color:#343155;
        font-weight:bold;
        }
        """)

        pageLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout(self)
        self.outerLayout = QHBoxLayout(self)
        self.frame = QFrame()
        self.frame.setStyleSheet("""
            border-width: 6px;
            border-height: 10px;
            border-radius:4px;
            font-size:20px;
            font-weight:bold;
            color: #F8F8FF;
        """)

        count2 = QVBoxLayout()
        btntime = QVBoxLayout()
        count2.setContentsMargins(0, 0, 0, 30)
        self.askbtnout = QHBoxLayout()

        self.mainLayout = QVBoxLayout()
        self.topLayout.addLayout(self.outerLayout)
        self.topLayout.addLayout(self.askbtnout)
        self.mainLayout.setContentsMargins(0, 10, 0, 30)
        warnin = QVBoxLayout()
        warnin.setContentsMargins(0, 10, 0, 0)
        helpLayout = QVBoxLayout()
        btnLayout = QHBoxLayout()
        textEditout = QHBoxLayout()
        textEditout.setContentsMargins(0, 50, 0, 0)
        stacklayout = QStackedLayout()
        pageLayout.addLayout(self.topLayout)
        pageLayout.addLayout(btntime)
        pageLayout.addLayout(count2)
        pageLayout.addLayout(self.mainLayout)
        pageLayout.addLayout(helpLayout)
        pageLayout.addLayout(warnin)
        pageLayout.addLayout(textEditout)
        pageLayout.addLayout(btnLayout)
        pageLayout.addLayout(stacklayout)

        self.label = QLabel("30")
        self.innerLayout = QHBoxLayout(self.frame)
        self.innerLayout.addWidget(self.label)
        self.outerLayout.addWidget(self.frame)
        self.askbtnout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.outerLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.frame.installEventFilter(self)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_func)
        self.warnin1 = QLabel("")
        self.warnin1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        warnin.addWidget(self.warnin1)
        self.warnin1.setStyleSheet("""
                    font-size:20px;
                    font-weight:bold;
                    color: #F8F8FF;
                """)

        self.textEdit = QLineEdit(self)
        self.start_stop_func()
        self.textEdit.setReadOnly(True)
        textEditout.addWidget(self.textEdit)
        self.textEdit.setStyleSheet("""
        *{
            background-color:#5b586e;
            border-radius:16px;
            padding:5px 0;
            border:1px solid #5b586e;	
            color:#fff;
            font-size:20px;
        }
        *:focus{
            border:1px solid #8b86aa;
            background-color:#343155;
        }
        """)

        askbtn = QPushButton("?")
        askbtn.pressed.connect(lambda: self.askButtn())

        self.askbtnout.addWidget(askbtn)
        askbtn.setStyleSheet("""
        *{
            width:34px;
            height:34px;
            background-color:#0d6efd;
            border-radius:16px;
            padding:6px ;
            border:1px solid #343155;  
            color:#fff;
            margin-top:1px;
            font-size:24px;
            font-weight:bold;
        }
        *:hover{
            background-color:#0b5ed7;
            border:1px solid #9ac3fe;
        }
        """)

        self.count1 = QLabel(f"{self.count}")
        self.count1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        count2.addWidget(self.count1)
        self.count1.setStyleSheet("""
            font-size:20px;
            font-weight:bold;
            color: #F8F8FF;
        """)

        self.Label1 = QLabel(f"Введите город на букву {self.lastlet.upper()}")
        self.Label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        helpLayout.addWidget(self.Label1)
        self.Label1.setStyleSheet("""
            font-size:27px;
            font-weight:bold;
            color: #F8F8FF;
        """)

        self.Label2 = QLabel(f"{self.compWord[:1].upper() + self.compWord[1:]}")
        self.Label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(self.Label2)
        self.Label2.setStyleSheet("""
            font-size:40px;
            font-weight:bold;
            color: #F8F8FF;
        """)
        btn1 = QPushButton("Проверить слово")
        btn1.pressed.connect(lambda: self.isword())
        btnLayout.addWidget(btn1)
        btn1.setStyleSheet("""
        *{
            background-color:#0d6efd;
            border-radius:12px;
            border:1px solid #343155;
            height:34px;
            color:#fff;
            font-size:18px;
            font-weight:bold;
        }
        *:hover{
            background-color:#0b5ed7;
            border:1px solid #9ac3fe;
        }
        """)

        btn2 = QPushButton("Пропустить слово")
        btn2.pressed.connect(lambda: self.skipWord())
        btnLayout.addWidget(btn2)
        btn2.setStyleSheet("""
        *{
            background-color:#0d6efd;
            border-radius:12px;
            border:1px solid #343155;
            color:#fff;
            height:34px;
            font-size:18px;
            font-weight:bold;
        }
        *:hover{
            background-color:#0b5ed7;
            border:1px solid #9ac3fe;
        }
        """)

        widget = QWidget(self)
        widget.setLayout(pageLayout)
        self.setCentralWidget(widget)

    def eventFilter(self, obj, event):
        if obj is self.frame:
            if event.type() == QEvent.Type.MouseButtonPress:
                self.start_stop_func()
        return super().eventFilter(obj, event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return:
            self.isword()

    def btn30(self):
        self.step = 30
        self.timer.stop()
        self.count = 0
        self.label.setText("30")
        self.textEdit.setReadOnly(True)
        self.textEdit.clear()
        self.usescity = list()
        self.warnin1.hide()
        self.getWord()
        self.on_click_label()
        return self.step

    def btn45(self):
        self.step = 45
        self.timer.stop()
        self.count = 0
        self.label.setText("45")
        self.textEdit.setReadOnly(True)
        self.textEdit.clear()
        self.usescity = list()
        self.warnin1.hide()
        self.getWord()
        self.on_click_label()
        self.start_stop_func()
        return self.step

    def btn60(self):
        self.step = 60
        self.timer.stop()
        self.count = 0
        self.label.setText("60")
        self.textEdit.setReadOnly(True)
        self.textEdit.clear()
        self.usescity = list()
        self.warnin1.hide()
        self.getWord()
        self.start_stop_func()
        self.on_click_label()
        return self.step

    def cantWrite(self):
        self.warnin1.show()
        self.warnin1.setText("Этого города нет в словаре \n или он был использован ранее!")

    def getWord(self):
        wordsFile = open("city.txt", "r", encoding="utf-8")
        words = wordsFile.read().split()
        self.compWord = random.choice(words)
        self.lastLetter()

    def lastLetter(self):
        if self.compWord[-1:] == "ь" or self.compWord[-1:] == "ъ" or self.compWord[-1:] == "ы" or self.compWord[
                                                                                                  -1:] == "й":
            self.lastlet = self.compWord[-2:-1]
            self.Label1.setText(f"Введите город на букву {self.lastlet.upper()}")
        else:
            self.lastlet = self.compWord[-1:]
            self.Label1.setText(f"Введите город на букву {self.lastlet.upper()}")

    def askButtn(self):
        if self.w is None:
            self.w = helpWindow()
            self.w.show()
        else:
            self.w.close()
            self.w = None

    def table(self):
        if self.a is None:
            self.a = Scoreboard()
            self.a.show()
        else:
            self.a.close()
            self.a = None

    def newCity(self):
        if self.value:
            wordsFile = open("city.txt", "r", encoding="utf-8")
            words = wordsFile.read().lower().split()
            random.shuffle(words)
            if self.Text.text()[-1:] == "ь" or self.Text.text()[-1:] == "ъ" or self.Text.text()[
                                                                               -1:] == "ы" or self.Text.text()[
                                                                                              -1:] == "й":
                for word in words:
                    if word[:1].lower() == self.Text.text()[
                                           -2:-1].lower() and word.lower() not in self.usescity and self.Text.text().lower() not in self.usescity:
                        self.usescity.append(self.compWord.lower())
                        self.usescity.append(self.Text.text().lower())
                        self.compWord = word
                        self.usescity.append(self.compWord.lower())
                        self.on_click_label()
                        self.lastLetter()
                        break


            else:
                for word in words:
                    if word[:1].lower() == self.Text.text()[
                                           -1:].lower() and word.lower() not in self.usescity and self.Text.text().lower() not in self.usescity:
                        self.usescity.append(self.compWord.lower())
                        self.usescity.append(self.Text.text().lower())
                        self.compWord = word
                        self.on_click_label()
                        self.usescity.append(self.compWord.lower())
                        self.lastLetter()
                        return "0"
        else:
            self.cantWrite()

    def on_click_label(self):
        self.Label2.setText(f"{self.compWord[:1].upper() + self.compWord[1:]}")
        self.Label2.adjustSize()
        self.count1.setText(f"{self.count}")

    def start_stop_func(self):
        if not self.timer.isActive():
            self.timer.start(1000)
            self.textEdit.setReadOnly(False)
        else:
            self.timer.stop()
            self.textEdit.setReadOnly(True)

    def resetAll(self):
        self.compWord = ""
        self.count = 0
        self.value = False
        self.step = 30
        self.label.setText("30")
        self.timer.stop()
        self.textEdit.setReadOnly(True)
        self.textEdit.clear()
        self.usescity = list()
        self.warnin1.hide()
        self.getWord()
        self.on_click_label()

    def update_func(self):
        if self.step > 0:
            self.step -= 1
            self.label.setText(str(self.step))
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Время вышло!")
            dlg.setText(f"Ваше время вышло!\nВаше максимальное кол-во очков: {self.maxcount}\nНачать заново?")
            dlg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            dlg.setIcon(QMessageBox.Icon.Question)
            dlg.setStyleSheet("""
            background-color:white;
            """)
            button = dlg.exec()
            print(self.text)
            print(len(self.text))
            self.add_to_table(self.text, self.count)
            if button == QMessageBox.StandardButton.Yes:
                self.resetAll()
            else:
                sys.exit(0)

    def add_to_table(self, name, count):
        with open("lb.csv", "a", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([name, count])
        file.close()

        with (open("lb.csv", "r", encoding="utf-8") as r,
              open("newlb.csv", "w", encoding="utf-8") as o):
            for line in r:
                if line.strip():
                    o.write(line)
        r.close()
        o.close()

    def skipWord(self):
        if self.count >= 3:
            self.count = self.count - 3
            self.getWord()
            self.warnin1.hide()
            self.usescity.append(self.getWord())
            self.on_click_label()
        else:
            self.warnin1.show()
            self.warnin1.setText("У вас недостаточно очков \n для пропуска слова")

    def update1(self):
        self.count = self.count + 1
        self.maxcount = self.count
        return self.count

    def isword(self):
        self.value = False
        wordsFile = open("city.txt", "r", encoding="utf-8")
        words = wordsFile.read().lower().split()
        self.Text = self.textEdit
        if self.Text.text().lower() in words and self.Text.text().lower() not in self.usescity:
            self.update1()
            self.warnin1.hide()
            self.value = True
            self.step = self.step + 15
        self.newCity()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = citys()
    game.show()
    app.exec()
