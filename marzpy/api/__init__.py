from .Admin import Admin
from .Node import NodeMethods
from .Subscription import Subscription
from .Core import Core
from .User import UserMethods
from .Template import TemplateMethods
from .System import System


class Methods(
    Admin, NodeMethods, Subscription, Core, UserMethods, TemplateMethods, System
):
    def __init__(self, username: str, password: str, panel_address: str):
        super().__init__(username, password, panel_address)
