import redis
import json

class RedisMemory:
    def __init__(self, host='localhost', port=6379, db=0):
        self.r = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def get_history(self, session_id):
        key = f"session:{session_id}:history"
        history = self.r.lrange(key, 0, -1)
        return [json.loads(item) for item in history]

    def save_history(self, session_id, user_message, agent_reply):
        key = f"session:{session_id}:history"
        item = json.dumps({"user": user_message, "agent": agent_reply})
        self.r.rpush(key, item) 