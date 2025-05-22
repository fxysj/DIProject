#自定义事件类
from llama_index.core.workflow import Event

class UserInputEvent(Event):
    def __init__(self, text: str):
        super().__init__({"text": text})

    @property
    def text(self):
        return self.data["text"]

class IntentEvent(Event):
    def __init__(self, text: str, intent: str = None):
        super().__init__({"text": text, "intent": intent})

    @property
    def text(self):
        return self.data["text"]

    @property
    def intent(self):
        return self.data.get("intent")

    @intent.setter
    def intent(self, value):
        self.data["intent"] = value

class SentimentEvent(Event):
    def __init__(self, text: str, intent: str, sentiment: str = None):
        super().__init__({"text": text, "intent": intent, "sentiment": sentiment})

    @property
    def text(self):
        return self.data["text"]

    @property
    def intent(self):
        return self.data["intent"]

    @property
    def sentiment(self):
        return self.data.get("sentiment")

    @sentiment.setter
    def sentiment(self, value):
        self.data["sentiment"] = value

class QueryEvent(Event):
    def __init__(self, text: str, intent: str, sentiment: str, summary: str = None):
        super().__init__({"text": text, "intent": intent, "sentiment": sentiment, "summary": summary})

    @property
    def text(self):
        return self.data["text"]

    @property
    def intent(self):
        return self.data["intent"]

    @property
    def sentiment(self):
        return self.data["sentiment"]

    @property
    def summary(self):
        return self.data.get("summary")

    @summary.setter
    def summary(self, value):
        self.data["summary"] = value

class ResponseEvent(Event):
    def __init__(self, intent: str, sentiment: str, summary: str, message: str = None):
        super().__init__({"intent": intent, "sentiment": sentiment, "summary": summary, "message": message})

    @property
    def intent(self):
        return self.data["intent"]

    @property
    def sentiment(self):
        return self.data["sentiment"]

    @property
    def summary(self):
        return self.data["summary"]

    @property
    def message(self):
        return self.data.get("message")

    @message.setter
    def message(self, value):
        self.data["message"] = value
