
from functools import partial
from PySide6.QtWidgets import *
from PySide6.QtUiTools import *
from PySide6.QtCore import *

import database

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        loader = QUiLoader()
        self.ui = loader.load("mainwindow.ui", None)
        self.ui.show()
        
        self.ui.save_Button.clicked.connect(self.add_newdatabase)
        self.readFromDatabase()

    def readFromDatabase(self):
        
        result = database.getAll()
        
        for i in range(len(result)):
            
            title_button = QPushButton()
            new_checkbox = QCheckBox()
            delet_button = QPushButton('❌')
            
            title_button.setText(result[i][1])
            title_button.clicked.connect(partial(self.showing_details, result[i][1], result[i][2],result[i][4],result[i][5]))
            
            delet_button.setStyleSheet('background-color: white; max-width: 15px; height: 15px')
            delet_button.clicked.connect(partial(self.delet_task, result[i][0], title_button, new_checkbox, delet_button))
            
            new_checkbox.clicked.connect(partial(self.changdone, result[i][0], new_checkbox, title_button, delet_button))
            if result[i][3] == 1:
                new_checkbox.setChecked(True)
            else:
                new_checkbox.setChecked(False)
            
            #priority color
            if result[i][6] == 1:      
                title_button.setStyleSheet('background-color: red; color: white')
            else:
                title_button.setStyleSheet('background-color: blue; color: white')   
           
            if result[i][3] == 0 or result[i][3] == None :
                self.ui.gridLayout.addWidget(new_checkbox, i, 0)
                self.ui.gridLayout.addWidget(title_button, i, 1)           
                self.ui.gridLayout.addWidget(delet_button, i, 3)
            
            elif result[i][3] == 1 or new_checkbox.isChecked() :
                self.ui.gridLayout_2.addWidget(new_checkbox, i, 0)
                self.ui.gridLayout_2.addWidget(title_button, i, 1)           
                self.ui.gridLayout_2.addWidget(delet_button, i, 3)
    
    def changdone(self, id, new_checkbox, title_button, delet_button):
        
        if new_checkbox.isChecked():
            database.done_update(id, 1)
            title_button.hide()
            new_checkbox.hide()
            delet_button.hide()         
        else:
            database.done_update(id, 0)
            title_button.hide()
            new_checkbox.hide()
            delet_button.hide()
       
        self.readFromDatabase()
    
    def add_newdatabase(self):
        title = self.ui.title_lineEdit.text()
        desc = self.ui.description_lineEdit.text()
        time = self.ui.time_lineEdit.text()
        date = self.ui.date_lineEdit.text()

        if self.ui.checkBox.isChecked():
            isdone = 1
        else:
            isdone = 0
        
        if self.ui.priorite_checkBox.isChecked():
            pr = 1
        else:
            pr = 0

        result = database.getAll()
        id_number = 1
        for i in range(len(result)):
            if id_number == result[i][0]:
                id_number +=1
            elif id_number != result[i][0]:
                break    
        
        database.add(id_number, title , desc, isdone, time, date, pr)

        self.readFromDatabase()
        
        self.ui.priorite_checkBox.setChecked(False)
        self.ui.checkBox.setChecked(False)
        self.ui.title_lineEdit.setText('')
        self.ui.description_lineEdit.setText('')  
        self.ui.time_lineEdit.setText('')
        self.ui.date_lineEdit.setText('')
    
    def delet_task(self, id, title_button, new_checkbox , delet_button):
        
        database.delet_fromdatabase(id)
        title_button.hide()
        new_checkbox.hide()
        delet_button.hide()
        #self.readFromDatabase()

    def showing_details(self,title,description,time,date):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(f'{title}')
        msg_box.setText(f'Description: {description} \nTime: {time} \nDate: {date}')
        msg_box.exec()

app = QApplication([])
window = MainWindow()
app.exec()        