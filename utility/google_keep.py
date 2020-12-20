import gkeepapi
from gkeepapi.node import TopLevelNode


class GoogleKeep:
    def __init__(self, account: str, password: str, note_id: str):
        self._keep = gkeepapi.Keep()
        self.account = account
        self.password = password
        self.note_id = note_id
        self._keep.login(self.account, self.password)

    def _get_note(self) -> TopLevelNode:
        return self._keep.get(self.note_id)

    def get_note_title(self):
        return self._get_note().title

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
