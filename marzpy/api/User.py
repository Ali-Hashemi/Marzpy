from .send_requests import *


class User:
    def __init__(
            self,
            proxies: dict = None,
            inbounds: dict = None,
            data_limit_reset_strategy: str = None,
            username: str = None,
            status: str = None,
            expire: float = None,
            used_traffic=None,
            data_limit: float = None,
            lifetime_used_traffic=None,
            created_at=None,
            subscription_url=None,
            links=[],
            excluded_inbounds={},
            note="",
            sub_updated_at="",
            sub_last_user_agent="",
            online_at="",
            on_hold_expire_duration="",
            on_hold_timeout="",
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

    def get_all(self):
        dictionary = {
            "expire": self.expire,
            "data_limit": self.data_limit,
            "used_traffic": self.used_traffic,
            "status": self.status,
        }

        return dictionary

    @staticmethod
    def title_translate():
        dictionary = {
            "Expire": "expire",
            "Data Limit": "data_limit",
            "Used Traffic": "used_traffic",
            "Status": "status"
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
