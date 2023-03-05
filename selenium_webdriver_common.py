from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def setenv(v, prefix):
    import os
    import inspect

    # getmembers() returns all the
    # members of an object
    for i in inspect.getmembers(v):
        # to remove private and protected
        # functions
        if not i[0].startswith("_"):
            # To remove other methods that
            # doesnot start with a underscore
            if not inspect.ismethod(i[1]):
                os.environ["{0}{1}".format(prefix, i[0])] = i[1]


def init():
    setenv(By(), "BY_")
    setenv(Keys(), "KEYS_")


# if __name__ == '__main__':
#     print('{0}:'.format(By.__name__))
#     init(By(), 'BY_')

#     print('{0}:'.format(Keys.__name__))
#     init(Keys(), 'KEY_')
