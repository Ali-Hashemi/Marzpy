from PyQt5.QtCore import QSize,QRect
from PyQt5.QtGui import QFont
from docx.shared import RGBColor


class CustomStyle:
    main_form_weight = 900
    main_form_height = 780

    main_list_widget_width = 300
    main_list_widget_height = 380

    secondary_list_widget_width = 301
    secondary_list_widget_height = 151

    form_size = QSize(550, 520)
    listbox_size = QRect(0, 90, 270, 290)
    fix_button_size = QRect(290, 230, 210, 100)
    clear_button_size = QRect(315, 340, 170, 60)

    websites_type_size = QRect(340, 0, 330, 100)
    film_type_size = QRect(0, 0, 300, 100)
    mode_type_size = QRect(320, 20, 420, 210)
    search_type_size = QRect(340, 0, 420, 230)
    browser_type_size = QRect(470, 0, 420, 100)
    dubbed_mode_cover_size = QRect(470, 0, 420, 100)
    info_cover_size = QRect(470, 110, 420, 80)

    radio_btn_font_size = QFont('Arial', 9)

    list_widget_font_size = 12

    tabs_height = 35
    # tabs_font = QFont('Arial', 8)
    tabs_font = QFont('Comic Sans MS', 8)

    label_size = QRect(175, 410, 200, 50)
    label_font = QFont('Arial', 12)

    spinbox_font = QFont('Segoe UI', 18)


class CustomNames:
    EXTRACTED_DATA = "zza.json"
    SOUP_SCREENSHOT = "my_screenshot.png"

    HTML_30nama_FILE_NAME = "30nama.html"
    HTML_IMDB_FILE_NAME = "imdb.html"
    HTML_Hex_FILE_NAME = "hexdownload.html"
    HTML_DOOSTIHA_FILE_NAME = "doostiha.html"

    PNG_30nama_FILE_NAME = "30nama.png"
    PNG_IMDB_FILE_NAME = "imdb.png"

    TXT_PER_NAME = "per_name.txt"
    TXT_ENG_NAME = "eng_name.txt"
    TXT_DATE = "date.txt"


class CustomPaths:
    CHROME_DRIVER = "chromedriver\\chromedriver.exe"


class StyleSheet:
    MAIN_BUTTON = "QPushButton{background-color : red;color: white;font: 12pt \"Segoe UI\";}QPushButton::pressed{background-color : lightgreen;color: red}"

    SECONDARY_BUTTON = "QPushButton{background-color : blue;color: white;font: 12pt \"Segoe UI\";}QPushButton::pressed{background-color : lightblue;}"

    TEXT_EDITOR_BORDER_GREY = "border: 1px solid grey;"
    TEXT_EDITOR_BORDER_RED = "border: 3px solid red;"
    TEXT_EDITOR_NO_BORDER = "border: 0px solid;color: red"


class CustomColor:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


class CustomColorRGB:
    BLACK = RGBColor(0, 0, 0)
    RED = RGBColor(255, 0, 0)
    LightGreen = RGBColor(85, 193, 0)
    DarkGreen = RGBColor(88, 165, 0)
    YELLOW = RGBColor(223, 255, 0)
    ORANGE = RGBColor(255, 116, 0)
    BLUE = RGBColor(0, 0, 255)
    WHITE = RGBColor(255, 255, 255)
