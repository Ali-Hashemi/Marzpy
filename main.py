from marzpy import Marzban
from marzpy.api.User import User
import time

panel = Marzban("z", "z", "https://myblog.intonature.tech")

mytoken = panel.get_token()

current_user = panel.get_user("lebron", mytoken)

new_user = User(
    proxies=current_user.proxies,
    inbounds=current_user.inbounds,
    expire=1703795399,
    data_limit=300000
)

# result2 = panel.modify_user(current_user.username, token=mytoken, user=new_user)

