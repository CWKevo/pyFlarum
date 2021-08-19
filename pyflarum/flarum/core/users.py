from typing import Optional

from datetime import datetime

from ..core import BaseFlarumBulkObject, BaseFlarumIndividualObject
from ...datetime_conversions import flarum_to_datetime


class Users(BaseFlarumBulkObject):
    """
        A data of multiple users fetched from the API.
    """


    def __iter__(self):
        return iter(self.get_users())


    def get_users(self) -> list['UserFromBulk']:
        """
            All users from the `Users` object.
        """

        all_users = [] # type: list[UserFromBulk]

        for raw_user in self.data:
            if raw_user.get("type", None) == 'users':
                user = UserFromBulk(user=self.user, _fetched_data=dict(data=raw_user, _parent_included=self.included))
                all_users.append(user)

        return all_users


class UserFromNotification(BaseFlarumIndividualObject):
    """
        An user from `BaseNotification`
    """


    @property
    def username(self) -> Optional[str]:
        """
            The user's username.
        """

        return self.attributes.get("username", None)


    @property
    def email(self) -> Optional[str]:
        """
            The user's E-mail, if you have permission to view it.
        """

        return self.attributes.get("email", None)


    @property
    def isEmailConfirmed(self) -> bool:
        """
            Whether or not this user confirmed their E-mail address.

            You must have the permission to view the user's E-mail address
            in order to know this too in the first place.
        """

        return self.attributes.get("isEmailConfirmed", False)


    @property
    def displayName(self) -> Optional[str]:
        """
            The display name/nickname of the user.
        """

        return self.attributes.get("displayName", None)


    @property
    def avatarUrl(self) -> Optional[str]:
        """
            The user's avatar URL.
        """

        return self.attributes.get("avatarUrl", None)


    @property
    def slug(self) -> Optional[str]:
        """
            The user's slug.
        """

        return self.attributes.get("slug", None)



class UserFromBulk(UserFromNotification):
    """
        An user from `Users`.
    """


    @property
    def joinTime(self) -> Optional[datetime]:
        """
            The `datetime` of when the user had joined this forum.
        """

        raw = self.attributes.get("joinTime", None)

        return flarum_to_datetime(raw)


    @property
    def discussionCount(self) -> Optional[int]:
        """
            The user's discussion count.
        """

        return self.attributes.get("discussionCount", None)


    @property
    def commentCount(self) -> Optional[int]:
        """
            The user's comment/post count.
        """

        return self.attributes.get("commentCount", None)


    @property
    def canEdit(self) -> bool:
        """
            Whether or not you are able to edit this user.
        """

        return self.attributes.get("canEdit", False)


    @property
    def canEditCredentials(self) -> bool:
        """
            Whether or not you are able to edit this user's credentials.
        """

        return self.attributes.get("canEditCredentials", False)


    @property
    def canEditGroups(self) -> bool:
        """
            Whether or not you are able to edit this user's groups.
        """

        return self.attributes.get("canEditGroups", False)


    @property
    def canDelete(self) -> bool:
        """
            Whether or not you are able to scronch this user forever.
        """

        return self.attributes.get("canDelete", False)



class User(UserFromBulk):
    """
        An user that was fetched from the API.
    """

    pass



class MyUser(User):
    """
        Your user, contains fullest user data.
    """

    @property
    def markedAllAsReadAt(self) -> Optional[datetime]:
        """
            When did you mark all discussions as read.
        """

        raw = self.attributes.get("markedAllAsReadAt", None)

        return flarum_to_datetime(raw)
    

    @property
    def unreadNotificationCount(self) -> Optional[int]:
        """
            Amount of your unread notifications.
        """

        return self.attributes.get("unreadNotificationCount", None)


    @property
    def newNotificationCount(self) -> Optional[int]:
        """
            Amount of your new notifications.
        """

        return self.attributes.get("newNotificationCount", None)


    @property
    def preferences(self) -> dict:
        """
            A raw `dict` of your preferences (for notifications).
        """

        return self.attributes.get("preferences", {})

