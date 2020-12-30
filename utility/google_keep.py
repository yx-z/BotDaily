import gkeepapi
from gkeepapi.node import TopLevelNode


class GoogleKeep:
    def __init__(self, account: str, password: str, title: str):
        self._keep = gkeepapi.Keep()
        self.account = account
        self.password = password
        self.title = title
        self._keep.login(self.account, self.password)

    def _get_note(self) -> TopLevelNode:
        return self._keep.find(query=self.title)[0]

    def get_note_txt(self):
        return self._get_note().text

    def get_note_imgs(self):
        return list(map(self._keep.getMediaLink, self._get_note().images))

    def set_note_txt(self, txt: str):
        note = self._get_note()
        note.text = txt
        self._keep.sync()

    def clear_note(self):
        self.set_note_txt("")
