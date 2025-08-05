import re
import requests
from typing import Optional, Dict
from config.private_config import XHS_COOKIES

class XiaohongshuParser:
    @staticmethod
    def parse(url: str) -> Optional[Dict]:
        """解析小红书笔记（自动处理登录）"""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        try:
            res = requests.get(
                url,
                cookies=XHS_COOKIES,
                headers=headers,
                timeout=10
            )
            
            if "login" in res.url:
                raise ValueError("小红书Cookie已失效，请更新配置")
                
            # 示例解析逻辑（实际需根据页面结构调整）
            title = re.search(r'<title>(.*?)</title>', res.text).group(1)
            content = re.search(r'"desc":"(.*?)"', res.text).group(1)
            
            return {
                "platform": "小红书",
                "title": title.replace(" - 小红书", ""),
                "content": content,
                "url": url
            }
        except Exception as e:
            print(f"❌ 小红书解析失败: {str(e)[:50]}...")
            return None