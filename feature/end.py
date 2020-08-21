from feature.text import Text


class End(Text):

    def __init__(self, sender_name: str = "Bot"):
        super().__init__(f"""
-----
你的,
{sender_name}
""")
