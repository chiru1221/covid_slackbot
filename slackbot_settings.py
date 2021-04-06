with open('key.txt', 'r') as f:
    key = list(map(lambda x: x.strip(), f.readline()))
API_TOKEN = key[0]
DEFAULT_REPLY = "hello"
PLUGINS = ['plugins']
