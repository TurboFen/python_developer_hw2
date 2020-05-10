import logging
import csv
import os.path
import pymysql
from homework.check import loggerE, loggerI, formatter, handler1, handler2


def my_logging_decorator(func):
    def wrapper(self, instance, value):
        try:
            func(self, instance, value)
        except ValueError:
            loggerE.error("Error")
            raise ValueError
        except AssertionError:
            loggerE.error("Error")
            raise AssertionError
        else:
            if instance.created:
                loggerI.info("Данные успешно обновлены")

    return wrapper


def my_logging_decorator_patient(func):
    def wrapper(self, first_name, last_name, birth_date, phone, document_type, document_id):
        func(self, first_name, last_name, birth_date, phone, document_type, document_id)
        loggerI.info(self.logi)
        self.logi = ""

    return wrapper


def my_logging_decorator_save(func):
    def wrapper(self):
        func(self)
        loggerI.info(self.logi)
        self.logi = ""

    return wrapper


class CheckName:

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    @my_logging_decorator
    def __set__(self, instance, value):

        if instance.created:
            raise AttributeError
        if type(value) != str:
            raise ValueError()
        count = 0
        for a in value:
            if 47 < ord(a) < 58:
                count = count + 1
        if count > 0:
            raise ValueError()
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name


class СheckBday:
    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    @my_logging_decorator
    def __set__(self, instance, value):
        if type(value) != str:
            raise ValueError()
        count = 0
        for a in value:
            if 47 < ord(a) < 58:
                count = count + 1
        if count != 8:
            raise ValueError("Bad number")
        year = "" + value[0:4]

        month = ""
        for a in value[4:len(value) - 2]:
            if not (a == "-") and not (a == " ") and not (a == "."):
                month = month + a
        day = "" + value[len(value) - 2:len(value)]

        year = year + "-" + month + "-" + day
        if instance.created:
            instance.logi = "Данные успешно обновлены"
        instance.__dict__[self.name] = year

    def __set_name__(self, owner, name):
        self.name = name


class CheckPhone:
    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    @my_logging_decorator
    def __set__(self, instance, value):
        if type(value) != str:
            raise ValueError
        if value is not None:
            str1 = ""
            flag = False
            count = 0
            for a in value:
                if 47 < ord(a) < 58:
                    count = count + 1
            if count < 11 or count > 11:
                raise ValueError
            if value[0] == "+":
                str1 = str1 + "8"
                flag = True
            else:
                str1 = str1 + "8"
            if value[0] != "8" and value[0] != "7" and value[0:2] != "+7":
                raise ValueError
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
                instance.logi = "Данные успешно обновлены"

    def __set_name__(self, owner, name):
        self.name = name


class Checkdoctype:
    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    @my_logging_decorator
    def __set__(self, instance, value):
        if value is not None:
            if type(value) != str:
                raise ValueError
            if len(value) < 7:
                raise ValueError
            if value != "паспорт" and value != "заграничный паспорт" and value != "водительское удостоверение":
                raise ValueError
            if instance.created:
                instance.logi = "Данные успешно обновлены"
            instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name


class Checkdocnumber:
    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    @my_logging_decorator
    def __set__(self, instance, value):
        if value is not None:
            if type(value) != str:
                raise ValueError
            count = 0
            for a in value:
                if 47 < ord(a) < 58:
                    count = count + 1
            if count != 9 and count != 10:
                raise ValueError
            if value is not None:
                str1 = ""
                for a in value:
                    if a != " " and a != "-" and a != "/":
                        str1 = str1 + a
                if instance.created:
                    instance.logi = "Данные успешно обновлены"
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
    logi = ""

    @my_logging_decorator_patient
    def __init__(self, first_name, last_name, birth_date, phone, document_type, document_id):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.phone = phone
        self.document_type = document_type
        self.document_id = document_id
        self.logi = "you create a new Patient"
        self.created = True
        self._saved = False

    @staticmethod
    def create(first_name, last_name, birth_date, phone, document_type, document_id):
        return Patient(first_name, last_name, birth_date, phone, document_type, document_id)

    @my_logging_decorator_save
    def save(self):
        if not self._saved:
            var = pymysql.connect(host='localhost', port=3306, user='root', passwd='passwd',
                                  db='forpat')
            conn = var.cursor(pymysql.cursors.DictCursor)
            sql = "INSERT INTO patiens (first_name, last_name, birth_date, phone, document_type, document_id) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (self.first_name, self.last_name, self.birth_date, self.phone, self.document_type, self.document_id)
            conn.execute(sql, val)
            self._saved = True
            self.logi = "Patient succesfully saved"
            var.commit()
            conn.close()
            var.close()

    def __str__(self):
        return f"Patient: {self.first_name, self.last_name, self.birth_date, self.phone, self.document_type, self.document_id}"


class PatientCollection:
    value1 = 0
    islim = False

    def __init__(self):
        pass

    def __iter__(self):
        var = pymysql.connect(host='localhost', port=3306, user='root', passwd='Vfkmdbyfb<ehfnbyjk.,znlheulheuf88',
                              db='forpat')
        conn = var.cursor(pymysql.cursors.DictCursor)
        conn.execute("SELECT * FROM patiens")
        rows = conn.fetchall()
        for row in rows:
            if self.value1 > 0 or self.islim == False:
                var.commit()
                a = Patient(**row)
                self.value1 = self.value1 - 1
                yield a
        conn.close()
        var.close()

    def limit(self, value):
        self.islim = True
        self.value1 = value
        return self.__iter__()
