from Form.MainWindow import Ui_MainWindow
from Form.CustomListViewJsonEditor import *
from marzpy import Marzban
from marzpy.api.User import User
from datetime import datetime
import time
import math
from PyQt5.QtWidgets import QListWidgetItem, QShortcut
from PyQt5.QtGui import QKeySequence
from datetime import datetime


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


class PanelClass(Marzban):
    MyMainWindow = None

    def __init__(self, mainwindow, panel_index) -> None:
        if panel_index == 0:
            super().__init__("mike", "z", "https://amzpnl1.intonature.tech")
        if panel_index == 1:
            super().__init__("mike", "z", "https://v1.fnldagger.shop")
        if panel_index == 2:
            super().__init__("z", "z", "https://myblog.intonature.tech")

        self.MyMainWindow = mainwindow

    def modify_user(self, user_username: str, token: dict, user: object):
        super().modify_user(user_username, token, user)

    def filter_user(self, users, search_name):
        list_array = []

        for i in users:
            current_user: User = i

            if find_in_text(current_user.username, search_name):
                list_array.append(current_user.username)

        return list_array


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    PANEL = None
    TOKEN = None
    GB_SIZE = (1024 * 1024 * 1024)
    days_in_seconds = 86400 + 50
    Users = None

    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.listWidget.hide()

        self.listWidget_items = ListBoxWidget(self.centralwidget, QtCore.QRect(self.listWidget.geometry().left(),
                                                                               self.listWidget.geometry().top(),
                                                                               self.listWidget.width(),
                                                                               self.listWidget.height()))

        self.PANEL = PanelClass(self,0)

        self.TOKEN = self.PANEL.get_token()

        self.refresh_items()

        self.pushButton_save.clicked.connect(
            lambda: (self.save_item()))

        self.shortcut_save = QShortcut(QKeySequence('ctrl+s'), self)
        self.shortcut_save.activated.connect(lambda: (self.save_item()))

        self.pushButton_disable_user.clicked.connect(
            lambda: (self.disable_user()))

        self.pushButton_add_30_days.clicked.connect(
            lambda: (self.add_30_days()))

        self.pushButton_reset_usage.clicked.connect(
            lambda: (self.reset_usage()))

        self.listWidget_items.itemSelectionChanged.connect(
            lambda: (self.get_each_items()))

        self.comboBox_panel.currentIndexChanged.connect(
            lambda: (self.change_panel(self.comboBox_panel.currentIndex())))

        self.pushButton_scan_active.clicked.connect(
            lambda: (self.scan_empty_fields(check_active=1)))

        self.pushButton_scan_limited.clicked.connect(
            lambda: (self.scan_empty_fields(check_limited=1)))

        self.pushButton_scan_expired.clicked.connect(
            lambda: (self.scan_empty_fields(check_expired=1)))

        self.pushButton_scan_disabled.clicked.connect(
            lambda: (self.scan_empty_fields(check_disabled=1)))

        self.lineEdit_search.textChanged.connect(
            lambda: (self.method_search(self.lineEdit_search.text())))

        self.pushButton_refresh.clicked.connect(
            lambda: (self.refresh_items()))

        self.pushButton_clear_search.clicked.connect(
            lambda: (self.clear_search()))
        self.shortcut_clear_search = QShortcut(QKeySequence('esc'), self)
        self.shortcut_clear_search.activated.connect(lambda: (self.clear_search()))

    def change_panel(self, index):
        self.PANEL = PanelClass(self, index)

        self.TOKEN = self.PANEL.get_token()

        self.refresh_items()

    def disable_user(self):
        current_row = self.listWidget_items.currentRow()
        if self.listWidget_items.item(current_row):
            selected_user = self.listWidget_items.item(current_row).text()
            current_user: User = self.PANEL.get_user(selected_user, self.TOKEN)
            current_user.status = 'disabled'

            self.PANEL.modify_user(current_user.username, self.TOKEN, current_user)
            self.clear_text_boxes()

    def refresh_items(self):
        self.listWidget_items.clear()

        self.Users = self.PANEL.get_all_users(self.TOKEN)

        if self.Users:
            for i in self.Users:
                current_user: User = i
                self.listWidget_items.addItem(current_user.username)

        self.clear_text_boxes()

    def clear_search(self):
        self.method_search("")

        self.lineEdit_search.clear()
        self.clear_text_boxes()

    def method_search(self, text):
        self.clear_text_boxes()

        self.listWidget_items.clear()

        list = self.PANEL.filter_user(self.Users, text)

        for i in list:
            self.listWidget_items.addItem(i)

    def get_each_items(self):
        list_count = self.listWidget_items.count()
        if list_count > 0:
            self.clear_text_boxes()
            current_row = self.listWidget_items.currentRow()
            if self.listWidget_items.item(current_row):
                selected_user = self.listWidget_items.item(current_row).text()
                current_user: User = self.PANEL.get_user(selected_user, self.TOKEN)

                data = current_user.get_all()

                title_translate = User.title_translate()

                form_dict = self.get_textboxes_dict()

                for i in title_translate:
                    current_text_box = form_dict.get(i)
                    current_data = data.get(title_translate[i])

                    if i == "Data Limit":
                        if current_data:
                            current_text_box.setStyleSheet(
                                StyleSheet.TEXT_EDITOR_BORDER_GREY)

                            data_limit = current_data / self.GB_SIZE

                            current_text_box.setValue(data_limit)
                    elif i == "Expire":
                        if current_data:
                            current_text_box.setStyleSheet(
                                StyleSheet.TEXT_EDITOR_BORDER_GREY)

                            expire_date = (current_data - time.time())
                            expire_date = math.ceil(expire_date / self.days_in_seconds)

                            current_text_box.setText(str(expire_date))
                    elif i == "Status":
                        if current_data:
                            if current_data == "active":
                                self.comboBox_status.setCurrentIndex(0)
                            elif current_data == "disabled":
                                self.comboBox_status.setCurrentIndex(1)
                            elif current_data == "expired":
                                self.comboBox_status.setCurrentIndex(2)

                    elif i == "Used Traffic":
                        current_text_box.setText(convert_size(current_data))

    def save_item(self):
        current_row = self.listWidget_items.currentRow()
        if self.listWidget_items.item(current_row):
            selected_user = self.listWidget_items.item(current_row).text()
            current_user: User = self.PANEL.get_user(selected_user, self.TOKEN)

            new_user = User(
                proxies=current_user.proxies,
                inbounds=current_user.inbounds,
            )

            form_dict = self.get_textboxes_dict()

            titles_translate = User.title_translate()

            for i in form_dict:
                current_user_property = titles_translate.get(i)

                if current_user_property == "data_limit":
                    textbox_value = filter_name_for_cast_and_info(form_dict[i].text())
                    if textbox_value:
                        new_data_limit = float(textbox_value) * self.GB_SIZE
                        setattr(new_user, current_user_property, new_data_limit)

                        if not getattr(new_user, current_user_property):
                            new_data_limit = new_data_limit
                            setattr(new_user, current_user_property, new_data_limit)

                elif current_user_property == "expire":
                    textbox_value = filter_name_for_cast_and_info(form_dict[i].text())
                    if textbox_value:
                        new_date = time.time() - self.get_today_seconds() + (
                            math.ceil(float(textbox_value) * self.days_in_seconds))

                        setattr(new_user, current_user_property, new_date)

                        if not getattr(new_user, current_user_property):
                            setattr(new_user, current_user_property, new_date)

                elif current_user_property == "status":
                    status = ""
                    current_status = self.comboBox_status.currentIndex()
                    if current_status == 0:
                        status = "active"
                    elif current_status == 1:
                        status = "disabled"
                    elif current_status == 2:
                        break

                    setattr(new_user, current_user_property, status)

                    if not getattr(new_user, current_user_property):
                        setattr(new_user, current_user_property, status)
                else:
                    textbox_value = filter_name_for_cast_and_info(form_dict[i].text())
                    if textbox_value:
                        setattr(new_user, current_user_property, textbox_value)

                        if not getattr(new_user, current_user_property):
                            setattr(new_user, current_user_property, textbox_value)

            self.PANEL.modify_user(current_user.username, self.TOKEN, new_user)
            self.clear_text_boxes()

    def add_30_days(self):
        current_row = self.listWidget_items.currentRow()
        if self.listWidget_items.item(current_row):
            selected_user = self.listWidget_items.item(current_row).text()
            current_user: User = self.PANEL.get_user(selected_user, self.TOKEN)

            new_date = time.time() - self.get_today_seconds() + (self.days_in_seconds * 30)
            current_user.expire = new_date
            current_user.data_limit = float(self.spinBox_data_limit.text()) * self.GB_SIZE
            current_user.status = 'active'

            self.PANEL.modify_user(current_user.username, token=self.TOKEN, user=current_user)
            self.PANEL.reset_user_traffic(current_user.username, token=self.TOKEN)
            self.clear_search()

    def reset_usage(self):
        current_row = self.listWidget_items.currentRow()
        if self.listWidget_items.item(current_row):
            selected_user = self.listWidget_items.item(current_row).text()
            current_user: User = self.PANEL.get_user(selected_user, self.TOKEN)
            current_user.status = 'active'

            self.PANEL.reset_user_traffic(current_user.username, token=self.TOKEN)
            self.clear_search()

    def get_textboxes_dict(self):
        form_dict = {
            "Expire": self.lineEdit_expire,
            "Data Limit": self.spinBox_data_limit,
            "Used Traffic": self.label_used_traffic,
            "Status": self.comboBox_status,
        }

        return form_dict

    def scan_empty_fields(self, check_active=0, check_expired=0, check_limited=0, check_disabled=0):
        list_array = []

        for i in self.Users:
            current_user: User = i

            if check_active == 1:
                if current_user.status == "active":
                    list_array.append(current_user.username)
            elif check_expired == 1:
                if current_user.status == "expired":
                    list_array.append(current_user.username)
            elif check_limited == 1:
                if current_user.status == "limited":
                    list_array.append(current_user.username)
            elif check_disabled == 1:
                if current_user.status == "disabled":
                    list_array.append(current_user.username)

        self.listWidget_items.clear()

        for i in list_array:
            item = QListWidgetItem(str(i))
            self.listWidget_items.addItem(item)

        self.clear_text_boxes()

    def get_today_seconds(self) -> int:
        now = datetime.now()
        seconds_since_midnight = math.ceil(
            (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds())

        return seconds_since_midnight

    def clear_items(self):
        self.listWidget_items.clear()

        self.clear_text_boxes()

    def clear_text_boxes(self):
        self.lineEdit_expire.clear()
        self.spinBox_data_limit.setValue(0)
        self.label_used_traffic.setText("")

        self.spinBox_data_limit.setStyleSheet(
            StyleSheet.TEXT_EDITOR_BORDER_GREY)

    def remove_selected_item(self):
        list_count = self.listWidget_items.count()
        if list_count > 0:
            current_row = self.listWidget_items.currentRow()

            self.listWidget_items.takeItem(current_row)


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()
