import pickle
import os.path

def load_cookie(driver):
    if check_cookies():
        with open("cookie", "rb") as cookiesfile:
            cookies = pickle.load(cookiesfile)
            for cookie in cookies:
                driver.add_cookie(cookie)


def save_cookie(driver):
    with open("cookie", "wb") as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)


def check_cookies():
    return os.path.isfile("cookie")
