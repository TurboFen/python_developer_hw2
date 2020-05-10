import logging

loggerE = logging.getLogger("Errors")
loggerE.setLevel(logging.ERROR)
formatter = logging.Formatter("%(filename)s %(name)s %(funcName)s [%(asctime)s]  %(message)s")
loggerI = logging.getLogger("Info")
loggerI.setLevel(logging.INFO)
handler1 = logging.FileHandler('mistakes.txt', 'a', 'utf-8')
handler1.setFormatter(formatter)
loggerE.addHandler(handler1)
handler2 = logging.FileHandler('Info.txt', 'a', 'utf-8')
handler2.setFormatter(formatter)
loggerI.addHandler(handler2)