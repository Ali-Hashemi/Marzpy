import json
import ntpath
import platform
import re
import sys
from time import sleep
import webbrowser
import urllib.request
import requests
from Config import *
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
import shutil
from pdf2image import convert_from_path
import os
from bs4 import BeautifulSoup
from send2trash import send2trash
import undetected_chromedriver as uc
from langdetect import detect
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import numpy as np
from PyQt5.QtWidgets import QMessageBox


class Print:
    @staticmethod
    def print_black(value):
        print(CustomColor.BLACK + str(value))

    @staticmethod
    def print_white(value):
        print(CustomColor.WHITE + str(value))

    @staticmethod
    def print_red(value):
        print(CustomColor.RED + str(value))

    @staticmethod
    def print_yellow(value):
        print(CustomColor.YELLOW + str(value))

    @staticmethod
    def print_green(*value):
        text = ""
        for i in value:
            text+=i
        print(CustomColor.GREEN + str(text))

    @staticmethod
    def print_cyan(value):
        print(CustomColor.CYAN + str(value))

    @staticmethod
    def print_blue(value):
        print(CustomColor.BLUE + str(value))

    @staticmethod
    def print_full_line(color=""):
        print(color + "----------------------------------------------------------------------")


class MyWebDriver:
    firefox_options = Options()
    firefox_options.headless = True

    driver = None

    def __init__(self, url=None):
        service = Service()
        self.driver = webdriver.Firefox(service=service, options=self.firefox_options)
        if url:
            self.driver.get(url)

    def set_url(self, url):
        # navigate to the url
        self.driver.get(url)

    def get_soup(self):
        return BeautifulSoup(self.driver.page_source, "lxml")

    def find_element_by_class(self, class_name):
        element = self.driver.find_element(By.CLASS_NAME, class_name)
        print(element.get_attribute("outerHTML"))

    def find_element_by_css_selector(self, selector):
        element = self.driver.find_element(By.CSS_SELECTOR, selector)
        return (element.get_attribute("outerHTML"))

    def close(self):
        self.driver.close()

        # find element by css selector
        # myDiv = driver.find_element(By.CSS_SELECTOR, 'div.post-title')
        # print(myDiv.get_attribute("outerHTML"))
        #
        # mydiv2 = driver.find_element(By.CLASS_NAME, 'post-title')
        # print(mydiv2.text)

        # service = Service()
        #
        # with webdriver.Firefox(service=service, options=firefox_options) as driver:
        #     driver.get(url)
        #
        #     return driver


