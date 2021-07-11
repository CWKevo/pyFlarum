from typing import List, Optional, Union

from ...extensions import ExtensionMixin
from ...extensions.admin import AdminFlarumUserMixin

from ...session import FlarumUser
from ...error_handler import parse_request


AUTHOR = 'malago'
NAME = 'achievements'
ID = f"{AUTHOR}-{NAME}"


class Achievement(dict):
    """
        An achievement (Malago's Achievements extension).
    """

    def __init__(self, user: 'FlarumUser', _fetched_data: dict):
        self.user = user

        super().__init__(_fetched_data)


    @property
    def data(self) -> dict:
        return self.get("data", {})


    @property
    def type(self) -> Optional[str]:
        return self.data.get("type", None)


    @property
    def attributes(self) -> dict:
        return self.data.get("attributes", {})


    @property
    def name(self) -> Optional[str]:
        return self.attributes.get("name", None)


    @property
    def description(self) -> Optional[str]:
        return self.attributes.get("description", None)


    @property
    def computation(self) -> Optional[str]:
        return self.attributes.get("computation", None)


    @property
    def points(self):
        raw = self.attributes.get("points", None)

        if raw:
            return int(raw)


    @property
    def icon(self) -> Optional[str]:
        return self.attributes.get("icon", None)


    @property
    def rectangle(self) -> Optional[str]:
        """
            No, I have no idea what this is either.
        """

        return self.attributes.get("rectangle", None)


    @property
    def active(self) -> Optional[bool]:
        raw = self.attributes.get("active", None)

        if raw:
            return bool(raw)


    @property
    def hidden(self) -> Optional[bool]:
        raw = self.attributes.get("hidden", None)

        if raw:
            return bool(raw)


    @property
    def new(self) -> Optional[str]:
        return self.attributes.get("new", None)



class AchievementsAdminFlarumUserMixin(AdminFlarumUserMixin):
    def update_settings(self, show_achievement_list_in_each_post_footer: Optional[bool]=None, show_achievement_list_in_user_badge: Optional[bool]=None):
        post_data = {}


        if isinstance(show_achievement_list_in_each_post_footer, bool):
            post_data["malago-achievements.show-post-footer"] = show_achievement_list_in_each_post_footer

        if isinstance(show_achievement_list_in_user_badge, bool):
            post_data["malago-achievements.show-user-card"] = show_achievement_list_in_user_badge


        raw = self.session.post(f"{self.api_urls['settings']}", json=post_data)
        parse_request(raw)

        return True


    def create_achievement(self, name: str, description: str, computation: str, points: int, image_url_or_fa_icon: str, active: Union[bool, int]=1, hidden: Union[bool, int]=0):
        post_data = {
            "data": {
                "type": "achievements",
                "attributes": {
                    "name": name,
                    "description": description,
                    "computation": computation,
                    "points": points,
                    "image": image_url_or_fa_icon,
                    "rectangle": "0,0,,", # TODO: What is this?
                    "active": int(active),
                    "hidden": int(hidden)
                }
            }
        }

        raw = self.session.post(f"{self.api_urls['base']}/achievements", json=post_data)
        json = parse_request(raw)

        return Achievement(user=self, _fetched_data=json)


    def get_all_achievements(self):
        raw = self.session.get(f"{self.api_urls['base']}/achievements")
        json = parse_request(raw)

        all_achievements = list() # type: List[Achievement]

        for raw_achievement in json['data']:
            achievement = Achievement(user=self, _fetched_data=dict(data=raw_achievement))
            all_achievements.append(achievement)

        return all_achievements



class AchievementsExtension(ExtensionMixin):
    def __init__(self):
        self.name = NAME
        self.author = AUTHOR
        self.id = ID


    def mixin(self):
        super().mixin(self, AdminFlarumUserMixin, AchievementsAdminFlarumUserMixin)
