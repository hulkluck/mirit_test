# -*- coding: utf-8 -*-
from datetime import datetime


class OpenFile:
    """Родительский класс. Открывает файл и позволяет использовать его дочерним классам"""

    def __init__(self, file_path):
        with open(file_path) as fd:
            lines = fd.readlines()
            self.lines = lines


class Convertor(OpenFile):
    """Класс преобразования данных в словари и списки. Реализует так-же вывод на печать и запись в файл"""

    def base_converted(self):
        variable = 0
        converted_dictionary = {}

        while variable < len(self.lines):
            if 'committer' in self.lines[variable]:
                line_committer = [x.strip()
                                  for x in self.lines[variable].split(':')]
                line_timestamp = [x.strip()
                                  for x in self.lines[variable+1].split(':')]
                line_revno = [x.strip()
                              for x in self.lines[variable-1].split(':')]

                converted_dictionary[line_revno[1]] = {
                    line_committer[1]: line_timestamp}

            variable += 1

        intermediate_list = converted_dictionary.values()

        return intermediate_list

    def get_converted_dictionary(self):
        variable = 0
        converted_dictionary = {}

        while variable < len(self.lines):
            if 'committer' in self.lines[variable]:
                line_committer = [x.strip()
                                  for x in self.lines[variable].split(':')]
                line_timestamp = [x.strip()
                                  for x in self.lines[variable+1].split(':')]
                line_revno = [x.strip()
                              for x in self.lines[variable-1].split(':')]

                converted_dictionary[line_revno[1]] = {
                    line_committer[1]: line_timestamp}

            variable += 1

        return converted_dictionary

    def get_dict_count_comment(self):
        variable = 0
        dict_count_comment = {}
        inter_list = self.base_converted()

        while variable < len(inter_list):

            if inter_list[variable].keys()[0] in dict_count_comment:
                dict_count_comment[inter_list[variable].keys()[0]] += 1
            else:
                dict_count_comment[inter_list[variable].keys()[0]] = 1

            variable += 1

        return dict_count_comment

    def get_list_committer(self):
        variable = 0
        list_committer = []
        inter_list = self.base_converted()

        while variable < len(inter_list):
            if inter_list[variable].keys()[0] not in list_committer:
                list_committer.append(inter_list[variable].keys()[0])
            variable += 1

        return list_committer

    def get_list_date_res(self):

        variable = 0
        list_date_res = {}
        inter_list = self.base_converted()
        list_committer = self.get_list_committer()

        while variable < len(list_committer):

            for i in inter_list:
                k = i.values()[0]
                l = k[1]
                n = l.split()[1]
                g = datetime.strptime(n, "%Y-%m-%d").year

                if i.keys()[0] == list_committer[variable]:
                    if g in list_date_res:
                        list_date_res[g] += 1
                    else:
                        list_date_res[g] = 1

            variable += 1
        return list_date_res

    def get_list_date(self):

        variable = 0
        list_date = {}
        inter_list = self.base_converted()
        list_committer = self.get_list_committer()

        while variable < len(list_committer):
            list_date[list_committer[variable]] = list()

            for i in inter_list:
                k = i.values()[0]
                l = k[1]
                n = l.split()[1]
                g = datetime.strptime(n, "%Y-%m-%d").year

                if i.keys()[0] == list_committer[variable]:
                    list_date[list_committer[variable]].append(g)

            variable += 1
        return list_date

    def get_list_full_date(self):

        variable = 0
        list_full_date = {}
        inter_list = self.base_converted()
        list_committer = self.get_list_committer()

        while variable < len(list_committer):
            list_full_date[list_committer[variable]] = list()

            for i in inter_list:
                k = i.values()[0]
                l = k[1]
                n = l.split()[1]
                m = datetime.strptime(n, "%Y-%m-%d").date()

                if i.keys()[0] == list_committer[variable]:
                    list_full_date[list_committer[variable]].append(m)

            variable += 1
        return list_full_date

    def printed(self):

        rezult = {}
        month_rezult = {}
        rez_date = {}
        count_year_commit = []
        variable = 0
        rez_full_date = {}
        dict_count_comment = self.get_dict_count_comment()
        converted_dictionary = self.get_converted_dictionary()
        list_date = self.get_list_date()
        list_date_res = self.get_list_date_res()
        list_full_date = self.get_list_full_date()

        file = open('rezult.txt', 'w')
        file.write('Статистика: \n')
        file.write('-------------------------------------------\n')

        for key, value in dict_count_comment.items():
            rezult_percent = 100 * float(value) / \
                float(len(converted_dictionary))
            print('Никнейм: ' + str(key) + ' - ' +
                  'К/коммитов: ' + str(value) + ' процент от всех коммитов ' + str(rezult_percent)[:4] + ' %')
            print('-----------------------------')

            file.write('Никнейм: ' + str(key) + ' - ' +
                       'К/коммитов: ' + str(value) + ' процент от всех коммитов ' + str(rezult_percent)[:4] + ' % \n')
        file.write('\n')
        file.write('Статистика по годам: \n')
        file.write('-------------------------------------------\n')

        while variable < len(list_date):
            rez_date.clear()
            rez_full_date.clear()
            for i in list_date.values()[variable]:

                if i in rez_date:
                    rez_date[i] += 1
                else:
                    rez_date[i] = 1

            rezult = {list_date.keys()[variable]: rez_date}
            count_year_commit = rezult.values()[0]
            print('Статистика по годам: \n')
            print('-------------------------------------------\n')
            print(rezult)
            file.write('Никнейм: ' + str(rezult.keys()[0]) + '\n\n')
            file.write('Разбивка по годам \n' + str(rezult.values()
                                                    [0]) + '\n\n' + 'В процентах по годам: \n')

            for i in list_date_res.keys():
                for j in count_year_commit.keys():
                    if i == j:
                        p = 100 * \
                            float(count_year_commit[j]) / list_date_res[i]
                        print(str(j) + ' - ' + str(p)[:4] + ' %')
                        file.write(str(j) + ' - ' + str(p)[:4] + ' %\n')

            file.write('\n')
            c = max(list_full_date.values()[variable])
            user = list_full_date.keys()[variable]

            for i in list_full_date[user]:

                if c.month == i.month and c.year == i.year:
                    if i.month in rez_full_date:
                        rez_full_date[i.month] += 1
                    else:
                        rez_full_date[i.month] = 1
                elif c.month - 1 == i.month and c.year == i.year:
                    if i.month in rez_full_date:
                        rez_full_date[i.month] += 1
                    else:
                        rez_full_date[i.month] = 1
                elif c.month - 2 == i.month and c.year == i.year:
                    if i.month in rez_full_date:
                        rez_full_date[i.month] += 1
                    else:
                        rez_full_date[i.month] = 1

            month_rezult = {list_full_date.keys()[variable]: rez_full_date}
            file.write('Дата последнего коммита: ' + str(c) + '\n')
            print('Дата последнего коммита: ' + str(c))
            file.write('Колличество коммитов за последние 3 месяца с разбивкой по месяцам:\n' +
                       str(month_rezult.values()[0]) + '\n')
            print('Колличество коммитов за последние 3 месяца с разбивкой по месяцам: ' +
                  str(month_rezult.values()[0]))
            file.write('-------------------------------------------\n\n')
            variable += 1

        file.close


if __name__ == '__main__':

    file_path = raw_input('Введите путь к фалу: ')
    result = Convertor(file_path)  # Создаем экземпляр класса
    print(result.printed())  # Записываем в файл и выводим на печать
