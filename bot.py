import requests
import json
import os
from core.helper import get_headers, countdown_timer, extract_user_data, config
from colorama import *
from base64 import urlsafe_b64decode
import random
from datetime import datetime
import time


class PAWS:
    def __init__(self) -> None:
        self.session = requests.Session()


    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        banner = f"""{Fore.GREEN}
                                 ██████  ██    ██   ██████  ██    ██  ███    ███  ██████   ███████  ██████  
                                ██       ██    ██  ██       ██    ██  ████  ████  ██   ██  ██       ██   ██ 
                                ██       ██    ██  ██       ██    ██  ██ ████ ██  ██████   █████    ██████  
                                ██       ██    ██  ██       ██    ██  ██  ██  ██  ██   ██  ██       ██   ██ 
                                 ██████   ██████    ██████   ██████   ██      ██  ██████   ███████  ██   ██     
                                    """
        print(Fore.GREEN + Style.BRIGHT + banner + Style.RESET_ALL)
        print(Fore.GREEN + f" PAWS Bot")
        print(Fore.RED + f" FREE TO USE = Join us on {Fore.GREEN}t.me/cucumber_scripts")
        print(Fore.YELLOW + f" before start please '{Fore.GREEN}git pull{Fore.YELLOW}' to update bot")
        print(f"{Fore.WHITE}~" * 60)

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

    def user_auth(self, query: str, retries=5):
        url = 'https://api.paws.community/v1/user/auth'
        data = json.dumps({'data':query, 'referralCode':'qEKFjt3Y'})
        self.headers.update({
            'Content-Type': 'application/json'
        })

        for attempt in range(retries):
            try:
                response = self.session.post(url, headers=self.headers, data=data)
                response.raise_for_status()
                result = response.json()
                if result['success']:
                    token = result['data'][0] if isinstance(result['data'][0], str) else None
                    return token
                else:
                    return None
            except (requests.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED+Style.BRIGHT}HTTP ERROR{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
        
    def user_data(self, token: str, retries=5):
        url = 'https://api.paws.community/v1/user'
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

        for attempt in range(retries):
            try:
                response = self.session.get(url, headers=self.headers)
                response.raise_for_status()
                result = response.json()
                if result['success']:
                    return result['data']
                else:
                    return None
            except (requests.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED+Style.BRIGHT}HTTP ERROR{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
        
    def quest_lists(self, token: str, retries=5):
        url = 'https://api.paws.community/v1/quests/list'
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

        for attempt in range(retries):
            try:
                response = self.session.get(url, headers=self.headers)
                response.raise_for_status()
                result = response.json()
                if result['success']:
                    return result['data']
                else:
                    return None
            except (requests.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED+Style.BRIGHT}HTTP ERROR{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None

    def set_proxy(self, proxy):
        self.session.proxies = {
            "http": proxy,
            "https": proxy,
        }
        if '@' in proxy:
            host_port = proxy.split('@')[-1]
        else:
            host_port = proxy.split('//')[-1]
        return host_port

    def start_quests(self, token: str, quest_id: str, retries=5):
        url = 'https://api.paws.community/v1/quests/completed'
        data = json.dumps({'questId':quest_id})
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

        for attempt in range(retries):
            try:
                response = self.session.post(url, headers=self.headers, data=data)
                response.raise_for_status()
                result = response.json()
                if result['success']:
                    return result['data']
                else:
                    return None
            except (requests.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED+Style.BRIGHT}HTTP ERROR{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None

    def connect_wallet(self, token: str, wallet: str):
        url = 'https://api.paws.community/v1/user/wallet'
        data = json.dumps({'wallet': wallet})
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })


        try:
            response = self.session.post(url, headers=self.headers, data=data)
            response.raise_for_status()
            result = response.json()
            if result['success']:
                self.log(Fore.GREEN + f"Successfully connected to wallet")
                return
            else:
                self.log(Fore.RED + f"Failed connected to wallet")
                return
        except (requests.RequestException, ValueError) as e:
                print(
                    f"{Fore.RED+Style.BRIGHT}HTTP ERROR{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} Retrying... {Style.RESET_ALL}",
                    end="\r",
                    flush=True
                )
        except Exception as e:
            print(e)

    def claim_quests(self, token: str, quest_id: str, retries=5):
        url = 'https://api.paws.community/v1/quests/claim'
        data = json.dumps({'questId':quest_id})
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

        for attempt in range(retries):
            try:
                response = self.session.post(url, headers=self.headers, data=data)
                response.raise_for_status()
                result = response.json()
                if result['success']:
                    return result['data']
                else:
                    return None
            except (requests.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED+Style.BRIGHT}HTTP ERROR{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None

    def save_token(self, id, token):
        tokens = json.loads(open("tokens.json").read())
        tokens[str(id)] = token
        open("tokens.json", "w").write(json.dumps(tokens, indent=4))

    def get_token(self, id):
        tokens = json.loads(open("tokens.json").read())
        if str(id) not in tokens.keys():
            return None

        return tokens[str(id)]

    def is_expired(self, token):
        header, payload, sign = token.split(".")
        deload = urlsafe_b64decode(payload + "==").decode()
        jeload = json.loads(deload)
        now = int(datetime.now().timestamp())
        if now > jeload["exp"]:
            return True
        return False

    def process_query(self, query: str, wallet: str, id):

        token = self.get_token(id)
        if token is None:
            token = self.user_auth(query)
            if token is None:
                return
            self.save_token(id, token)

        if self.is_expired(token):
            token = self.user_auth(query)
            if token is None:
                return
            self.save_token(id, token)
        
        if token:
            user = self.user_data(token)
            if user:
                self.log(
                    f"{Fore.MAGENTA+Style.BRIGHT}[ Account{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {user['userData']['firstname']} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}] [ Balance{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {user['gameData']['balance']} $PAWS {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                )
                account_delay = config['account_delay']
                countdown_timer(random.randint(min(account_delay), max(account_delay)))

                if wallet:
                    self.connect_wallet(token, wallet)
                    countdown_timer(random.randint(min(account_delay), max(account_delay)))

                quests = self.quest_lists(token)
                if quests:
                    for quest in quests:
                        quest_id = quest['_id']
                        rewards = quest.get('rewards', [])
                        amount = rewards[0]['amount'] if rewards and 'amount' in rewards[0] else None

                        current_progress = quest['progress']['current']
                        total_progress = quest['progress']['total']
                        claimed = quest['progress']['claimed']

                        if quest and not claimed:
                            
                            if current_progress != total_progress:
                                start = self.start_quests(token, quest_id)
                                if start:
                                    self.log(
                                        f"{Fore.MAGENTA+Style.BRIGHT}[ Quest{Style.RESET_ALL}"
                                        f"{Fore.WHITE+Style.BRIGHT} {quest['title']} {Style.RESET_ALL}"
                                        f"{Fore.GREEN+Style.BRIGHT}Is Started{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                                    )
                                    countdown_timer(random.randint(min(account_delay), max(account_delay)))

                                    claim = self.claim_quests(token, quest_id)
                                    if claim:
                                        self.log(
                                            f"{Fore.MAGENTA+Style.BRIGHT}[ Quest{Style.RESET_ALL}"
                                            f"{Fore.WHITE+Style.BRIGHT} {quest['title']} {Style.RESET_ALL}"
                                            f"{Fore.GREEN+Style.BRIGHT}Is Claimed{Style.RESET_ALL}"
                                            f"{Fore.MAGENTA+Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                            f"{Fore.WHITE+Style.BRIGHT} {amount} $PAWS {Style.RESET_ALL}"
                                            f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                                        )
                                    else:
                                        self.log(
                                            f"{Fore.MAGENTA+Style.BRIGHT}[ Quest{Style.RESET_ALL}"
                                            f"{Fore.WHITE+Style.BRIGHT} {quest['title']} {Style.RESET_ALL}"
                                            f"{Fore.RED+Style.BRIGHT}Isn't Claimed{Style.RESET_ALL}"
                                            f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                                        )
                                else:
                                    self.log(
                                        f"{Fore.MAGENTA+Style.BRIGHT}[ Quest{Style.RESET_ALL}"
                                        f"{Fore.WHITE+Style.BRIGHT} {quest['title']} {Style.RESET_ALL}"
                                        f"{Fore.RED+Style.BRIGHT}Isn't Started{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                                    )

                            else:
                                claim = self.claim_quests(token, quest_id)
                                if claim:
                                    self.log(
                                        f"{Fore.MAGENTA+Style.BRIGHT}[ Quest{Style.RESET_ALL}"
                                        f"{Fore.WHITE+Style.BRIGHT} {quest['title']} {Style.RESET_ALL}"
                                        f"{Fore.GREEN+Style.BRIGHT}Is Claimed{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                        f"{Fore.WHITE+Style.BRIGHT} {amount} $PAWS {Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                                    )
                                else:
                                    self.log(
                                        f"{Fore.MAGENTA+Style.BRIGHT}[ Quest{Style.RESET_ALL}"
                                        f"{Fore.WHITE+Style.BRIGHT} {quest['title']} {Style.RESET_ALL}"
                                        f"{Fore.RED+Style.BRIGHT}Isn't Claimed{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                                    )
                else:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Quest{Style.RESET_ALL}"
                        f"{Fore.RED+Style.BRIGHT} Is None {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    )
            else:
                self.log(
                    f"{Fore.MAGENTA+Style.BRIGHT}[ Account{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Is None {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                )
                
    def main(self):
        try:
            with open('query.txt', 'r') as file:
                queries = [line.strip() for line in file if line.strip()]
            with open('proxies.txt', 'r') as file:
                proxies = [line.strip() for line in file if line.strip()]
            with open('wallets.txt', 'r') as file:
                wallets = [line.strip() for line in file if line.strip()]


            while True:
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(queries)}{Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Proxy's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(proxies)}{Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Wallets's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(wallets)}{Style.RESET_ALL}"
                )
                self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)

                for i, query in enumerate(queries):
                    query = query.strip()
                    if query:
                        self.log(
                            f"{Fore.GREEN + Style.BRIGHT}Account: {Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT}{i + 1} / {len(queries)}{Style.RESET_ALL}"
                        )
                        if len(proxies) >= len(queries):
                            proxy = self.set_proxy(proxies[i])  # Set proxy for each account
                            self.log(
                                f"{Fore.GREEN + Style.BRIGHT}Use proxy: {Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT}{proxy}{Style.RESET_ALL}"
                            )

                        else:
                            self.log(Fore.RED + "Number of proxies is less than the number of accounts. Proxies are not used!")


                        if config['connect_wallets']:
                            if len(wallets) >= len(queries):
                                wallet = wallets[i]
                                self.log(
                                    f"{Fore.GREEN + Style.BRIGHT}Connect wallet:{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT}{wallet}{Style.RESET_ALL}"
                                )

                            else:
                                self.log(Fore.RED + "The number of wallets is less than the number of accounts. The connection of wallets is disabled!")
                                wallet = None
                        else:
                            wallet = None

                        user_info = extract_user_data(query)
                        user_id = str(user_info.get('id'))
                        self.headers = get_headers(user_id)

                        try:
                            self.process_query(query, wallet, user_id)
                        except Exception as e:
                            self.log(f"{Fore.RED + Style.BRIGHT}An error process_query: {e}{Style.RESET_ALL}")

                        self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)
                        account_delay = config['account_delay']
                        countdown_timer(random.randint(min(account_delay), max(account_delay)))

                cycle_delay = config['cycle_delay']
                countdown_timer(random.randint(min(cycle_delay), max(cycle_delay)))

        except KeyboardInterrupt:
            self.log(f"{Fore.RED + Style.BRIGHT}[ EXIT ] PAWS - BOT{Style.RESET_ALL}")
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}An error occurred: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    bot = PAWS()
    bot.clear_terminal()
    bot.welcome()
    bot.main()