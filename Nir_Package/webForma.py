
from PyQt5 import QtCore, QtGui, QtWidgets, Qt, QtWebEngineWidgets
from PyQt5.QtCore import Qt, QFile, QFileInfo, QTextStream
from PyQt5.QtWidgets import (QMainWindow, QTextEdit,QAction, QFileDialog, QApplication,QMenuBar)
class webForm(QtWidgets.QDialog):
    def __init__(self, parent=None, selectedText = ""):
        QtWidgets.QDialog.__init__(self, parent)
        self.parent = parent
        self.selectedText = selectedText

        self.initUI()
        self.show_web_view()

        #self.textEdit.keyPressEvent(self, QtCore.Qt.Key_Return)
        #self.textEdit.textChanged.connect(self.show_web_view)
        #self.textEdit.viewportEvent.connect(self.enter_checker)
        #self.show_web_view()

    def initUI(self):
        self.setObjectName("MathJax helper")
        self.resize(1000, 400)
        self.setMinimumSize(QtCore.QSize(1000, 400))
        self.setMaximumSize(QtCore.QSize(1400, 700))
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        #self.lineEdit_3 = QtWidgets.QLineEdit(self)
        #self.lineEdit_3.setObjectName("lineEdit_3")
        # self.menu = QtWidgets.QMenuBar(self)
        # self.file = self.menu.addMenu("File")
        # self.file.addAction("Open")
        # self.file.addAction("Exit")
        # self.gridLayout_4.addWidget(self.menu, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_4, 0, 0, 1, 3)
        self.textEdit = QtWidgets.QTextEdit(self)
        font = QtGui.QFont()
        font.setFamily("Constantia")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 1, 0, 1, 1)
        self.line = QtWidgets.QFrame(self)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 1, 1, 1, 1)
        self.webView = QtWebEngineWidgets.QWebEngineView(self)
        self.webView.setMinimumSize(QtCore.QSize(400, 300))
        self.webView.setMaximumSize(QtCore.QSize(400, 700))
        self.webView.setUrl(QtCore.QUrl("about:blank"))
        self.webView.setObjectName("webView")
        self.gridLayout.addWidget(self.webView, 1, 2, 1, 1)
        self.line_4 = QtWidgets.QFrame(self)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.gridLayout.addWidget(self.line_4, 1, 3, 1, 1)
        self.line_2 = QtWidgets.QFrame(self)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 2, 0, 1, 1)
        self.line_3 = QtWidgets.QFrame(self)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout.addWidget(self.line_3, 2, 2, 1, 1)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.textEdit.keyPressEvent = self.handleEditorKeyPress



    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MathJax helper", "MathJax helper"))

    def handleEditorKeyPress(self,qKeyEvent):
        #print(qKeyEvent.key())
        if qKeyEvent.key() == QtCore.Qt.Key_Return:
            self.show_web_view()
        return QTextEdit.keyPressEvent(self.textEdit, qKeyEvent)

    def show_web_view(self):

        pageSourcePart1 = r"""<html><head>
            <script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
            </head><body>
            <p><mathjax>"""
        if self.selectedText != "":
            self.textEdit.setText(self.selectedText)
            self.selectedText = ""
        pageSourcePart2 = ""
        pageSourcePart3 = """</mathjax></p>
                            </body></html>"""


        # Создаём временный файл и записываем в него формулы
        # далее этот файл открывается в webView, чтобы наглядно был виден mathJax

        formulas = self.textEdit.toPlainText().splitlines()
        for i,line in enumerate(formulas):
            formulas[i] = "<p>" + line + "</p> "
            pageSourcePart2 = pageSourcePart2 + formulas[i] + "\n"


        tempFile = QFile('mathjax.html')
        tempFile.open(QFile.WriteOnly)
        stream = QTextStream(tempFile)
        stream << (pageSourcePart1 + pageSourcePart2 + pageSourcePart3)
        tempFile.close()
        fileUrl = QtCore.QUrl.fromLocalFile(QFileInfo(tempFile).canonicalFilePath())
        self.webView.setUrl(fileUrl)


from PyQt5 import QtWebEngineWidgets
