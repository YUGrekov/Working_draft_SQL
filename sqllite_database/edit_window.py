from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget
from main_base import *
from datetime import datetime



class Window_tabl_checkbox(QWidget):
    def __init__(self, list_tabl):
        super(Window_tabl_checkbox, self).__init__()
        self.setWindowTitle('Список таблиц')
        self.setStyleSheet("background-color: #a0b0a5;")
        self.resize(260, 80)
        #self.move(200,40)
        
        clickButton = QPushButton('Подключиться к таблице', self)
        clickButton.resize(80,40)
        clickButton.clicked.connect(self.choose_tabl)

        self.combo = QComboBox()
        self.combo.setFont(QFont('Arial', 10))

        for tabl in list_tabl:
            self.combo.addItem(str(tabl))

        layout = QVBoxLayout()
        layout.addWidget(self.combo)
        layout.addWidget(clickButton)

        self.setLayout(layout)
    # Choose table
    def choose_tabl(self):
        name_table = self.combo.currentText()
        self.ch_tabl = Window_update_sql(name_table)
        self.ch_tabl.show()

class Window_update_sql(QWidget):
    def __init__(self, table_used):
        super(Window_update_sql, self).__init__()
        self.setWindowTitle('Редактор базы данных')
        self.setStyleSheet("background-color: #a0b0a5;")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.resize(1600, 870)

        self.TableWidget = QTableWidget(self)
        self.TableWidget.setGeometry(10,50,1580,710)

        self.logTextBox = QTextEdit(self)
        self.logTextBox.setGeometry(10,759,1580,100)
        self.logTextBox.setReadOnly(True)

        self.table_used = table_used
        self.edit_SQL = Editing_table_SQL()
        column, row, self.hat_name, value = self.edit_SQL.editing_sql(self.table_used)
        self.tablew(column, row, self.hat_name, value)

        new_addrow_Button = QPushButton('Добавить строку', self)
        new_addrow_Button.resize(120,25)
        new_addrow_Button.move(10, 10) 
        new_addrow_Button.clicked.connect(self.add_row)

        remoterow_Button = QPushButton('Удалить строку', self)
        remoterow_Button.resize(120,25)
        remoterow_Button.move(150, 10) 
        remoterow_Button.clicked.connect(self.delete_row)

        self.namecolumn = QLineEdit(self, placeholderText='Название нового столбца', clearButtonEnabled=True)
        self.namecolumn.setStyleSheet('border: 1px solid #6f7370;')
        self.namecolumn.move(300, 10)
        self.namecolumn.resize(150,25)
        new_addcol_Button = QPushButton('Добавить столбец', self)
        new_addcol_Button.resize(120,25)
        new_addcol_Button.move(455, 10) 
        new_addcol_Button.clicked.connect(self.add_column)

        remoterow_Button = QPushButton('Удалить столбец', self)
        remoterow_Button.resize(120,25)
        remoterow_Button.move(600, 10) 
        remoterow_Button.clicked.connect(self.delete_column)

        cleartab_Button = QPushButton('Очистить таблицу', self)
        cleartab_Button.resize(120,25)
        cleartab_Button.move(745, 10) 
        cleartab_Button.clicked.connect(self.clear_tabl)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.logTextBox)
        self.layout.addWidget(new_addrow_Button)
        self.layout.addWidget(new_addcol_Button)
        self.layout.addWidget(remoterow_Button)
        self.layout.addWidget(cleartab_Button)
        self.layout.addWidget(self.TableWidget)
    # Сompletely clear the table
    def clear_tabl(self):
        rowcount = self.TableWidget.rowCount()

        while rowcount >= 0:
            self.TableWidget.removeRow(rowcount)
            rowcount -= 1

        self.edit_SQL.clear_tabl(self.table_used)
    # Adding new lines
    def add_row(self):  
        column = self.TableWidget.currentColumn()
        rowPos = self.TableWidget.rowCount()
        
        if rowPos == 0: 
            print('Невозможно добавить строки в пустую таблицу')
            return

        self.TableWidget.insertRow(rowPos)

        text_cell = self.TableWidget.item(rowPos - 1, 0).text()
        self.TableWidget.setItem(rowPos, 0, QTableWidgetItem (f'{int(text_cell) + 1}'))

        self.edit_SQL.add_new_row(column, self.table_used, self.hat_name)
        # Logs
        self.logs_msg('В конец таблицы добавлена новая строка\n')
    # Removing rows
    def delete_row(self):
        row = self.TableWidget.currentRow()
        if row <= 0: 
            self.logs_msg('Невозможно удалить строки из пустой таблицы\n')
            return
        
        text_cell_id = self.TableWidget.item(int(row), 0).text()
        if row > -1: 
            self.TableWidget.removeRow(row)
            self.TableWidget.selectionModel().clearCurrentIndex()

        self.edit_SQL.delete_row(text_cell_id, self.table_used)
        # Logs
        self.logs_msg(f'Из таблицы: {self.table_used} удалена строка id={text_cell_id}\n')
    # Adding new column
    def add_column(self):
        def letters(name):
            if len(name) == 0: name = 'newcolumn'
            return ''.join(filter(str.isalnum, name))
        
        namecolumn = letters(self.namecolumn.text())
        hat_name = self.edit_SQL.column_names(self.table_used)
        if namecolumn in hat_name: 
            self.logs_msg('Дублирующие название столбца!\n')
            return

        column_count = self.TableWidget.columnCount()
        self.TableWidget.insertColumn(column_count)

        self.edit_SQL.add_new_column(self.table_used, namecolumn)

        hat_name = self.edit_SQL.column_names(self.table_used)
        self.TableWidget.setHorizontalHeaderLabels(hat_name)
    
    
        # Removing rows
    # Removing column
    def delete_column(self):
        column = self.TableWidget.currentColumn()
        self.TableWidget.removeColumn(column)

        hat_name = self.edit_SQL.column_names(self.table_used)
        self.edit_SQL.delete_column(column, hat_name, self.table_used)
        self.logs_msg('Удален столбец\n')
    # tabl: Signals
    def tabl_signals(self):
        self.models_used = Signals
        column, row, self.hat_name, value = self.edit_SQL.editing_sql(self.table_used)
        self.tablew(column, row, self.hat_name, value)
    # Building the selected table
    def tablew(self, column, row, hat_name, value):
        # Logs
        self.logs_msg(f'Запущен редактор базы данных. Таблица: {self.table_used}\n')
        # TableW
        self.TableWidget.setColumnCount(column)
        self.TableWidget.setRowCount(row)
        self.TableWidget.setHorizontalHeaderLabels(hat_name)
        # Разрешить щелчок правой кнопкой мыши для создания меню
        #self.TableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.TableWidget.verticalHeader().setVisible(False)
        # column size
        #for size_column in list_size:
        #   self.TableWidget.setColumnWidth(size_column[0], size_column[1])

        for row_t in range(row):
            for column_t in range(column):
                if value[row_t][column_t] is None:
                    item = QTableWidgetItem('')
                else:
                    item = QTableWidgetItem(str(value[row_t][column_t]))
                # center text
                #item.setTextAlignment(Qt.AlignHCenter)
                # Выравнивание все столбцов по общей ширине
                #self.TableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                self.TableWidget.setItem(row_t, column_t, item)
        # Выравнивание по столбцов и строк по наибольшей длине
        self.TableWidget.resizeColumnsToContents()
        self.TableWidget.resizeRowsToContents()
        # Events
        self.TableWidget.itemChanged.connect(self.click_position)
    # Cell change on click
    def click_position(self):
        row    = self.TableWidget.currentRow()
        column = self.TableWidget.currentColumn()

        for currentQTableWidgetItem in self.TableWidget.selectedItems():
            text_cell = self.TableWidget.item(currentQTableWidgetItem.row(), column).text()
        
        check_cell = self.TableWidget.item(int(row), 0)
        if check_cell is None: return

        text_cell_id = self.TableWidget.item(int(row), 0).text()

        hat_name = self.edit_SQL.column_names(self.table_used)
        self.edit_SQL.update_row_tabl(column, text_cell, text_cell_id, self.table_used, hat_name)
    # Logging messeges
    def logs_msg(self, logs):
        today = datetime.now()
        self.logTextBox.insertPlainText(f'{today} - {logs}')
 