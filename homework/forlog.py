import logging

loggerE = logging.getLogger("Errors")
loggerE.setLevel(logging.ERROR)
formatter = logging.Formatter("%(filename)s %(name)s %(funcName)s [%(asctime)s]  %(message)s")
loggerI = logging.getLogger("Info")
loggerI.setLevel(logging.INFO)
