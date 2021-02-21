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
        candidates = list(
            self._keep.find(func=lambda x: x.title.startswith(self.title))
        )
        # get index by suffix in title
        indices = list(map(lambda x: int(x.title[len(self.title) :]), candidates))
        # get candidate w/ largest index
        return sorted(zip(candidates, indices), key=lambda x: x[1])[-1][0]

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

    def create_note(self, title: str, text: str):
        self._keep.createNote(title, text)
