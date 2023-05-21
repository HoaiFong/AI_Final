# Form implementation generated from reading ui file 'app.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
import yfinance as yf
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import load_model


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1102, 847)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(180, 60, 671, 121))
        font = QtGui.QFont()
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.groupBox = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(130, 240, 731, 371))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.label_2 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(90, 70, 281, 81))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.date = QtWidgets.QLineEdit(parent=self.groupBox)
        self.date.setGeometry(QtCore.QRect(330, 100, 251, 31))
        self.date.setObjectName("date")
        self.pushButton = QtWidgets.QPushButton(parent=self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(590, 100, 101, 31))
        self.pushButton.setObjectName("pushButton")
        self.label_3 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(10, 250, 311, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.lineEdit = QtWidgets.QLineEdit(parent=self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(320, 260, 251, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.label_4 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(580, 260, 55, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(330, 60, 211, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1102, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.pushButton.clicked.connect(self.data_pred)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Stock Price Prediction"))
        self.label_2.setText(_translate("MainWindow", "Nhập phiên đóng cửa:"))
        self.pushButton.setText(_translate("MainWindow", "OK"))
        self.label_3.setText(_translate("MainWindow", "Dự đoán giá phiên đóng cửa tiếp theo là:"))
        self.label_4.setText(_translate("MainWindow", "$"))
        self.label_5.setText(_translate("MainWindow", "Ví dụ: 2023-05-15"))

    def data_pred(self):
        end_date= self.date.text()

        model_RNN = load_model('stock.h5')
        scaler = MinMaxScaler(feature_range=(0,1))
        #Get the quote
        quote = yf.download('GOOGL', start='2013-05-15', end=end_date)
        #Create a dataframe
        new_df = quote.filter(['Close'])
        #Get teh last 60 day closing price values and convert the dataframe to an array 
        last_60_days = new_df[-60:].values
        #Scale the data to be values between 0 and 1
        last_60_days_scaled = scaler.fit_transform(last_60_days)
        #Create an emty list
        xx_test = []
        #append the past 60 days
        xx_test.append(last_60_days_scaled)
        #convert the xx_test dataset to a numpy array
        xx_test = np.array(xx_test)
        #reshape the data 
        xx_test = np.reshape(xx_test,(xx_test.shape[0], xx_test.shape[1], 1))
        #get the predicted scaled price 
        pred_price =  model_RNN.predict(xx_test)
        #undo the scaling 
        pred_price = scaler.inverse_transform(pred_price)
        pred_price = pred_price[0][0]
        
        self.lineEdit.setText(str(pred_price))
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
