import redis as red

redis = red.Redis('localhost', 6379, charset="utf-8", decode_responses=True)