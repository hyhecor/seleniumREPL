from selenium.webdriver.remote import webdriver as webdriver_
from sys import stdin
import argparse
import driver_factory
import repl
import traceback


def main():
    __args__DriverName = "firefox"
    __args__InputFiles = None
    __args__LineFeed = "\\"

    parser = argparse.ArgumentParser(
        prog="ProgramName",
        description="What the program does",
        epilog="Text at the bottom of help",
    )

    parser.add_argument(
        "--driver-name",
        "-d",
        default=__args__DriverName,
        type=str,
        help="selenium driver name",
    )

    parser.add_argument("--input-files", "-f", type=str, nargs="*", help="input files")

    parser.add_argument(
        "--linefeed", "-L", default=__args__LineFeed, type=str, help="linefeed"
    )

    try:
        flag = parser.parse_args()

        if not (flag.driver_name is None):
            __args__DriverName = flag.driver_name

        if not (flag.input_files is None):
            __args__InputFiles = flag.input_files

        if not (flag.linefeed is None):
            __args__LineFeed = flag.linefeed

    except Exception as ex:
        print("ERROR: {0}".format(ex))
        traceback.print_tb(ex.__traceback__)
        return

    driver = driver_factory.SeleniumWebDriver(__args__DriverName)

    try:
        if not (__args__InputFiles is None):
            for it in __args__InputFiles:
                ExecFile(driver, it, __args__LineFeed)
        else:
            REPL(driver, __args__LineFeed)

    except Exception as ex:
        print("ERROR: {0}".format(ex))
        traceback.print_tb(ex.__traceback__)

    try:
        if driver is None:
            return

        driver.quit()
        driver = None

    except:
        pass


def ExecFile(driver: webdriver_.WebDriver, fileName: str, lineFeed: str = ";"):
    file = open(fileName)
    i = 0

    exec, buff = Exec(driver, lineFeed)

    while True:
        line = file.readline()
        if not line:
            print("EOF")
            break

        print("{0}: {1}".format(i, line))
        i += 1

        if exec(line) == False:
            break

    file.close()


def REPL(driver: webdriver_.WebDriver, lineFeed: str = "\\"):
    exec, buf = Exec(driver, lineFeed)

    # while True:
    #     print('REPL> ', end='') if len(buff()) == 0 else print('> ', end='')
    #     n+=1
    #     line = input()
    #     if not line:
    #         print('EOF')
    #         break

    #     if exec(line) == False:
    #         break

    while True:
        print("REPL> ", end="") if len(buf()) == 0 else print("> ", end="")

        line = stdin.readline()
        if not line:
            print("EOF")
            break

        if exec(line) == False:
            break


def Exec(driver: webdriver_.WebDriver, lineFeed: str = "\\"):
    buf = ""
    repl_ = repl.New(driver, lineFeed, True)

    def exec(s: str):
        nonlocal buf

        if (len(buf) == 0) and (len(strip(s)) == 0):
            return True

        # comment: '#'
        if strip(s).find("#") == 0:
            return True

        # comment: '//'
        if strip(s).find("//") == 0:
            return True

        s = s.strip(" \r\n")
        # convert str reverse to find
        end = s[::-1].find(lineFeed)
        if end == 0:
            buf += s[: -len(lineFeed)] + "\n"
            return True
        else:
            buf += s.strip(" ")

        try:
            s, buf = buf, ""

            return repl_.Parse(strip(s))

        except Exception as ex:
            print("ERROR: {0}".format(ex))
            traceback.print_tb(ex.__traceback__)

        return True

    def buff():
        nonlocal buf
        return buf

    return exec, buff


def strip(s: str) -> str:
    return s.strip(" \t\n\r")


if __name__ == "__main__":
    main()
