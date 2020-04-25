import logging
import csv
import os.path
from homework.forlog import loggerE, loggerI, formatter


class CheckName:

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):

        if instance.created:
            loggerE.error("This Patient is created")
            raise AttributeError
        if type(value) != str:
            loggerE.error("wrong type")
        count = 0
        for a in value:
            if 47 < ord(a) < 58:
                count = count + 1
        if count > 0:
            loggerE.error("Name contain numbers")
            raise ValueError()
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name


class СheckBday:
    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if type(value) != str:
            loggerE.error("wrong type")
        count = 0
        for a in value:
            if 47 < ord(a) < 58:
                count = count + 1
        if count != 8:
            loggerE.error("wrong type")
            raise ValueError("Bad number")
        year = "" + value[0:4]

        month = ""
        for a in value[4:len(value) - 2]:
            if not (a == "-") and not (a == " ") and not (a == "."):
                month = month + a
        day = "" + value[len(value) - 2:len(value)]

        year = year + "-" + month + "-" + day
        if instance.created:
            loggerI.info("Данные успешно обновлены")
        instance.__dict__[self.name] = year

    def __set_name__(self, owner, name):
        self.name = name


class CheckPhone:
    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if type(value) != str:
            loggerE.error("wrong type")
        if value is not None:
            str1 = ""
            flag = False
            count = 0
            for a in value:
                if 47 < ord(a) < 58:
                    count = count + 1
            if count < 11 or count > 11:
                loggerE.error("Check your number again")
                raise ValueError("error numbers")
            if value[0] == "+":
                str1 = str1 + "8"
                flag = True
            else:
                str1 = str1 + "8"
            if value[0] != "8" and value[0] != "7" and value[0:2] != "+7":
                loggerE.error("number starts with (8) or (7)")
                raise ValueError()
            if flag:
                for a in range(2, len(value)):
                    if 58 > ord(value[a]) > 47:
                        str1 = str1 + value[a]
            else:
                for a in range(1, len(value)):
                    if 58 > ord(value[a]) > 47:
                        str1 = str1 + value[a]
            instance.__dict__[self.name] = str1
            if instance.created:
                loggerI.info("Данные успешно обновлены")

    def __set_name__(self, owner, name):
        self.name = name


class Checkdoctype:
    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if value is not None:
            if type(value) != str:
                loggerE.error("wrong type2")
            if len(value) < 7:
                loggerE.error("small name of type")
            if value != "паспорт" and value != "заграничный паспорт" and value != "водительское удостоверение":
                loggerE.error("Не опознанный тип")
                raise ValueError("not")
            if instance.created:
                loggerI.info("Данные успешно обновлены")
            instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name


class Checkdocnumber:
    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if value is not None:
            if type(value) != str:
                loggerE.error("wrong type3")
            count = 0
            for a in value:
                if 47 < ord(a) < 58:
                    count = count + 1
            if count != 9 and count != 10:
                loggerE.error("wrong type")
                raise ValueError("Bad number")
            if value is not None:
                str1 = ""
                for a in value:
                    if a != " " and a != "-" and a != "/":
                        str1 = str1 + a
                if instance.created:
                    loggerI.info("Данные успешно обновлены")
                instance.__dict__[self.name] = str1

    def __set_name__(self, owner, name):
        self.name = name


class Patient:
    created = False
    first_name = CheckName()
    last_name = CheckName()
    birth_date = СheckBday()
    phone = CheckPhone()
    document_type = Checkdoctype()
    document_id = Checkdocnumber()
    handler1 = logging.FileHandler('mistakes.txt', 'a', 'utf-8')
    handler1.setFormatter(formatter)
    loggerE.addHandler(handler1)
    handler2 = logging.FileHandler('Info.txt', 'a', 'utf-8')
    handler2.setFormatter(formatter)
    loggerI.addHandler(handler2)

    def __init__(self, first_name=None, last_name=None, birth_date=None, phone=None, document_type=None,
                 document_id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.phone = phone
        self.document_type = document_type
        self.document_id = document_id
        loggerI.info("you create a new Patient")
        self.created = True
        self._saved = False

    @staticmethod
    def create(*args):
        return Patient(*args)

    def save(self):
        if not self._saved:
            patient = [self.first_name, self.last_name, self.birth_date, self.phone, self.document_type,
                       self.document_id]
            FILENAME = "patiens.csv"
            with open(FILENAME, "a", newline="", encoding='utf-8') as file:
                writer = csv.writer(file)
                # for a in self.patient:
                writer.writerow(patient)
                self._saved = True
                loggerI.info("Patient succesfully created")

    def __str__(self):
        return f"Patient: {self.first_name, self.last_name, self.birth_date, self.phone, self.document_type, self.document_id}"

    def __del__(self):
        self.handler2.close()
        self.handler1.close()


class PatientCollection:
    value1 = 0
    islim = False

    def __init__(self, path_to_file):
        if not os.path.exists(path_to_file):
            raise ValueError("this file doesnt exist")

    def __iter__(self):
        with open('patiens.csv', 'r', encoding='utf-8') as File:
            reader = csv.reader(File)
            for row in reader:
                if self.value1 > 0 or self.islim == False:
                    a = Patient(*row)
                    self.value1 = self.value1 - 1
                    yield a

    def limit(self, value):
        self.islim = True
        self.value1 = value
        return self.__iter__()
