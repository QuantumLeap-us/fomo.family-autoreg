import requests
import random
import string
import json
from fake_useragent import UserAgent
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import urllib3
import warnings

# Disable warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings('ignore')

def generate_random_email():
    """Generate a random email address"""
    letters = string.ascii_lowercase
    username = ''.join(random.choice(letters) for i in range(8))
    return f"{username}@gmail.com"

def generate_heartbeat_uuid():
    """Generate a random UUID"""
    return ''.join(random.choice(string.hexdigits) for _ in range(32))

def check_referral(session, email, proxy, headers):
    """Check referral status"""
    try:
        response = session.get(
            f"https://api.getwaitlist.com/api/v1/waiter?email={email}&waitlist_id=24484",
            headers={
                **headers,
                "accept": "*/*",
                "sec-gpc": "1",
                "referer": "https://fomo.family/"
            },
            proxies=proxy,
            verify=False,
            timeout=30
        )
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        print(f"Query failed: {str(e)}")
        return None

def register_with_proxy(proxy, referral_code, max_retries=3):
    session = requests.Session()
    retry_strategy = Retry(
        total=max_retries,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    proxies = {
        "http": proxy,
        "https": proxy
    }
    
    headers = {
        "accept": "*/*",  # 修改为通用接受类型
        "accept-language": "zh-CN,zh;q=0.9",
        "content-type": "application/json",
        "origin": "https://fomo.family",
        "referer": "https://fomo.family/",
        "priority": "u=1, i",
        "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site"
    }
    
    email = generate_random_email()
    
    try:
        print(f"📧 {email}")
        
        # 1. 发送心跳请求获取 uuid
        heartbeat_data = {
            "location": f"https://fomo.family/waitlist?ref_id={referral_code}",
            "waitlist_id": "24484",
            "referrer": "",
            "widget_type": "WIDGET_1",
            "referral_token": referral_code
        }
        
        heartbeat_response = session.post(
            "https://api.getwaitlist.com/api/v1/widget_heartbeats",
            headers={
                **headers,
                "accept": "*/*",
                "sec-fetch-site": "cross-site",
                "referer": f"https://fomo.family/waitlist?ref_id={referral_code}"
            },
            json=heartbeat_data,
            proxies=proxies,
            verify=False,
            timeout=30
        )
        
        if heartbeat_response.status_code != 200:
            print(f"❌ 心跳请求失败: {heartbeat_response.status_code}")
            return {
                "error": "心跳请求失败",
                "status_code": heartbeat_response.status_code
            }
            
        try:
            heartbeat_data = heartbeat_response.json()
            heartbeat_uuid = heartbeat_data.get("uuid")
        except json.JSONDecodeError:
            print("❌ 心跳响应格式错误")
            return {"error": "心跳响应格式错误"}
            
        if not heartbeat_uuid:
            print("❌ 未获取到 uuid")
            return {"error": "未获取到 uuid"}
        
        time.sleep(random.uniform(1, 2))
        
        # 2. 获取等待列表信息
        waitlist_response = session.get(
            "https://api.getwaitlist.com/api/v1/waitlist/24484",
            headers=headers,
            proxies=proxies,
            verify=False,
            timeout=30
        )
        
        time.sleep(random.uniform(1, 2))
        
        # 3. 发送注册请求
        data = {
            "waitlist_id": 24484,
            "referral_link": f"https://fomo.family/waitlist?ref_id={referral_code}",
            "heartbeat_uuid": heartbeat_uuid,
            "widget_type": "WIDGET_1",
            "email": email,
            "answers": [{
                "question_value": "What is your X/Twitter username? (optional)",
                "answer_value": ""
            }]
        }
        
        headers["accept"] = "application/json"
        
        response = session.post(
            "https://api.getwaitlist.com/api/v1/waiter",
            headers=headers,
            json=data,
            proxies=proxies,
            timeout=30,
            verify=False
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 成功 | 排名: {result.get('priority')}")
            return result
        else:
            print(f"❌ 失败: HTTP {response.status_code}")
            return {
                "error": f"请求失败: HTTP {response.status_code}",
                "email": email
            }
            
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        return {"error": str(e), "email": email}
    finally:
        session.close()

def read_proxies(filename):
    """从文本文件读取代理列表"""
    try:
        with open(filename, 'r') as f:
            return [line.strip() for line in f if line.strip() and not line.strip().startswith('//')]
    except FileNotFoundError:
        print(f"错误: 找不到文件 {filename}")
        return []
    except Exception as e:
        print(f"读取代理文件时出错: {str(e)}")
        return []

def main():
    proxies = read_proxies('proxies.txt')
    if not proxies:
        print("没有找到可用的代理")
        return
    
    referral_code = "DSNDSJ97Q"
    success_count = 0
    fail_count = 0
    
    print(f"\n🚀 开始注册")
    print(f"📎 邀请码: {referral_code}")
    print(f"🌐 代理数: {len(proxies)}\n")
    
    while True:
        try:
            for proxy in proxies:
                result = register_with_proxy(proxy, referral_code)
                
                if result and not result.get('error'):
                    success_count += 1
                else:
                    fail_count += 1
                    
                total = success_count + fail_count
                success_rate = (success_count/total*100) if total > 0 else 0
                
                print(f"📊 {success_count}/{total} ({success_rate:.1f}%)")
                
                delay = random.uniform(3, 7)
                time.sleep(delay)
                
        except KeyboardInterrupt:
            print("\n🛑 已停止")
            total = success_count + fail_count
            success_rate = (success_count/total*100) if total > 0 else 0
            print(f"📊 总计: {success_count}/{total} ({success_rate:.1f}%)")
            break
        except Exception as e:
            print(f"❌ 错误: {str(e)}")
            time.sleep(5)

if __name__ == "__main__":
    main() 