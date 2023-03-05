import os
from selenium.webdriver.remote import webdriver as webdriver_
from selenium.webdriver.remote import webelement
import argparse

# from nltk.tokenize import word_tokenize
# import nltk
# nltk.download('punkt')
from shlex import split
import selenium_webdriver_common

selenium_webdriver_common.init()

W = "\033[0m"  # white (normal)
R = "\033[31m"  # red
G = "\033[32m"  # green
O = "\033[33m"  # orange
B = "\033[34m"  # blue
P = "\033[35m"  # purple


def printVerbose(msg):
    print(B + ">> " + msg + W)


class REPL:
    def __init__(self, driver: webdriver_.WebDriver, verbose: bool) -> None:
        self.memory = []
        self.isClosed = False
        self.driver = driver
        self.verbose = verbose

    def get(self, *args: str):
        parser = argparse.ArgumentParser(
            description="""Loads a web page in the current browser session"""
        )

        parser.add_argument("url", nargs="?", type=str, help="url")

        if self.verbose:
            printVerbose("{0} args={1}".format(parser.description, args))

        flag = parser.parse_args(map(lambda x: x, args))
        url = self.Value(flag.url)

        self.driver.get(url)

    def close(self, *args: str):
        parser = argparse.ArgumentParser(description="""Closes the current window""")

        if self.verbose:
            printVerbose("{0} args={1}".format(parser.description, args))

        self.driver.close()
        self.isClosed = True

    def quit(self, *args: str):
        parser = argparse.ArgumentParser(
            description="""Quits the driver and closes every associated window"""
        )

        if self.verbose:
            printVerbose("{0} args={1}".format(parser.description, args))

        self.driver.quit()
        self.isClosed = True

    def find_element(self, *args: str):
        parser = argparse.ArgumentParser(
            description="""Find an element given a By strategy and locator"""
        )

        parser.add_argument("by", nargs="?", type=str, help="By.\{str\}")

        parser.add_argument("value", nargs="?", type=str, help="value: str")

        if self.verbose:
            printVerbose("{0} args={1}".format(parser.description, args))

        flag = parser.parse_args(map(lambda x: x, args))
        by = self.Value(flag.by)
        value = self.Value(flag.value)

        return self.driver.find_element(by, value)

    def text(self, *args: str):
        parser = argparse.ArgumentParser(description="""The text of the element""")

        parser.add_argument("prev", nargs="?", type=str, help="prev")

        if self.verbose:
            printVerbose("{0} args={1}".format(parser.description, args))

        flag = parser.parse_args(map(lambda x: x, args))
        elem = self.Value(flag.prev, "-1")

        return elem.text

    def click(self, *args: str):
        parser = argparse.ArgumentParser(description="""Clicks the element""")

        parser.add_argument("prev", nargs="?", type=str, help="prev")

        if self.verbose:
            printVerbose("{0} args={1}".format(parser.description, args))

        flag = parser.parse_args(map(lambda x: x, args))
        elem = self.Value(flag.prev, "-1")

        return elem.click()

    def clear(self, *args: str):
        parser = argparse.ArgumentParser(
            description="""Clears the text if it's a text entry element"""
        )

        parser.add_argument("prev", nargs="?", type=str, help="prev")

        if self.verbose:
            printVerbose("{0} args={1}".format(parser.description, args))

        flag = parser.parse_args(map(lambda x: x, args))
        elem = self.Value(flag.prev, "-1")

        return elem.clear()

    def send_keys(self, *args: str):
        parser = argparse.ArgumentParser(
            description="""Simulates typing into the element"""
        )

        parser.add_argument("prev", nargs="?", type=str, help="prev")

        parser.add_argument("value", nargs="*", type=str, help="prev")

        if self.verbose:
            printVerbose("{0} args={1}".format(parser.description, args))

        flag = parser.parse_args(map(lambda x: x, args))
        elem = self.Value(flag.prev, "-1")
        value = map(self.Value, flag.value)
        value = tuple(value)

        return elem.send_keys(value)

    def refresh(self, *args: str):
        parser = argparse.ArgumentParser(description="""Refreshes the current page""")

        if self.verbose:
            printVerbose("{0} args={1}".format(parser.description, args))

        self.driver.refresh()

    def current_url(self, *args: str):
        parser = argparse.ArgumentParser(
            description="""Gets the URL of the current page"""
        )

        if self.verbose:
            printVerbose("{0} args={1}".format(parser.description, args))

        return self.driver.current_url

    def setenv(self, *args: str):
        parser = argparse.ArgumentParser(description="""Set value to os.enviroment""")

        parser.add_argument("value", nargs="?", type=str, help="value")
        parser.add_argument("key", nargs="?", type=str, help="key")

        if self.verbose:
            printVerbose("{0} args={1}".format(parser.description, args))

        flag = parser.parse_args(map(lambda x: x, args))
        value = self.Value(flag.value, "-1")
        key = self.Value(flag.key)

        os.environ["{0}".format(key)] = value

    def Parse(self, s: str):
        args = split(s)
        args = map(strip, args)
        args = list(args)
        arg0 = args[0] if 0 < len(args) else ""

        default = (None, False)
        fn, memorise = {
            # 'quit': (self.quit, False),
            "close": (self.close, False),
            "get": (self.get, False),
            "elem": (self.find_element, True),
            "find_element": (self.find_element, True),
            "text": (self.text, True),
            "click": (self.click, False),
            "clear": (self.clear, False),
            "type": (self.send_keys, False),
            "send_keys": (self.send_keys, False),
            "reflash": (self.refresh, False),
            "current_url": (self.current_url, True),
            "setenv": (self.setenv, False),
        }.get(arg0, default)

        if fn is None:
            print('"{0}" is not a command'.format(s))
            return not self.isClosed

        rst = fn(*(args[1:]))
        if memorise:
            self.memory.append(rst)

        return not self.isClosed

    def Value(self, s: str, default: str = ""):
        if len(s) == 0:
            return default

        if strip(s).find("$") == 0:
            s = s.strip("$ ()\{\}")
            return os.getenv(s)

        if strip(s).find("#") == 0:
            s = s.strip("# ()\{\}")

            return self.memory[int(s)]

        return s


def New(driver: webdriver_.WebDriver, verbose: bool = False) -> REPL:
    return REPL(driver, verbose)


# if __name__ == '__main__':
#     while True:
#         print('> ')
#         s = input()
#         print(s+'\n')


def strip(s: str) -> str:
    return s.strip(" \t\n\r")
