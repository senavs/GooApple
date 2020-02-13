import logging


class Logger:

    def __init__(self, name: str, output_file: str, fmt: str = None):
        """Custom logger

        :param name: logger name
            :type: str
        :param output_file: file logger output
            :type: str
        :param fmt: logger formatter
            :type: str
            :style: {
        """

        # default format
        if not fmt:
            fmt = '{asctime} | {name} | {levelname:^9} | {message}'

        # logger
        self.log = logging.getLogger(name)
        self.log.setLevel(logging.DEBUG)

        # format
        self.formatter = logging.Formatter(fmt, style='{')
        # stream
        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setLevel(logging.DEBUG)
        self.stream_handler.setFormatter(self.formatter)
        # file
        self.file_handler = logging.FileHandler(output_file)
        self.file_handler.setLevel(logging.DEBUG)
        self.file_handler.setFormatter(self.formatter)

        # adding
        self.log.addHandler(self.stream_handler)
        self.log.addHandler(self.file_handler)

    @property
    def level(self):
        return self.log.level

    @level.setter
    def level(self, value):
        self.log.setLevel(value)

    def debug(self, msg: str):
        self.log.debug(msg)

    def info(self, msg: str):
        self.log.info(msg)

    def warning(self, msg: str):
        self.log.warning(msg)

    def error(self, msg: str):
        self.log.error(msg)

    def critical(self, msg: str):
        self.log.critical(msg)
