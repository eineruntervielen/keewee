"""Implements an autovivification dictionary for global state recording and management"""


class KeeWeeRepo(dict):
    """Global repository for state recording and management"""

    def __missing__(self, kee):
        wee = self[kee] = type(self)()
        return wee


_repo: KeeWeeRepo = KeeWeeRepo()
