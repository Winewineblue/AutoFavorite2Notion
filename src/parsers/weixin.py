import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict

class WeixinParser:
    @staticmethod
    def parse(url: str) -> Optional[Dict]:
        """解析公众号文章（带反爬处理）"""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://mp.weixin.qq.com/"
        }
        
        try:
            res = requests.get(url, headers=headers, timeout=10)
            if "验证码" in res.text:
                raise ValueError("公众号触发验证码，请手动访问")
                
            soup = BeautifulSoup(res.text, 'html.parser')
            title = soup.find('meta', property='og:title')['content']
            content = soup.find('meta', property='og:description')['content']
            
            return {
                "platform": "微信公众号",
                "title": title,
                "content": content[:2000],  # Notion字段限制
                "url": url
            }
        except Exception as e:
            print(f"❌ 公众号解析失败: {str(e)[:50]}...")
            return None