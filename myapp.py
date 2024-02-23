from marzpy.api.User import User
import time
import math
from datetime import datetime
from marzpy import Marzban
from Classes.ClassUtility import Print

GB_SIZE = (1024 * 1024 * 1024)
days_in_seconds = 86400 + 50

panel_amz = Marzban("mike", "z", "https://amzpnl1.intonature.tech")
panel_dag = Marzban("mike", "z", "https://v1.fnldagger.shop")
panel_myblog = Marzban("z", "z", "https://myblog.intonature.tech")

main_panel = None
mytoken = None

# print("Select Panel :")
# print("1. Amazon")
# print("2. Dagger")
# print("3. Myblog")
#
# choice = ""
#
# while choice != "q":
#     choice = input("What would you like to do (press q to quit)   ")
#     print("")
#     if choice == '1':
#         main_panel = panel_amz
#         break
#     elif choice == '2':
#         main_panel = panel_dag
#         break
#     elif choice == '3':
#         main_panel = panel_myblog
#         break
#
#     else:
#         print("")
#         print("That is not a valid input.")
#         exit()

main_panel = panel_myblog

if main_panel:
    mytoken = main_panel.get_token()

if not mytoken:
    exit()

ALL_USERS = main_panel.get_all_users(mytoken)


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def renew_user(user: User):
    days = input("Enter Days : ")

    data_limit = input("Enter Data Limit : ")

    # Print.print_black("")

    if days and days.isnumeric():
        user.expire = get_midnight_time() + (days_in_seconds * int(days))
    else:
        user.expire = get_midnight_time() + (days_in_seconds * 30)

    if data_limit and data_limit.isnumeric():
        user.data_limit = int(data_limit)
    else:
        user.data_limit = user.data_limit

    user.status = 'active'

    main_panel.modify_user(user.username, token=mytoken, user=user)
    main_panel.reset_user_traffic(user.username, token=mytoken)


def reset_usage(self, user: User):
    user.status = 'active'

    main_panel.reset_user_traffic(user.username, token=self.TOKEN)
    self.clear_search()


def get_midnight_time():
    seconds_left_till_midnight = days_in_seconds - get_today_seconds_gone()

    midnight_seconds = time.time() + seconds_left_till_midnight

    return midnight_seconds


def get_today_seconds_gone() -> int:
    now = datetime.now()
    seconds_since_midnight = math.ceil(
        (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds())

    return seconds_since_midnight


def scan_users(check_active=0, check_expired=0, check_limited=0, check_disabled=0):
    list_array = []

    users = ALL_USERS

    for i in users:
        current_user: User = i

        if check_active == 1:
            if current_user.status == "active":
                list_array.append(i)
        elif check_expired == 1:
            if current_user.status == "expired":
                list_array.append(i)
        elif check_limited == 1:
            if current_user.status == "limited":
                list_array.append(i)
        elif check_disabled == 1:
            if current_user.status == "disabled":
                list_array.append(i)
        elif check_expired and check_limited:
            if current_user.status == "expired" or current_user.status == "limited":
                list_array.append(i)

    return list_array


def scan_reminder_days():
    users = scan_users(check_active=1)

    for i in users:
        current_user: User = i

        two_days_remain = int(get_midnight_time() + (days_in_seconds * 2))

        if current_user.expire and current_user.expire < two_days_remain:
            Print.print_red(" ----> " + current_user.username)


def scan_reminder_volume():
    users = scan_users(check_active=1)

    for i in users:
        current_user: User = i
        remaining_data = current_user.data_limit - current_user.used_traffic

        if remaining_data < 1073741824:
            Print.print_red(" ----> " + current_user.username)


def show_and_renew_users(users):
    list = {}
    for index, value in enumerate(users):
        current_user: User = value
        list[index + 1] = current_user

    for x in list:
        current_user: User = list[x]
        print_this = "----> " + str(x) + ".   " + current_user.username
        Print.print_black(print_this)

    choice_1 = ""
    while choice_1 != "q" or choice_1 != "quit()":
        Print.print_black("")
        choice_1 = input("Which User to renew ? (press q to main menu)")

        Print.print_black("")

        if choice_1.isnumeric():
            selected_user: User = list[int(choice_1)]

            renew_user(selected_user)

            Print.print_green(selected_user.username + " has been renewed !")

            list.pop(int(choice_1))
        else:
            Print.print_black("")
            Print.print_black("That is not a valid input.")

    if choice_1 == "q" or choice_1=="quit()":
        main_menu()


def disable_users(users):
    list = {}
    for index, value in enumerate(users):
        current_user: User = value
        list[index + 1] = current_user

    for x in list:
        current_user: User = list[x]
        print_this = "----> " + str(x) + ".   " + current_user.username
        Print.print_black(print_this)

    choice_1 = ""
    while choice_1 != "q" or choice_1 != "quit()":
        Print.print_black("")
        choice_1 = input("Which User to disable ? (press q to main menu)")

        Print.print_black("")

        if choice_1.isnumeric():

            selected_user: User = list[int(choice_1)]

            selected_user.status = 'disabled'

            main_panel.modify_user(selected_user.username, token=mytoken, user=selected_user)

            list.pop(int(choice_1))

            Print.print_blue(selected_user.username + " has been disabled !")

        else:
            Print.print_black("")
            Print.print_black("That is not a valid input.")

    if choice_1 == "q" or choice_1=="quit()":
        main_menu()


def print_list(users):
    for i in users:
        user: User = i
        Print.print_cyan(user.username)


def main_menu():
    Print.print_black("Select Operation :")
    Print.print_black("1. Show Expired")
    Print.print_black("2. Show Limited")
    Print.print_black("3. Disable Users")
    Print.print_black("4. Show 2 Days Remaining")
    Print.print_black("5. Show 1 GB Remaining")

    choice = ""

    while choice != "q"  or choice != "quit()":
        Print.print_black("")
        choice = input("What would you like to do? (press q to quit)")
        Print.print_black("")
        if choice == '1':
            show_and_renew_users(scan_users(check_expired=1))
        elif choice == '2':
            show_and_renew_users(scan_users(check_limited=1))
        elif choice == '3':
            disable_users(scan_users(check_expired=1, check_limited=1))
        elif choice == '4':
            scan_reminder_days()
        elif choice == '5':
            scan_reminder_volume()

        else:
            Print.print_black("")
            Print.print_black("That is not a valid input.")


main_menu()
