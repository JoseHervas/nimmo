class MessageStore:
    __instance = None
    __messages = [
        {"role": "system", "content": "Eres Klaus, el asistente personal de Jose"}
    ]

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def add_message(self, message):
        self.__messages.append(message)

    def get_messages(self):
        return self.__messages