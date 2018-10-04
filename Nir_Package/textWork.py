#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import re, itertools, collections
def reformat_file(self, file):
    left_answers = {self.ui.lineEdit.text(): self.ui.lineEdit_6.text(),
                    self.ui.lineEdit_2.text(): self.ui.lineEdit_7.text(),
                    self.ui.lineEdit_3.text(): self.ui.lineEdit_8.text(),
                    self.ui.lineEdit_4.text(): self.ui.lineEdit_9.text(),
                    self.ui.lineEdit_5.text(): self.ui.lineEdit_10.text()}

    right_answers = {self.ui.lineEdit_21.text(): self.ui.lineEdit_11.text(),
                     self.ui.lineEdit_22.text(): self.ui.lineEdit_12.text(),
                     self.ui.lineEdit_23.text(): self.ui.lineEdit_13.text(),
                     self.ui.lineEdit_24.text(): self.ui.lineEdit_14.text(),
                     self.ui.lineEdit_25.text(): self.ui.lineEdit_15.text(),
                     self.ui.lineEdit_26.text(): self.ui.lineEdit_16.text(),
                     self.ui.lineEdit_27.text(): self.ui.lineEdit_17.text(),
                     self.ui.lineEdit_28.text(): self.ui.lineEdit_18.text(),
                     self.ui.lineEdit_29.text(): self.ui.lineEdit_19.text(),
                     self.ui.lineEdit_30.text(): self.ui.lineEdit_20.text()}


    true_answers  = []  # Список вида [[левая часть, правая часть], [левая часть, правая часть]...]
    false_answers = []  # Список вида [[левая часть, правая часть], [левая часть, правая часть]...]
    amount_of_answers = int(self.ui.amountOfAnswers.currentText()) # Количество ответов в "одном". Имеется ввиду обычный, пары, тройки
    for key_left, value_left in left_answers.items():
        for key_right, value_right in right_answers.items():
            if key_left == key_right:
                if value_left != "" and value_right != "":
                    true_answers.append([value_left,value_right])
                    if [value_left,value_right] in false_answers:
                        false_answers.remove([value_left,value_right])
            else:
                if value_left != "" and value_right != "":
                    if [value_left, value_right] not in true_answers and [value_left, value_right] not in false_answers:
                        false_answers.append([value_left,value_right])

    pairs_of_true_answers = []
    pairs_of_false_answers = []
    true_answers.sort()
    false_answers.sort()
    #Составление всех возможных пар комбинаций из правильных ответов
    for i in itertools.combinations(true_answers, amount_of_answers):
        pairs_of_true_answers.append(i)
    # print("True Answers!")
    # for i in pairs_of_true_answers:
    #    print("".join(str(i[0][0]) + " - " + str(i[0][1]) + ", " + str(i[1][0]) + " - " + str(i[1][1])))
    # Составление всех возможных пар комбинаций из неверных ответов
    for i in itertools.combinations(false_answers, amount_of_answers):
        pairs_of_false_answers.append(i)
    # print("False Answers!")
    # for i in pairs_of_false_answers:
    #     print("".join(str(i[0][0]) + " - " + str(i[0][1]) + ", " + str(i[1][0]) + " - " + str(i[1][1])))
    # print("end!")
    # Удаление ответа, если пары, тройки взаимоисключающие
    # For ex нельзя допустить, чтобы (1-выполнимая, 1-невыполнимая) было ответом
    # Используется Counter,чтобы узнать количество первых ключей, если их меньше чем количетсво пар в ответе, то
    # Ответ удаляется
    if amount_of_answers > 1:
        j = 0
        while(i < len(pairs_of_false_answers)):
            answer = pairs_of_false_answers[j]
            counter = collections.Counter([i[0] for i in answer])
            if len(counter) != len(answer):
                pairs_of_false_answers.remove(answer)
            else:
                j += 1

    # Запись в файл текста задачи
    file.write(self.ui.textEdit.toHtml())

    # Создание выборки ответов
    file.write('\n')
    file.write("<multiplechoiceresponse>" + '\n')
    file.write('''<choicegroup label="ChoiceLabel" type="MultipleChoice" answer-pool="''' + self.ui.answersNumber.text() + '''">''' + '\n')

    # Правильные пары ответов как множество, чтобы хранить их в случайном порядке
    allAnswers = set()

    # re.sub(' +', '\;', value) нужен для замены обычных пробелов на \;  - это пробелы,
    # которые воспринимает mathJax в своём выражении типа \(...\), если будут обычные, то они просто сотрутся
    for answer in pairs_of_true_answers:
        str_temp = '''<choice correct="true">''' + " \("
        for one_pair in answer:
            str_temp += one_pair[0] + " " + self.ui.midSymbol.text() + " " + re.sub(' +', '\;', one_pair[1]) + ','
        str_temp = str_temp[:-1] # удаляет последнюю запятую
        str_temp += " \)</choice>" + '\n'
        allAnswers.add(str_temp)

    # Неправильные пары ответов
    for answer in pairs_of_false_answers:
        str_temp = '''<choice correct="false">''' + " \("
        for one_pair in answer:
            str_temp += one_pair[0] + " " + self.ui.midSymbol.text() + " " + re.sub(' +', '\;', one_pair[1]) + ','
        str_temp = str_temp[:-1] # удаляет последнюю запятую
        str_temp += " \)</choice>" + '\n'
        allAnswers.add(str_temp)

    for answer in allAnswers:
        file.write(answer)

    file.write("</choicegroup>" + '\n' + "</multiplechoiceresponse>" + '\n')



