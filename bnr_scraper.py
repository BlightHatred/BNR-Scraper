#!/usr/bin/env python
# coding: utf-8



from bs4 import BeautifulSoup as bs
from scraper import scraper
from config import confparser
import mysql.connector
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QWidget,  QLineEdit, QMainWindow,   QVBoxLayout, QTableView
import sys

#Importing scraper module, collecting data
title_date_content_list = scraper.scrapedata()

#Collecting authentication data for database, signing into database
sqlc = confparser.read_config()

mydb = mysql.connector.connect(**sqlc)

#Creating table (if needed)
mycursor = mydb.cursor()

sqltable = '''CREATE TABLE IF NOT EXISTS NEWS(
    TITLE VARCHAR(200),
    DATE VARCHAR(20),
    CONTENT TEXT(20000)
    )'''
mycursor.execute(sqltable)

# Adding data to the table in the database
for item in title_date_content_list:
    if "'" in item[2]:
        item[2] = item[2].replace("'", "`") 
    querystr = f"INSERT INTO NEWS(TITLE, DATE, CONTENT) VALUES ('{item[0]}', '{item[1]}', '{item[2]}')" 
    mycursor.execute(querystr)
 



#Creating the UI
class Table(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("News")
        self.resize(1200, 500)  
        self.layout = QVBoxLayout()
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)
        self.initUI2()
        
    def initUI2(self):
        rowcount = len(title_date_content_list)
        model = QStandardItemModel(rowcount, 3)
        model.setHorizontalHeaderLabels(['Title', 'Date', 'Content'])
        for item in title_date_content_list:
            row = title_date_content_list.index(item)
            for i in range(3):
                item2 = QStandardItem(item[i])
                model.setItem(row, i, item2)
        
        proxy_model_filter = QSortFilterProxyModel()
        proxy_model_filter.setSourceModel(model)
        proxy_model_filter.setFilterKeyColumn(1)
        proxy_model_filter.setFilterCaseSensitivity(Qt.CaseInsensitive)
        
        table = QTableView()
        table.setModel(proxy_model_filter)
        table.setSortingEnabled(True)

        for i in range(3):
            table.setColumnWidth(i, 400)
        
        lineedit = QLineEdit()
        lineedit.setPlaceholderText('Search news by date (DD.MM.YY)')
        lineedit.textChanged.connect(proxy_model_filter.setFilterRegExp)

        self.layout.addWidget(lineedit)
        self.layout.addWidget(table)


 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Table()
    window.show()
    sys.exit(app.exec_())







