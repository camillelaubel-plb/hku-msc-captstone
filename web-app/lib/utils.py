import collections
import os

Page = collections.namedtuple('Page', ['module', 'url', 'display'])


def get_full_path(relative_path_from_app_root):
    app_root = os.path.join(
        os.path.dirname(
            os.path.realpath(__file__)
        ),
        '..'
    )
    return os.path.join(app_root, relative_path_from_app_root)
