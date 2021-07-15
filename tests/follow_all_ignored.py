from typing import Union


from normalize_path import normalize_path
normalize_path()

from dotenv import load_dotenv
load_dotenv()

import os

from pyflarum import FlarumUser

from pyflarum.flarum.core.filters import Filter

from pyflarum.extensions import absolutely_all
from pyflarum.extensions.flarum import Flarum_Subscriptions


EXTENSIONS = [
    absolutely_all.AbsolutelyAllExtension,
    Flarum_Subscriptions.SubscriptionsExtension
]

user = FlarumUser(forum_url=os.environ['forum_url'], username='test', password=os.environ['account_password'], extensions=EXTENSIONS) # type: absolutely_all.AbsolutelyAllFlarumUserMixin


def follow_all():
    discussion: Union[Flarum_Subscriptions.SubscriptionsDiscussionFromBulkMixin]

    for discussions in user.absolutely_all_discussions(Filter(query='is:ignored')):
        for discussion in discussions:
            discussion = discussion.follow()
            print(f"Now following ignored discussion {discussion.id} ({discussion.url})")


if __name__ == "__main__":
    follow_all()
