import os
import time
import random
import requests
import subprocess
from threading import Thread

STREAM_URL = "https://www.twitch.tv/denievalollipop"
TOTAL_BOTS = 5

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15"
]

def fetch_proxies():
    print("[Система] Сбор SOCKS5 прокси из расширенного списка репозиториев...")
    urls = [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=5000",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
        "https://raw.githubusercontent.com/Hookzof/socks5_list/master/proxy.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
        "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt",
        "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt"
    ]
    
    unique_proxies = set()
    for url in urls:
        try:
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                for line in res.text.splitlines():
                    if line.strip() and ":" in line:
                        unique_proxies.add(line.strip())
        except:
            continue
            
    proxies = list(unique_proxies)
    random.shuffle(proxies)
    print(f"[Система] Собрано {len(proxies)} уникальных SOCKS5 адресов.")
    return proxies

def run_bot(bot_id, proxy_list):
    print(f"=== Бот №{bot_id} инициализирован ===")
    for proxy in proxy_list:
        proxy = proxy.strip()
        user_agent = random.choice(USER_AGENTS)
        try:
            proxies_dict = {"http": f"socks5://{proxy}", "https": f"socks5://{proxy}"}
            requests.get("https://www.twitch.tv", proxies=proxies_dict, headers={"User-Agent": user_agent}, timeout=2)
        except:
            continue
            
        print(f"[Бот №{bot_id}] 🟢 РАБОТАЕТ через SOCKS5: {proxy}")
        cmd = [
            "streamlink", 
            "--http-proxy", f"socks5://{proxy}", 
            "--http-header", f"User-Agent={user_agent}",
            "--loglevel", "info", 
            STREAM_URL, 
            "audio_only,worst"
        ]
        process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        process.wait()
        print(f"[Бот №{bot_id}] 🔴 Отключение прокси {proxy}")
        time.sleep(2)

def main():
    proxies = fetch_proxies()
    if not proxies:
        print("[Ошибка] Список прокси пуст.")
        return
    threads = []
    for i in range(1, TOTAL_BOTS + 1):
        t = Thread(target=run_bot, args=(i, proxies.copy()))
        threads.append(t)
        t.start()
        time.sleep(0.4)
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
