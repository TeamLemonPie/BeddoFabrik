from datetime import datetime

class LogLevel(object):
	DEBUG = "DEBUG"
	INFO = "INFO"
	WARNING = "WARNING"
	ERROR = "ERROR"


class Logger(object):
	DATE_FORMAT = "%d.%m.%Y - %H:%M:%S"

	@staticmethod
	def log(logLevel, message):
		date = datetime.now()
		level = "[{0}]".format(logLevel)

		print("{0} - {1} - {2}".format(level.ljust(9),
									   date.strftime(Logger.DATE_FORMAT),
									   message))

	@staticmethod
	def debug(message):
		Logger.log(LogLevel.DEBUG, message)

	@staticmethod
	def info(message):
		Logger.log(LogLevel.INFO, message)

	@staticmethod
	def warning(message):
		Logger.log(LogLevel.WARNING, message)

	@staticmethod
	def error(message):
		Logger.log(LogLevel.ERROR, message)
