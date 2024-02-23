from .send_requests import *
from datetime import datetime


class User:
    def __init__(
            self,
            username: str=None,
            proxies: dict=None,
            inbounds: dict=None,
            expire: float=None,
            data_limit: float=None,
            data_limit_reset_strategy: str=None,
            status=None,
            used_traffic=None,
            lifetime_used_traffic=None,
            created_at=None,
            links=[],
            subscription_url=None,
            excluded_inbounds={},
            note=None,
            sub_updated_at=None,
            sub_last_user_agent=None,
            online_at=None,
            on_hold_expire_duration=None,
            on_hold_timeout=None,
    ):
        self.username = username
        self.proxies = proxies
        self.inbounds = inbounds
        self.expire = expire
        self.data_limit = data_limit
        self.data_limit_reset_strategy = data_limit_reset_strategy
        self.status = status
        self.used_traffic = used_traffic
        self.lifetime_used_traffic = lifetime_used_traffic
        self.created_at = created_at
        self.links = links
        self.subscription_url = subscription_url
        self.excluded_inbounds = excluded_inbounds
        self.note = note
        self.sub_updated_at = sub_updated_at
        self.sub_last_user_agent = sub_last_user_agent
        self.online_at = online_at
        self.on_hold_expire_duration = on_hold_expire_duration
        self.on_hold_timeout = on_hold_timeout

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def proxies(self):
        return self._proxies

    @proxies.setter
    def proxies(self, value):
        self._proxies = value

    @property
    def inbounds(self):
        return self._inbounds

    @inbounds.setter
    def inbounds(self, value):
        self._inbounds = value

    @property
    def expire(self):
        return self._expire

    @expire.setter
    def expire(self, value):
        self._expire = value

    @property
    def data_limit(self):
        return self._data_limit

    @data_limit.setter
    def data_limit(self, value):
        self._data_limit = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def used_traffic(self):
        return self._used_traffic

    @used_traffic.setter
    def used_traffic(self, value):
        self._used_traffic = value

    @property
    def lifetime_used_traffic(self):
        return self._lifetime_used_traffic

    @lifetime_used_traffic.setter
    def lifetime_used_traffic(self, value):
        self._lifetime_used_traffic = value

    @property
    def created_at(self):
        return self._created_at

    @created_at.setter
    def created_at(self, value):
        self._created_at = value

    @property
    def subscription_url(self):
        return self._subscription_url

    @subscription_url.setter
    def subscription_url(self, value):
        self._subscription_url = value

    @property
    def sub_updated_at(self):
        return self._sub_updated_at

    @sub_updated_at.setter
    def sub_updated_at(self, value):
        self._sub_updated_at = value

    @property
    def sub_last_user_agent(self):
        return self._sub_last_user_agent

    @sub_last_user_agent.setter
    def sub_last_user_agent(self, value):
        self._sub_last_user_agent = value

    @property
    def online_at(self):
        return self._online_at

    @online_at.setter
    def online_at(self, value):
        self._online_at = value

    def get_all(self):
        dictionary = {
            "username": self.username,
            "proxies": self.proxies,
            "inbounds": self.inbounds,
            "expire": self.expire,
            "data_limit": self.data_limit,
            "status": self.status,
            "used_traffic": self.used_traffic,
            "lifetime_used_traffic": self.lifetime_used_traffic,
            "created_at": self.created_at,
            "subscription_url": self.subscription_url,
            "sub_updated_at": self.sub_updated_at,
            "sub_last_user_agent": self._sub_last_user_agent,
            "online_at": self.online_at,
        }

        return dictionary

    @staticmethod
    def title_translate():
        dictionary = {
            "Username": "username",
            "Proxies": "proxies",
            "Inbounds": "inbounds",
            "Expire": "expire",
            "Data Limit": "data_limit",
            "Status": "status",
            "Used Traffic": "used_traffic",
            "Lifetime Used Traffic": "lifetime_used_traffic",
            "Created At": "created_at",
            "Subscription Url": "subscription_url",
            "Sub Updated At": "sub_updated_at",
            "Sub Last User Agent": "sub_last_user_agent",
            "Online At": "online_at",
        }
        return dictionary


class UserMethods:
    def add_user(self, user: User, token: dict):
        """add new user.

        Parameters:
            user (``api.User``) : User Object

            token (``dict``) : Authorization token

        Returns: `~User`: api.User object
        """
        request = send_request(
            endpoint="user", token=token, method="post", data=user.__dict__
        )

        return User(**request)

    def get_user(self, user_username: str, token: dict):
        """get exist user information by username.

        Parameters:
            user_username (``str``) : username of user

            token (``dict``) : Authorization token

        Returns: `~User`: api.User object
        """
        request = send_request(f"user/{user_username}", token=token, method="get")
        return User(**request)

    def modify_user(self, user_username: str, token: dict, user: object):
        """edit exist user by username.

        Parameters:
            user_username (``str``) : username of user

            token (``dict``) : Authorization token

            user (``api.User``) : User Object

        Returns: `~User`: api.User object
        """
        request = send_request(f"user/{user_username}", token, "put", user.__dict__)
        return User(**request)

    def delete_user(self, user_username: str, token: dict):
        """delete exist user by username.

        Parameters:
            user_username (``str``) : username of user

            token (``dict``) : Authorization token

        Returns: `~str`: success
        """
        send_request(f"user/{user_username}", token, "delete")
        return "success"

    def reset_user_traffic(self, user_username: str, token: dict):
        """reset exist user traffic by username.

        Parameters:
            user_username (``str``) : username of user

            token (``dict``) : Authorization token

        Returns: `~str`: success
        """
        send_request(f"user/{user_username}/reset", token, "post")
        return "success"

    def get_all_users(self, token: dict):
        """get all users list.

        Parameters:
            token (``dict``) : Authorization token

        Returns:
            `~list`: list of users
        """
        request = send_request("users", token, "get")
        user_list = [
            User(
                username="",
                proxies={},
                inbounds={},
                expire=0,
                data_limit=0,
                data_limit_reset_strategy="",
            )
        ]
        for user in request["users"]:
            user_list.append(User(**user))
        del user_list[0]
        return user_list

    def reset_all_users_traffic(self, token: dict):
        """reset all users traffic.

        Parameters:
            token (``dict``) : Authorization token

        Returns: `~str`: success
        """
        send_request("users/reset", token, "post")
        return "success"

    def get_user_usage(self, user_username: str, token: dict):
        """get user usage by username.

        Parameters:
            user_username (``str``) : username of user

            token (``dict``) : Authorization token

        Returns: `~dict`: dict of user usage
        """
        return send_request(f"user/{user_username}/usage", token, "get")["usages"]

    def get_all_users_count(self, token: dict):
        """get all users count.

        Parameters:
            token (``dict``) : Authorization token

        Returns: `~int`: count of users
        """
        return self.get_all_users(token)["content"]["total"]