class Html:

    @staticmethod
    def get_soup(url, accept_lang="", timer=None, folder_path=None, soup_name=None):
        soup = None

        try:
            if accept_lang:
                soup_headers = {'User-Agent': 'Mozilla/5.0',
                                'Accept-Language': 'en-US,en;q=0.8'}
            else:
                soup_headers = {
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; SM-G928X Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36'}

            response = requests.get(url, headers=soup_headers, verify=True).text

            if timer:
                sleep(timer)

            soup = BeautifulSoup(response, "lxml")
            if soup:
                if folder_path and soup_name:
                    soup_file_path = rename_file_paths_by_os(folder_path) + soup_name
                    File.save_to_file(soup, soup_file_path)

        except Exception as e:
            Print.print_red(str(e))

        return soup

    @staticmethod
    def get_soup_with_chrome_driver_undetected(url, timer=None, folder_path=None, soup_name=None):
        soup = None

        try:

            chrome_options = Options()
            # chrome_options.add_experimental_option("detach", True)
            chrome_options.add_argument("--window-position=2000,0")

            # driver = webdriver.Chrome(options=chrome_options)
            # driver.get(url)
            # driver.execute_script("document.body.style.zoom='60%'")

            # chrome_driver_path = rename_file_paths_for_files(get_root_path() + CustomPaths.CHROME_DRIVER)

            # driver = uc.Chrome(driver_executable_path=chrome_driver_path, use_subprocess=True,
            #                    options=chrome_options)

            driver = uc.Chrome(use_subprocess=True, options=chrome_options)

            # driver.minimize_window()

            if timer:
                sleep(timer)

            driver.get(url)

            if folder_path:
                driver.save_screenshot(rename_file_paths_by_os(folder_path) + CustomNames.SOUP_SCREENSHOT)

            soup = BeautifulSoup(driver.page_source, "lxml")
            if soup:
                if folder_path and soup_name:
                    soup_file_path = rename_file_paths_by_os(folder_path) + soup_name
                    if os.path.exists(folder_path):
                        if os.path.exists(soup_file_path):
                            send2trash(soup_file_path)

                            File.save_to_file(soup, soup_file_path)
                        else:
                            File.save_to_file(soup, soup_file_path)

            driver.quit()

        except Exception as e:
            Print.print_red(str(e))

        return soup

    @staticmethod
    def get_soup_for_subscene(url, timer=None, folder_path=None, soup_name=None, accept_lang=""):
        soup = None

        try:
            # chrome_options = Options()
            # chrome_options.add_experimental_option("detach", True)
            # chrome_options.add_argument("--window-position=2000,0")
            # chrome_options.add_argument("--window-position=-2000,0")
            # chrome_options.add_argument("--start-maximized")
            # chrome_options.add_argument("--headless")

            # driver = webdriver.Chrome(options=chrome_options)

            firefox_options = Options()
            firefox_options.headless = True

            service_log_path = "C:\\Users\\Ali\\geckodriver.log"

            driver = webdriver.Firefox(options=firefox_options, service_log_path=service_log_path)

            if timer:
                sleep(timer)

            driver.get(url)

            soup = BeautifulSoup(driver.page_source, "lxml")

            if soup:
                if folder_path and soup_name:
                    soup_file_path = rename_file_paths_by_os(folder_path) + soup_name
                    if os.path.exists(folder_path):
                        if os.path.exists(soup_file_path):
                            send2trash(soup_file_path)

                            File.save_to_file(soup, soup_file_path)
                        else:
                            File.save_to_file(soup, soup_file_path)

            driver.close()

        except Exception as e:
            Print.print_red(str(e))

        return soup

    @staticmethod
    def get_soup_from_file(file_path) -> BeautifulSoup:
        with open(file_path, 'r') as f:
            # with open(file_path, 'rb') as f:
            contents = f.read()

            soup = BeautifulSoup(contents, 'lxml')

            return soup

    @staticmethod
    def download_with_browser(urls):
        firefox_options = Options()
        firefox_options.headless = True

        driver = webdriver.Firefox(options=firefox_options)

        for index, item in enumerate(urls):
            Print.print_green(item)
            driver.get(item)
            sleep(0.5)

        driver.close()

    @staticmethod
    def html2png(html_path, png_path, zoom=None):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        # chrome_options.add_argument("--window-position=2000,0")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("headless")

        driver = webdriver.Chrome(options=chrome_options)
        html_path = rename_file_paths_for_files(html_path)
        driver.get("file:///" + html_path)
        if zoom:
            driver.execute_script("document.body.style.zoom='" + str(zoom) + "%'")
        driver.save_screenshot(rename_file_paths_for_files(png_path))
        driver.quit()

    @staticmethod
    def find_elements_in_soup(soup, element):
        # for example:
        # element = Element("div", "sc-5be2ae66-0 gESiMH")      #   example of given elements as parameter
        # element2 = Element("div", "sc-5be2ae66-1 dRYQIl")     #   example of given elements as parameter
        # element3 = Element("h1", "sc-b73cd867-0 cEmnhL")      #   example of given elements as parameter
        # find_elements_in_soup(soup, element, element2, element3)

        final_element = []

        temp_soup = soup

        if element.find_all:
            if temp_soup:
                tempoo = []
                for i in temp_soup.find_all(str(element.name), {"class": element.classes}):
                    tempoo.append(i)
                if tempoo:
                    final_element = tempoo
        else:
            if temp_soup:
                temp_soup = temp_soup.find(str(element.name), {"class": element.classes})
                if temp_soup:
                    final_element = temp_soup

        return final_element

    @staticmethod
    def find_elements_in_multiple_soup_array_best(soup, *array_of_elements_array):
        # for example:
        # elements1_array = [
        #     Element("div", "sc-b5e8e7ce-0 dZsEkQ"),
        #     Element("div", "sc-b5e8e7ce-1 kNhUtn"),
        #     Element("h1", "sc-b73cd867-0 cEmnhL")
        # ]
        #
        # elements2_array = [
        #     Element("div", "sc-ab3b6b3d-3 goiwap"),
        #     Element("div", "sc-eda143c4-0 gGwFYG"),
        #     Element("h1", "sc-afe43def-0 hnYaOZ")
        # ]
        # found = Html.find_elements_in_multiple_soup_array_best(soup, elements1_array, elements2_array)

        final_final = None

        for index, value in enumerate(array_of_elements_array):
            final_element = []
            temp_soup = soup
            for k in value:
                if k.find_all:
                    if temp_soup:
                        tempoo = []
                        for i in temp_soup.find_all(str(k.name), {"class": k.classes}):
                            tempoo.append(i)
                        if tempoo:
                            final_element = tempoo
                    else:
                        break
                else:
                    if temp_soup:
                        temp_soup = temp_soup.find(str(k.name), {"class": k.classes})
                        if temp_soup:
                            final_element = temp_soup
                        else:
                            final_element = []
                    else:
                        break
            if final_element:
                final_final = final_element
                break

        return final_final


class Json:

    @staticmethod
    def write_to_json_file(json_object, json_file_path):
        if not isinstance(json_object, dict):
            json_object = json_object.__dict__
        with open(json_file_path, 'w') as f:
            json.dump(json_object, f)

        # hide_file(json_file_path)

    @staticmethod
    def read_from_json_file(json_file_path):
        json_data = None

        if os.path.exists(json_file_path):
            with open(json_file_path) as f:
                json_data = json.load(f)
        else:
            Print.print_red("File does not exist !!!")

        return json_data

    @staticmethod
    def sort_json(json_object):
        return dict(sorted(json_object.items()))


class File:

    @staticmethod
    def trim_name_movie(name):
        date = "(" + File.trim_released_date(name) + ")"
        code = "(" + File.trim_poster_code(name) + ") - "

        new_name = str(name).replace(date, "")
        new_name = str(new_name).replace(code, "")

        new_name = strip_text(new_name)

        return new_name

    @staticmethod
    def trim_name_tv_series(name):
        date = "(" + File.trim_released_date(name) + ")"
        code = "(" + File.trim_poster_code(name) + ") - "

        new_name = str(name).replace(date, "")
        new_name = str(new_name).replace(code, "")
        new_name = str(new_name).replace("(Only Dub)", "")

        new_name = strip_text(new_name)

        full_names_to_filter = [
            " (Dub) 480p",
            " (Dub) 720p",
            " (Dub) 1080p",
            " (Dub)",
            " (Cen)",
            " 480p",
            " 720p",
            " 1080p",
        ]

        for word in full_names_to_filter:
            if str(word).endswith(word):
                new_name = new_name.replace(word, '')

        regex = str("[(]20\d{2}-20\d{2}[)]" +
                    "|" + "[(]19\d{2}-20\d{2}[)]" +
                    "|" + "[(]19\d{2}-[)]" +
                    "|" + "[(]20\d{2}-[)]")

        m = re.findall(regex, new_name)
        for x in m:
            new_name = new_name.replace(x, '')

        new_name = strip_text(new_name)

        return new_name

    @staticmethod
    def trim_released_date(name) -> str:
        name = strip_text(name)

        regex = str("[(]20\d{2}[)]" + "|" + "[(]19\d{2}[)]" + "|" + "[(]13\d{2}[)]" + "|" + "[(]14\d{2}[)]")

        date = ""

        j = re.findall(regex, name)

        if j:
            date = j[0]
            date = str(date).replace("(", "")
            date = str(date).replace(")", "")

        if not date:
            regex2 = str("20\d{2}" + "|" + "19\d{2}" + "|" + "13\d{2}" + "|" + "14\d{2}")

            m = re.findall(regex2, name)

            if m:
                date = m[0]
                date = str(date).replace("(", "")
                date = str(date).replace(")", "")

        return date

    @staticmethod
    def trim_season_and_episode(name) -> str:
        name = str(name)
        regex = "[S|s]\d{2}[E|e]\d{2}"

        new_name = ""

        find = re.findall(regex, name)

        if find:
            new_name = find[0]
            new_name = new_name.upper()

        return new_name

    @staticmethod
    def trim_poster_code(name) -> str:
        name = str(name)
        regex = "^[(][a-zA-Z][a-zA-Z]+\d+[)]|^[(][a-zA-Z]+\d+[)]"

        new_name = ""

        find = re.findall(regex, name)

        if find:
            new_name = find[0]
            new_name = str(new_name).replace("(", "")
            new_name = str(new_name).replace(")", "")

        return new_name

    @staticmethod
    def trim_only_digits(name):
        char_str = re.sub('\D', '', name)

        char_str = strip_text(char_str)

        if char_str:
            return char_str
        else:
            return False

    @staticmethod
    def trim_only_letters(name):
        pattern_order = r'[0-9]'

        char_str = re.sub(pattern_order, '', name)

        char_str = strip_text(char_str)

        if char_str:
            return char_str
        else:
            return False

    @staticmethod
    def has_ok_at_the_end(name):
        name = str(name)
        regex = "[(](OK)[)]$"

        find = re.findall(regex, name)

        if find:
            return True
        else:
            return False

    @staticmethod
    def get_file_name(name):
        return strip_text(str(os.path.splitext(name)[0]))

    @staticmethod
    def get_file_ext(name):
        return strip_text(str(os.path.splitext(name)[1]))

    @staticmethod
    def get_all_dates(name) -> []:
        name = strip_text(name)

        j = re.findall("20\d{2}|19\d{2}|13\d{2}|14\d{2}", name)

        date = []

        if j:
            for x in j:
                date.append(x)
        elif name.find("(") != -1:
            date.append(name[name.find("(") + 1:name.find(")")])

        return date

    @staticmethod
    def hide_file(file_path):
        os.system('attrib +h -s ' + '"' + file_path + '"')

    @staticmethod
    def save_to_file(content, file_path):
        with open(file_path, "w") as file:
            file.write(strip_text(str(content)))

    @staticmethod
    def load_from_file(file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                contents = f.read()

                return strip_text(str(contents))
        else:
            Print.print_red("File does not exist !!!")
            return None


class Download:
    def __init__(self, url, location, name, file_extension):
        location = rename_file_paths_by_os(location)

        new_name = str(name).replace("/", ".")
        new_name = str(new_name).replace(":", ".")

        final_location = str(location + new_name + file_extension)

        if not os.path.exists(location):
            os.makedirs(location)

        if not os.path.exists(final_location):
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-Agent',
                                  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'),
                                 ('Accept',
                                  'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'),
                                 ('Accept-Encoding', 'gzip, deflate, br'),
                                 ('Accept-Language', 'en-US,en;q=0.5'), ("Connection", "keep-alive"),
                                 ("Upgrade-Insecure-Requests", '1')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(url, final_location)


class Message:
    @staticmethod
    def showOk(title=None, text=None):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Message box pop up window")
        msgBox.setWindowTitle("QMessageBox Example")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        # if returnValue == QMessageBox.Ok:
        #     print('OK clicked')

        # dlg = QMessageBox()
        # if title:
        #     dlg.setWindowTitle(str(title))
        # if text:
        #     dlg.setText(str(text))
        # button = dlg.exec()

        button = msgBox.exec()
        if button == QMessageBox.Ok:
            return True
        else:
            return False


def is_contain_4_digit_numbers(text) -> bool:
    state = False

    # regex = str("20\d{2}" + "|" + "19\d{2}" + "|" + "13\d{2}" + "|" + "14\d{2}")
    regex = str("\d{4}")

    j = re.findall(regex, text)

    if j:
        state = True

    return state


def is_contain_hour_or_minute(text) -> bool:
    state = False

    regex = str("\d{1,3}m" + "|" + "\d+h")

    j = re.findall(regex, text)

    if j:
        state = True

    return state


def detect_lang(text):
    return detect(str(text))


def convert_qt_creator_to_class(file):
    parent_folder, ui_file = get_path_and_file(file)
    command = "pyuic5 " + str(file) + " -o " + parent_folder + "MainWindow.py"
    os.system(command)


def convert_pdf_to_image(source, dest):
    poppler_path = rename_file_paths_by_os(get_root_path() + "poppler-23.01.0/Library/bin")

    pages = convert_from_path(pdf_path=source, poppler_path=poppler_path)

    if not os.path.exists(dest):
        os.makedirs(dest)

    c = 1
    for page in pages:
        img_name = f"img-{c}.jpg"
        page.save(os.path.join(dest, img_name), "jpeg")
        c += 1


def iterate_folder_with_subdirs(dir):
    files_array = []

    for rootdir, dirs, files in os.walk(dir):
        for name in files:
            files_array.append(rename_file_paths_by_os(rootdir) + str(name))

    return files_array


def find_in_text(item, value):  # TODO ----------------- Use this method more often
    return (strip_text(item).lower()).find(strip_text(value).lower()) != -1


def clear_txt_contents(location):
    o = open(location, "r+")
    o.truncate(0)
    o.close()


def check_if_is_array(array):
    return isinstance(array, (list, tuple, np.ndarray))


def remove_array_duplicates(array):
    if find_in_text((array[-1]), " و "):
        last_index = array[-1]
        if not (find_in_text(last_index, "کودک") and find_in_text(last_index, "نوجوان")):
            last_index = last_index.split(" و ")
        array.pop()
        if last_index:
            if check_if_is_array(last_index):
                for l in last_index:
                    array.append(l)
            else:
                array.append(last_index)

    array = [i for n, i in enumerate(array) if i not in array[:n]]
    return array


def get_root_path():
    return rename_file_paths_by_os(str(os.path.dirname(os.path.abspath(__file__))).replace("\\Classes", ""))


def get_current_script_path():
    return rename_file_paths_for_files(sys.argv[0])


def get_path_and_file(path):
    if path.endswith("/") or path.endswith("\\"):
        path = path[:-1]
    ntpath.basename("a/b/c")
    path, file_or_folder = ntpath.split(path)
    return rename_file_paths_by_os(path), str(file_or_folder)


def get_last_file_or_folder_from_path(name):
    path = rename_file_paths_for_files(name)

    if not is_os_linux():
        path = str(name).replace("\\", "/")

    if path.endswith("/"):
        path = path[:-1]

    split_text = (path.split("/"))[-1]

    return split_text


def filter_name(name) -> str:
    name = str(name).strip()

    if find_in_text(name, "("):
        new_name = name[:name.find("(")]
    else:
        new_name = name

    new_name = new_name.replace(",", "")
    new_name = new_name.replace("'", "")
    new_name = new_name.replace("’", "")
    new_name = new_name.replace(".", "")
    new_name = new_name.replace(":", "")
    new_name = new_name.replace("?", "")
    new_name = " ".join(new_name.split())  # Deletes Multiple Spaces
    new_name = new_name.strip()

    return new_name


def filter_name_for_equal_checking(name) -> str:
    name = str(name).strip()

    if find_in_text(name, "("):
        new_name = name[:name.find("(")]
    else:
        new_name = name

    new_name = new_name.replace("?", "")
    new_name = " ".join(new_name.split())  # Deletes Multiple Spaces
    new_name = new_name.strip()

    return new_name


def filter_name_for_cast_and_info(name) -> str:
    name = strip_text(name)

    if name:
        new_name = name.replace("\u200e", " ")
        new_name = new_name.replace("\u200c", " ")
        new_name = str(new_name).replace("و….", "")
        new_name = str(new_name).replace("و …", "")
        new_name = str(new_name).replace("و…", "")
        new_name = str(new_name).replace("...", "")
        new_name = str(new_name).replace("…", "")
        new_name = str(new_name).replace("..", "")
        new_name = str(new_name).replace("'", "")
        new_name = str(new_name).replace("، ،", "،")
        new_name = str(new_name).replace("[", "")
        new_name = str(new_name).replace("]", "")
        new_name = str(new_name).replace(" با حضور افتخاری ", "")
        new_name = str(new_name).replace(" و با صدای ", " , ")
        new_name = str(new_name).replace(" و با حضور ", " , ")
        new_name = str(new_name).replace(" و با معرفی ", " , ")
        new_name = str(new_name).replace("و بازیگران خردسال این فیلم سینمایی", "،")
        new_name = str(new_name).replace("هٔ", "ه")
        new_name = strip_text(new_name)

        if new_name.endswith(" و"):
            new_name = new_name[:-2]

        if new_name[-1] == ".":
            new_name = new_name[:-1]

        if new_name[-1] == "و":
            new_name = new_name[:-1]

        if new_name[-1] == ",":
            new_name = new_name[:-1]

        new_name = strip_text(new_name)

        return new_name
    else:
        return name


def filter_name_for_url(name) -> str:
    new_name = strip_text(name)

    x = re.findall(" \d{1} ", new_name)

    # if new_name.find(" 1 ") != -1:
    #     new_name = str(new_name.replace(" 1 ", "")).strip()

    if x:
        new_name = new_name.replace(x[0], " ").strip()

    if new_name.find("(") != -1:
        new_name = (new_name[:new_name.find("(")]).strip()
    else:
        new_name = new_name

    # new_name = new_name.replace(" ", "+")
    new_name = new_name.replace(" ", "%20")
    new_name = new_name.replace("'", "%27")
    new_name = new_name.replace("’", "%27")
    new_name = new_name.replace("&", "%26")
    new_name = new_name.replace("!", "%21")
    new_name = new_name.replace(",", "%2C")
    new_name = re.sub("  ", " ", new_name)

    new_name = strip_text(new_name)

    return new_name


def filter_name_for_url_30nama(name) -> str:
    new_name = strip_text(name)

    # x = re.findall(" \d{1} ", new_name)

    # if new_name.find(" 1 ") != -1:
    #     new_name = str(new_name.replace(" 1 ", "")).strip()

    # if x:
    #     new_name = new_name.replace(x[0], " ").strip()

    # if new_name.find("(") != -1:
    #     new_name = (new_name[:new_name.find("(")]).strip()
    # else:
    #     new_name = new_name

    new_name = new_name.replace("'", "%20")
    new_name = new_name.replace("’", "%20")
    new_name = new_name.replace(" ", "%20")
    new_name = new_name.replace("&", "%26")
    new_name = new_name.replace("!", "%21")
    new_name = new_name.replace(",", "%2C")
    new_name = re.sub("  ", " ", new_name)

    new_name = strip_text(new_name)

    return new_name


def strip_text(name) -> str:
    text = str(name).strip()
    text = " ".join(text.split())  # Deletes Multiple Spaces

    return text


def slicer(my_str, sub):
    index = my_str.find(sub)
    if index != -1:
        return my_str[:index].strip()
    else:
        Print.print_white('Sub string not found!')


def has_per_subtitle(path):
    new_location = rename_file_paths_by_os(path)

    state = 0  # if =0 is nothing, =1 is sub, =2 is only dub, =3 is sub & dub

    has_full_sub = 0
    has_dub_sub = 0

    is_subbed_state = 0
    is_dubbed_state = 0

    folder_release_date = " (" + File.trim_released_date(new_location) + ")"

    folder_name = File.trim_name_movie(get_last_file_or_folder_from_path(new_location))

    # per_sub_file_path = new_location + "(Per) " + folder_name + folder_release_date + ".srt"

    per_sub_folder_path = new_location + "Full Subs"

    if find_in_text(new_location, "dubbed"):
        if os.path.exists(new_location):
            for name in os.listdir(new_location):
                if not os.path.isdir(new_location + name):
                    if name.lower().endswith(".srt") and find_in_text(name, "(Per)"):
                        has_full_sub = 1
            has_dub_sub = 1

    elif find_in_text(new_location, "sub"):
        if os.path.exists(new_location):
            # for name in os.listdir(new_location):
            #     if not os.path.isdir(new_location + name):
            #         if name.lower().endswith(".srt") and not find_in_text(name, "(Per)"):
            has_full_sub = 1

    if os.path.exists(per_sub_folder_path):
        has_full_sub = 1

    if has_full_sub and has_dub_sub:
        state = 3
    elif has_full_sub and not has_dub_sub:
        state = 1
    elif not has_full_sub and has_dub_sub:
        state = 2

    if state == 1 or state == 3:
        is_subbed_state = 1

    if state == 2 or state == 3:
        is_dubbed_state = 1

    return is_subbed_state, is_dubbed_state


def copy_files_to_folder(source, dest, file_name):
    dest = rename_file_paths_by_os(dest)
    if not os.path.exists(dest):
        os.makedirs(dest)
        shutil.copy(source, dest + str(file_name))
    else:
        shutil.copy(source, dest + str(file_name))


def move_or_rename_files(source, dest, file_name):
    dest = rename_file_paths_by_os(dest)
    if not os.path.exists(dest):
        os.makedirs(dest)
        shutil.move(str(source), str(dest + file_name))
    else:
        shutil.move(str(source), str(dest + file_name))


def delete_empty_folder(*folder_path):
    for path in folder_path:
        if os.path.exists(path):
            if len(os.listdir(path)) == 0:
                send2trash(path)


def extract_zip_files_movies(location, parent_name):
    new_location = rename_file_paths_by_os(location)
    if os.path.exists(new_location):
        for name in os.listdir(new_location):
            if not os.path.isdir(new_location + name):
                if name.lower().endswith(".zip"):
                    filename_without_extension = str(File.get_file_name(name))

                    file_location = str(new_location + name)

                    extracted_folder_name = new_location + filename_without_extension

                    try:
                        shutil.unpack_archive(
                            file_location, extracted_folder_name)

                    except Exception as e:
                        Print.print_red(name)
                        print(e)
                        Print.print_red("An Exception Occurred")
                        Print.print_full_line(CustomColor.RED)

                    if os.path.exists(extracted_folder_name):
                        send2trash(file_location)
        folder_count = 0
        for name in os.listdir(new_location):
            if folder_count > 0:
                break
            else:
                if os.path.isdir(new_location + name):
                    folder_count += 1
                    folder_length = len(os.listdir(new_location + name))
                    if folder_length > 1:
                        for idx, n in enumerate(os.listdir(new_location + name)):
                            if not os.path.isdir(n):
                                file_new_name = parent_name + " " + \
                                                str(idx + 1) + str(os.path.splitext(n)[1])
                                move_or_rename_files(new_location + name + "\\" + n, new_location + "\\",
                                                     file_new_name)
                    else:
                        for s in os.listdir(new_location + name):
                            if not os.path.isdir(s):
                                file_new_name = parent_name + str(os.path.splitext(s)[1])
                                move_or_rename_files(rename_file_paths_by_os(new_location + name) + s, new_location,
                                                     file_new_name)

                    send2trash(new_location + name)


def extract_zip_files_tv_series(location):
    season_array_equivalent = ["10", "9", "8",
                               "7", "6", "5", "4", "3", "2", "1"]

    for j in season_array_equivalent:
        folder_location = rename_file_paths_by_os(rename_file_paths_by_os(location) + j)
        if os.path.exists(folder_location):
            for name in os.listdir(folder_location):
                if not os.path.isdir(folder_location + name):
                    if name.lower().endswith(".zip"):
                        filename_without_extension = str(File.get_file_name(name))

                        file_location = str(folder_location + name)

                        extracted_folder_name = folder_location + filename_without_extension

                        try:
                            shutil.unpack_archive(file_location, extracted_folder_name)

                        except:
                            Print.print_red(name)
                            Print.print_red("An Exception Occurred")
                            Print.print_full_line(CustomColor.RED)

                        if os.path.exists(extracted_folder_name):
                            send2trash(file_location)


def open_in_browser(url, browser_type=1):
    if browser_type == 1:
        if is_os_linux():
            browser_path = '/usr/bin/google-chrome %s'
        else:
            # browser_path = 'C:/Users/Ali/AppData/Local/Programs/Opera/opera.exe %s'
            # browser_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
            browser_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'

        webbrowser.get(browser_path).open(url)

    elif browser_type == 2:
        if is_os_linux():
            browser_path = '/usr/bin/firefox'
        else:
            browser_path = "C:/Program Files/Mozilla Firefox/firefox.exe %s"

        webbrowser.get(browser_path).open(url)


def open_html_file_in_browser(file):
    if is_os_linux():
        browser_path = '/usr/bin/google-chrome %s'
    else:
        # browser_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        browser_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'

    url = "file://" + file
    webbrowser.get(browser_path).open(url)


def rename_file_paths_for_files(item):
    if is_os_linux():
        return str(item.replace("\\", "/"))
    else:
        return str(item.replace("/", "\\"))


# slash_or_b_slash_by_os = lambda: str("/") if (is_os_linux()) else str("\\")

def rename_file_paths_by_os(item):
    path = ""
    if is_os_linux():
        path = str(item).replace("//", "/")
        path = str(path).replace("\\", "/")
        if not path[-1] == "/":
            path = path + "/"
    else:
        path = str(item).replace("\\\\", "\\")
        path = (str(path).replace("/", "\\"))
        if not path[-1] == "\\":
            path = path + "\\"
    return path


def is_os_linux():
    is_linux = False
    if str(platform.system()).lower().find("linux") != -1:
        is_linux = True

    return is_linux
