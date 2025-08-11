class Bot:
    def __init__(self, token, default=None):
        self.token = token
        self.default = default
        class Session:
            async def close(self):
                return None
        self.session = Session()

    async def send_message(self, chat_id=None, text="", **kwargs):
        """Simple stub that pretends to send a message."""
        return {"chat_id": chat_id, "text": text}
