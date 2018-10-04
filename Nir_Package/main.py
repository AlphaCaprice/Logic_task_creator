#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
# Импортируем наш интерфейс из файла
sys.path.append(r'/NIR_new')
import window, table, datetime, textWork, webForma
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QMainWindow, QTextEdit,QAction, QFileDialog, QApplication, QToolBar)


class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = window.Ui_MainWindow()
        self.ui.setupUi(self)
        self.filename = ""

        self.initUI()

        # Здесь прописываем событие нажатия на кнопку
        self.ui.pushButton.clicked.connect(self.create_task)

    def initUI(self):
        self.initMenubar()
        self.initToolbar()
        self.initFormatBar()
        self.ui.textEdit.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.textEdit.customContextMenuRequested.connect(self.context)



    def initToolbar(self):

        self.ui.cutAction = QtWidgets.QAction(QtGui.QIcon("icons/cut.png"), "Cut to clipboard", self)
        self.ui.cutAction.setStatusTip("Delete and copy text to clipboard")
        self.ui.cutAction.setShortcut("Ctrl+X")
        self.ui.cutAction.triggered.connect(self.ui.textEdit.cut)

        self.ui.copyAction = QtWidgets.QAction(QtGui.QIcon("icons/copy.png"), "Copy to clipboard", self)
        self.ui.copyAction.setStatusTip("Copy text to clipboard")
        self.ui.copyAction.setShortcut("Ctrl+C")
        self.ui.copyAction.triggered.connect(self.ui.textEdit.copy)

        self.ui.pasteAction = QtWidgets.QAction(QtGui.QIcon("icons/paste.png"), "Paste from clipboard", self)
        self.ui.pasteAction.setStatusTip("Paste text from clipboard")
        self.ui.pasteAction.setShortcut("Ctrl+V")
        self.ui.pasteAction.triggered.connect(self.ui.textEdit.paste)

        self.ui.undoAction = QtWidgets.QAction(QtGui.QIcon("icons/undo.png"), "Undo last action", self)
        self.ui.undoAction.setStatusTip("Undo last action")
        self.ui.undoAction.setShortcut("Ctrl+Z")
        self.ui.undoAction.triggered.connect(self.ui.textEdit.undo)

        self.ui.redoAction = QtWidgets.QAction(QtGui.QIcon("icons/redo.png"), "Redo last undone thing", self)
        self.ui.redoAction.setStatusTip("Redo last undone thing")
        self.ui.redoAction.setShortcut("Shift+Z")
        self.ui.redoAction.triggered.connect(self.ui.textEdit.redo)

        self.ui.dateTimeAction = QtWidgets.QAction(QtGui.QIcon("icons/calender.png"), "Insert current date/time", self)
        self.ui.dateTimeAction.setStatusTip("Insert current date/time")
        self.ui.dateTimeAction.setShortcut("Ctrl+D")
        self.ui.dateTimeAction.triggered.connect(datetime.DateTime(self).show)

        self.ui.imageAction = QtWidgets.QAction(QtGui.QIcon("icons/image.png"), "Insert image", self)
        self.ui.imageAction.setStatusTip("Insert image")
        self.ui.imageAction.setShortcut("Ctrl+Shift+I")
        self.ui.imageAction.triggered.connect(self.insertImage)

        self.ui.tableAction = QtWidgets.QAction(QtGui.QIcon("icons/table.png"), "Insert table", self)
        self.ui.tableAction.setStatusTip("Insert table")
        self.ui.tableAction.setShortcut("Ctrl+T")
        self.ui.tableAction.triggered.connect(table.Table(self).show)

        self.ui.webAction = QtWidgets.QAction(QtGui.QIcon("icons/help.png"), "MathJax helper", self)
        self.ui.webAction.setStatusTip("Show mathJax helper")
        self.ui.webAction.triggered.connect(self.init_webForma)
        #self.ui.webAction.triggered.connect(webForma.webForm(self).show)

        self.ui.toolBar.addAction(self.ui.tableAction)

        self.ui.toolBar.addAction(self.ui.actionOpen)
        self.ui.toolBar.addAction(self.ui.actionNew)
        self.ui.toolBar.addAction(self.ui.actionSave)

        self.ui.toolBar.addSeparator()

        self.ui.toolBar.addAction(self.ui.cutAction)
        self.ui.toolBar.addAction(self.ui.copyAction)
        self.ui.toolBar.addAction(self.ui.pasteAction)
        self.ui.toolBar.addAction(self.ui.undoAction)
        self.ui.toolBar.addAction(self.ui.redoAction)

        self.ui.toolBar.addSeparator()
        self.ui.toolBar.addAction(self.ui.tableAction)
        self.ui.toolBar.addAction(self.ui.dateTimeAction)
        self.ui.toolBar.addAction(self.ui.imageAction)
        self.ui.toolBar.addAction(self.ui.webAction)

        self.addToolBarBreak()

    def initMenubar(self):

        self.ui.actionNew.setIcon(QtGui.QIcon("icons/new.png"))
        self.ui.actionNew.setShortcut("Ctrl+N")
        self.ui.actionNew.setStatusTip("Create a new document")
        self.ui.actionNew.triggered.connect(self.file_new)

        self.ui.actionOpen.setIcon(QtGui.QIcon("icons/open.png"))
        self.ui.actionOpen.setStatusTip("Open existing document")
        self.ui.actionOpen.setShortcut("Ctrl+O")
        self.ui.actionOpen.triggered.connect(self.file_open)

        self.ui.actionSave.setIcon(QtGui.QIcon("icons/save.png"))
        self.ui.actionSave.setStatusTip("Save document")
        self.ui.actionSave.setShortcut("Ctrl+S")
        self.ui.actionSave.triggered.connect(self.file_save)

        self.setWindowIcon(QtGui.QIcon("icons/icon.png"))

    def initFormatBar(self):
        self.ui.formatbar = self.addToolBar("Format")

        self.ui.fontBox = QtWidgets.QFontComboBox(self)
        self.ui.fontBox.currentFontChanged.connect(lambda font: self.ui.textEdit.setCurrentFont(font))

        self.ui.fontSize = QtWidgets.QSpinBox(self)
        # Will display " pt" after each value
        self.ui.fontSize.setSuffix(" pt")
        self.ui.fontSize.valueChanged.connect(lambda size: self.ui.textEdit.setFontPointSize(size))
        self.ui.fontSize.setValue(14)

        self.ui.fontColor = QtWidgets.QAction(QtGui.QIcon("icons/font-color.png"), "Change font color", self)
        self.ui.fontColor.triggered.connect(self.fontColorChanged)

        self.ui.boldAction = QtWidgets.QAction(QtGui.QIcon("icons/bold.png"), "Bold", self)
        self.ui.boldAction.setShortcut("Ctrl+B")
        self.ui.boldAction.setStatusTip("Ctrl+B")
        self.ui.boldAction.triggered.connect(self.bold)

        self.ui.italicAction = QtWidgets.QAction(QtGui.QIcon("icons/italic.png"), "Italic", self)
        self.ui.italicAction.setShortcut("Ctrl+I")
        self.ui.italicAction.setStatusTip("Ctrl+I")
        self.ui.italicAction.triggered.connect(self.italic)

        self.ui.underlAction = QtWidgets.QAction(QtGui.QIcon("icons/underline.png"), "Underline", self)
        self.ui.underlAction.setShortcut("Ctrl+U")
        self.ui.underlAction.setStatusTip("Ctrl+U")
        self.ui.underlAction.triggered.connect(self.underline)

        self.ui.mathJaxAction = QtWidgets.QAction(QtGui.QIcon("icons/mathJax.png"), "Insert mathJax formula", self)
        #self.ui.mathJaxAction.setFixedSize(100,100)
        #self.ui.mathJaxAction.setIconSize(QtCore.QSize(100,100))
        self.ui.mathJaxAction.triggered.connect(self.insertMathJax)
        self.ui.mathJaxAction.setShortcut("Ctrl+M")
        self.ui.mathJaxAction.setStatusTip("Ctrl+M")

        self.ui.toAction = QtWidgets.QAction(QtGui.QIcon("icons/to.png"), "to", self)
        self.ui.toAction.triggered.connect(self.logicTo)
        self.ui.toAction.setShortcut("Ctrl+4")
        self.ui.toAction.setStatusTip("Ctrl+4")

        self.ui.orAction = QtWidgets.QAction(QtGui.QIcon("icons/or.png"), "or", self)
        self.ui.orAction.triggered.connect(self.logicOr)
        self.ui.orAction.setShortcut("Ctrl+1")
        self.ui.orAction.setStatusTip("Ctrl+1")

        self.ui.andAction = QtWidgets.QAction(QtGui.QIcon("icons/and.png"), "and", self)
        self.ui.andAction.triggered.connect(self.logicAnd)
        self.ui.andAction.setShortcut("Ctrl+2")
        self.ui.andAction.setStatusTip("Ctrl+2")

        self.ui.notAction = QtWidgets.QAction(QtGui.QIcon("icons/not.png"), "not", self)
        self.ui.notAction.triggered.connect(self.logicNot)
        self.ui.notAction.setShortcut("Ctrl+3")
        self.ui.notAction.setStatusTip("Ctrl+3")

        self.ui.norAction = QtWidgets.QAction(QtGui.QIcon("icons/nor.png"), "nor", self)
        self.ui.norAction.triggered.connect(self.logicNor)
        self.ui.norAction.setShortcut("Ctrl+5")
        self.ui.norAction.setStatusTip("Ctrl+5")

        self.ui.leftRightArrowAction = QtWidgets.QAction(QtGui.QIcon("icons/leftrightarrow.png"), "leftrightarrow", self)
        self.ui.leftRightArrowAction.triggered.connect(self.logicLeftRightArrow)
        self.ui.leftRightArrowAction.setShortcut("Ctrl+6")
        self.ui.leftRightArrowAction.setStatusTip("Ctrl+6")

        self.ui.oplusAction = QtWidgets.QAction(QtGui.QIcon("icons/oplus.png"), "oplus", self)
        self.ui.oplusAction.triggered.connect(self.logicOplus)
        self.ui.oplusAction.setShortcut("Ctrl+7")
        self.ui.oplusAction.setStatusTip("Ctrl+7")

        self.ui.equivAction = QtWidgets.QAction(QtGui.QIcon("icons/equiv.png"), "equiv", self)
        self.ui.equivAction.triggered.connect(self.logicEquiv)
        self.ui.equivAction.setShortcut("Ctrl+8")
        self.ui.equivAction.setStatusTip("Ctrl+8")

        self.ui.nandAction = QtWidgets.QAction(QtGui.QIcon("icons/nand.png"), "nand", self)
        self.ui.nandAction.triggered.connect(self.logicNand)
        self.ui.nandAction.setShortcut("Ctrl+9")
        self.ui.nandAction.setStatusTip("Ctrl+9")

        self.ui.topAction = QtWidgets.QAction(QtGui.QIcon("icons/top.png"), "top", self)
        self.ui.topAction.triggered.connect(self.logicTop)

        self.ui.formatbar.addWidget(self.ui.fontBox)
        self.ui.formatbar.addWidget(self.ui.fontSize)

        self.ui.formatbar.addSeparator()

        self.ui.formatbar.addAction(self.ui.fontColor)

        self.ui.formatbar.addSeparator()

        self.ui.formatbar.addAction(self.ui.boldAction)
        self.ui.formatbar.addAction(self.ui.italicAction)
        self.ui.formatbar.addAction(self.ui.underlAction)

        self.ui.formatbar.addSeparator()

        self.ui.formatbar.addAction(self.ui.mathJaxAction)
        self.ui.formatbar.addAction(self.ui.orAction)
        self.ui.formatbar.addAction(self.ui.andAction)
        self.ui.formatbar.addAction(self.ui.notAction)
        self.ui.formatbar.addAction(self.ui.toAction)
        self.ui.formatbar.addAction(self.ui.norAction)
        self.ui.formatbar.addAction(self.ui.leftRightArrowAction)
        self.ui.formatbar.addAction(self.ui.oplusAction)
        self.ui.formatbar.addAction(self.ui.equivAction)
        self.ui.formatbar.addAction(self.ui.nandAction)
        self.ui.formatbar.addAction(self.ui.topAction)

        #self.ui.formatbar.setIconSize(QtCore.QSize(40,40))

    def create_task(self):
        #if not self.filename:
        self.filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File')[0]

        if self.filename:
            #my_file = open(r'C:\Users\Роман\Documents\Питон\NIR_new\text.txt', "w+")
            #text = self.ui.textEdit.toPlainText()
            with open(self.filename, "w+") as my_file:
                #textWork.reformat_file(self, my_file)
                textWork.reformat_file(self, my_file)
                my_file.close()

                popup = QtWidgets.QMessageBox(self)
                popup.setIcon(QtWidgets.QMessageBox.Warning)
                popup.setText("Task has been created!")
                popup.setStandardButtons(QtWidgets.QMessageBox.Ok)
                popup.setDefaultButton(QtWidgets.QMessageBox.Ok)
                popup.exec_()
            f = open(self.filename).readlines()
            f.pop(0)
            with open(self.filename, 'w') as F:
                F.writelines(f)
                F.close()

    def file_open(self):
        self.filename = QtWidgets.QFileDialog.getOpenFileName(self)[0]
        if not self.filename.endswith(".logic"):
            popup = QtWidgets.QMessageBox(self)
            popup.setIcon(QtWidgets.QMessageBox.Warning)
            popup.setText("File has wrong format!")
            popup.setStandardButtons(QtWidgets.QMessageBox.Ok)
            popup.setDefaultButton(QtWidgets.QMessageBox.Ok)
            popup.exec_()
            return
        if self.filename:
            with open(self.filename, "rt") as file:
                self.ui.textEdit.setText(file.read())
                file.close()

            with open(self.filename, "rt") as file:
                answers = file.readlines()
                lineNum = 0
                for num, i in enumerate(answers):
                    if i == "!!!ANSWERS!!!\n":
                        lineNum = num+1
                        break

                self.ui.lineEdit_6.setText((answers[lineNum + 0]).rstrip())
                self.ui.lineEdit_7.setText((answers[lineNum + 1]).rstrip())
                self.ui.lineEdit_8.setText((answers[lineNum + 2]).rstrip())
                self.ui.lineEdit_9.setText((answers[lineNum + 3]).rstrip())
                self.ui.lineEdit_10.setText((answers[lineNum + 4]).rstrip())
                self.ui.lineEdit_11.setText((answers[lineNum + 5]).rstrip())
                self.ui.lineEdit_12.setText((answers[lineNum + 6]).rstrip())
                self.ui.lineEdit_13.setText((answers[lineNum + 7]).rstrip())
                self.ui.lineEdit_14.setText((answers[lineNum + 8]).rstrip())
                self.ui.lineEdit_15.setText((answers[lineNum + 9]).rstrip())
                self.ui.lineEdit_16.setText((answers[lineNum + 10]).rstrip())
                self.ui.lineEdit_17.setText((answers[lineNum + 11]).rstrip())
                self.ui.lineEdit_18.setText((answers[lineNum + 12]).rstrip())
                self.ui.lineEdit_19.setText((answers[lineNum + 13]).rstrip())
                self.ui.lineEdit_20.setText((answers[lineNum + 14]).rstrip())

        # Удаление строки с ответами, которая хранится в файле и нужна для заполнения
        # Строк с ответами, но не должна отображаться в текстовом поле
        cursor = self.ui.textEdit.textCursor()
        line = ""
        while not (line.startswith("!!!")):
            cursor.movePosition(QtGui.QTextCursor.End)
            cursor.selectionStart()
            cursor.movePosition(QtGui.QTextCursor.StartOfLine,  QtGui.QTextCursor.KeepAnchor)
            line = cursor.selectedText()
            cursor.removeSelectedText()
        self.ui.textEdit.setTextCursor(cursor)

    def file_save(self):

        #cursor = self.ui.textEdit.textCursor()
        self.filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File')[0]

        if self.filename:

            # Append extension if not there yet
            if not self.filename.endswith(".logic"):
                self.filename += ".logic"

            # We just store the contents of the text file along with the
            # format in html, which Qt does in a very nice way for us
            with open(self.filename, "wt") as file:
                # Основной текст
                file.write(self.ui.textEdit.toHtml())

                # Заполнение строк с ответами
                file.write("\n"+"!!!ANSWERS!!!"+"\n")
                file.write(self.ui.lineEdit_6.text() + "\n")
                file.write(self.ui.lineEdit_7.text() + "\n")
                file.write(self.ui.lineEdit_8.text() + "\n")
                file.write(self.ui.lineEdit_9.text() + "\n")
                file.write(self.ui.lineEdit_10.text()+ "\n")
                file.write(self.ui.lineEdit_11.text() + "\n")
                file.write(self.ui.lineEdit_12.text() + "\n")
                file.write(self.ui.lineEdit_13.text() + "\n")
                file.write(self.ui.lineEdit_14.text() + "\n")
                file.write(self.ui.lineEdit_15.text() + "\n")
                file.write(self.ui.lineEdit_16.text() + "\n")
                file.write(self.ui.lineEdit_17.text() + "\n")
                file.write(self.ui.lineEdit_18.text() + "\n")
                file.write(self.ui.lineEdit_19.text() + "\n")
                file.write(self.ui.lineEdit_20.text() + "\n")

                file.close()
            # self.changesSaved = True

    def file_new(self):
        popup = QtWidgets.QMessageBox(self)

        popup.setIcon(QtWidgets.QMessageBox.Warning)

        popup.setText("Do you want to save your changes?")

        popup.setStandardButtons(QtWidgets.QMessageBox.Yes |
                                 QtWidgets.QMessageBox.No)

        popup.setDefaultButton(QtWidgets.QMessageBox.Yes)

        answer = popup.exec_()

        if answer == QtWidgets.QMessageBox.Yes:
            self.file_save()
        else:
            self.ui.textEdit.setPlainText("")
            self.ui.lineEdit_6.setText("")
            self.ui.lineEdit_7.setText("")
            self.ui.lineEdit_8.setText("")
            self.ui.lineEdit_9.setText("")
            self.ui.lineEdit_10.setText("")
            self.ui.lineEdit_11.setText("")
            self.ui.lineEdit_12.setText("")
            self.ui.lineEdit_13.setText("")
            self.ui.lineEdit_14.setText("")
            self.ui.lineEdit_15.setText("")
            self.ui.lineEdit_16.setText("")
            self.ui.lineEdit_17.setText("")
            self.ui.lineEdit_18.setText("")
            self.ui.lineEdit_19.setText("")
            self.ui.lineEdit_20.setText("")

    def closeEvent(self, event):
        popup = QtWidgets.QMessageBox(self)

        popup.setIcon(QtWidgets.QMessageBox.Warning)

        popup.setText("The document has been modified")

        popup.setInformativeText("Do you want to save your changes?")

        popup.setStandardButtons(QtWidgets.QMessageBox.Save |
                                 QtWidgets.QMessageBox.Cancel |
                                 QtWidgets.QMessageBox.Discard)

        popup.setDefaultButton(QtWidgets.QMessageBox.Save)

        answer = popup.exec_()

        if answer == QtWidgets.QMessageBox.Save:
            self.file_save()
        elif answer == QtWidgets.QMessageBox.Discard:
            event.accept()
        else:
            event.ignore()

    def init_webForma(self):
        cursor = self.ui.textEdit.textCursor()
        selectedText = cursor.selectedText()
        print(selectedText)
        self.webFormaUi = webForma.webForm(self, selectedText)
        self.webFormaUi.show()

    def insert_table(self):
        cursor = self.parent.text.textCursor()

        # Get the configurations
        rows = self.rows.value()

        cols = self.cols.value()

        if not rows or not cols:

            popup = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning,
                                          "Parameter error",
                                          "Row and column numbers may not be zero!",
                                          QtWidgets.QMessageBox.Ok,
                                          self)
            popup.show()

        else:

            padding = self.pad.value()

            space = self.space.value()

            # Set the padding and spacing
            fmt = QtGui.QTextTableFormat()

            fmt.setCellPadding(padding)

            fmt.setCellSpacing(space)

            # Inser the new table
            cursor.insertTable(rows, cols, fmt)

            self.close()

    def context(self, pos):

        # Grab the cursor
        cursor = self.ui.textEdit.textCursor()

        # Grab the current table, if there is one
        table = cursor.currentTable()

        # Above will return 0 if there is no current table, in which case
        # we call the normal context menu. If there is a table, we create
        # our own context menu specific to table interaction
        if table:

            menu = QtWidgets.QMenu(self)

            appendRowAction = QtWidgets.QAction("Append row", self)
            appendRowAction.triggered.connect(lambda: table.appendRows(1))

            appendColAction = QtWidgets.QAction("Append column", self)
            appendColAction.triggered.connect(lambda: table.appendColumns(1))

            removeRowAction = QtWidgets.QAction("Remove row", self)
            removeRowAction.triggered.connect(self.removeRow)

            removeColAction = QtWidgets.QAction("Remove column", self)
            removeColAction.triggered.connect(self.removeCol)

            insertRowAction = QtWidgets.QAction("Insert row", self)
            insertRowAction.triggered.connect(self.insertRow)

            insertColAction = QtWidgets.QAction("Insert column", self)
            insertColAction.triggered.connect(self.insertCol)

            mergeAction = QtWidgets.QAction("Merge cells", self)
            mergeAction.triggered.connect(lambda: table.mergeCells(cursor))

            # Only allow merging if there is a selection
            if not cursor.hasSelection():
                mergeAction.setEnabled(False)

            splitAction = QtWidgets.QAction("Split cells", self)

            cell = table.cellAt(cursor)

            # Only allow splitting if the current cell is larger
            # than a normal cell
            if cell.rowSpan() > 1 or cell.columnSpan() > 1:

                splitAction.triggered.connect(lambda: table.splitCell(cell.row(), cell.column(), 1, 1))

            else:
                splitAction.setEnabled(False)

            menu.addAction(appendRowAction)
            menu.addAction(appendColAction)

            menu.addSeparator()

            menu.addAction(removeRowAction)
            menu.addAction(removeColAction)

            menu.addSeparator()

            menu.addAction(insertRowAction)
            menu.addAction(insertColAction)

            menu.addSeparator()

            menu.addAction(mergeAction)
            menu.addAction(splitAction)

            # Convert the widget coordinates into global coordinates
            pos = self.mapToGlobal(pos)

            # Add pixels for the tool and formatbars, which are not included
            # in mapToGlobal(), but only if the two are currently visible and
            # not toggled by the user

            if self.ui.toolBar.isVisible():
                pos.setY(pos.y() + 45)

            # if self.formatbar.isVisible():
            #     pos.setY(pos.y() + 45)

            # Move the menu to the new position
            menu.move(pos)

            menu.show()

        else:
            self._normalMenu = self.ui.textEdit.createStandardContextMenu()
            self._normalMenu.addSeparator()
            self._normalMenu.addAction("MathJax Helper", self.init_webForma)
            self._normalMenu.exec_(self.focusWidget().mapToGlobal(pos))

            event = QtGui.QContextMenuEvent(QtGui.QContextMenuEvent.Mouse, QtCore.QPoint())
            self.ui.textEdit.contextMenuEvent(event)

    def removeRow(self):

        # Grab the cursor
        cursor = self.ui.textEdit.textCursor()

        # Grab the current table (we assume there is one, since
        # this is checked before calling)
        table = cursor.currentTable()

        # Get the current cell
        cell = table.cellAt(cursor)

        # Delete the cell's row
        table.removeRows(cell.row(), 1)

    def removeCol(self):

        # Grab the cursor
        cursor = self.ui.textEdit.textCursor()

        # Grab the current table (we assume there is one, since
        # this is checked before calling)
        table = cursor.currentTable()

        # Get the current cell
        cell = table.cellAt(cursor)

        # Delete the cell's column
        table.removeColumns(cell.column(), 1)

    def insertRow(self):

        # Grab the cursor
        cursor = self.ui.textEdit.textCursor()

        # Grab the current table (we assume there is one, since
        # this is checked before calling)
        table = cursor.currentTable()

        # Get the current cell
        cell = table.cellAt(cursor)

        # Insert a new row at the cell's position
        table.insertRows(cell.row(), 1)

    def insertCol(self):

        # Grab the cursor
        cursor = self.ui.textEdit.textCursor()

        # Grab the current table (we assume there is one, since
        # this is checked before calling)
        table = cursor.currentTable()

        # Get the current cell
        cell = table.cellAt(cursor)

        # Insert a new row at the cell's position
        table.insertColumns(cell.column(), 1)

    def insertImage(self):

        # Get image file name
        # PYQT5 Returns a tuple in PyQt5
        filename = \
        QtWidgets.QFileDialog.getOpenFileName(self, 'Insert image', ".", "Images (*.png *.xpm *.jpg *.bmp *.gif)")[0]

        if filename:

            # Create image object
            image = QtGui.QImage(filename)

            # Error if unloadable
            if image.isNull():

                popup = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                              "Image load error",
                                              "Could not load image file!",
                                              QtWidgets.QMessageBox.Ok,
                                              self)
                popup.show()

            else:

                cursor = self.ui.textEdit.textCursor()

                cursor.insertImage(image, filename)

    def fontColorChanged(self):

        # Get a color from the text dialog
        color = QtWidgets.QColorDialog.getColor()

        # Set it as the new text color
        self.ui.textEdit.setTextColor(color)

    def bold(self):

        if self.ui.textEdit.fontWeight() == QtGui.QFont.Bold:
            self.ui.textEdit.setFontWeight(QtGui.QFont.Normal)

        else:
            self.ui.textEdit.setFontWeight(QtGui.QFont.Bold)

    def italic(self):
        state = self.ui.textEdit.fontItalic()
        self.ui.textEdit.setFontItalic(not state)

    def underline(self):
        state = self.ui.textEdit.fontUnderline()
        self.ui.textEdit.setFontUnderline(not state)

    def insertMathJax(self):
        self.ui.textEdit.insertPlainText(r"\( \)")
        cursor = self.ui.textEdit.textCursor()
        cursor.movePosition(cursor.Left, False, 3)
        self.ui.textEdit.setTextCursor(cursor)
        return

    def logicTo(self):
        self.ui.textEdit.insertPlainText(r"\to")

    def logicOr(self):
        self.ui.textEdit.insertPlainText("\lor")

    def logicAnd(self):
        self.ui.textEdit.insertPlainText("\land")

    def logicNot(self):
        self.ui.textEdit.insertPlainText("\lnot")

    def logicNor(self):
        self.ui.textEdit.insertPlainText("\downarrow")

    def logicLeftRightArrow(self):
        self.ui.textEdit.insertPlainText("\leftrightarrow")

    def logicOplus(self):
        self.ui.textEdit.insertPlainText("\oplus")

    def logicEquiv(self):
        self.ui.textEdit.insertPlainText("\equiv")

    def logicNand(self):
        self.ui.textEdit.insertPlainText("\mid")

    def logicTop(self):
        self.ui.textEdit.insertPlainText(r"\top")

    # def EnablePairAnswers(self, state):
    #     self.ui.lineEdit.setEnabled(state)
    #     self.ui.lineEdit_2.setEnabled(state)
    #     self.ui.lineEdit_3.setEnabled(state)
    #     self.ui.lineEdit_4.setEnabled(state)
    #     self.ui.lineEdit_5.setEnabled(state)
    #     self.ui.lineEdit_5.setEnabled(state)
    #     self.ui.lineEdit_21.setEnabled(state)
    #     self.ui.lineEdit_22.setEnabled(state)
    #     self.ui.lineEdit_23.setEnabled(state)
    #     self.ui.lineEdit_24.setEnabled(state)
    #     self.ui.lineEdit_25.setEnabled(state)
    #     self.ui.lineEdit_26.setEnabled(state)
    #     self.ui.lineEdit_27.setEnabled(state)
    #     self.ui.lineEdit_28.setEnabled(state)
    #     self.ui.lineEdit_29.setEnabled(state)
    #     self.ui.lineEdit_30.setEnabled(state)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()

    sys.exit(app.exec_())
