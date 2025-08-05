import re
from typing import Dict, Any
from WeChatPYAPI import WeChatPYApi
from .notion_client import NotionHelper
from .parsers import xiaohongshu, weixin

class WeChatProcessor:
    def __init__(self):
        self.wx = WeChatPYApi()
        self.notion = NotionHelper()
    
    def process_recent_messages(self, count: int = 20):
        """处理最近N条微信消息"""
        msgs = self.wx.get_chat_history("文件传输助手", count=count)
        url_pattern = re.compile(r'https?://[^\s]+')
        
        for msg in msgs:
            if msg.get("msg_type") == 49:  # 链接消息
                self._process_url_message(msg["content"], url_pattern)

    def _process_url_message(self, content: str, pattern: re.Pattern):
        """处理含URL的消息"""
        urls = pattern.findall(content)
        for url in filter(lambda x: len(x) > 20, urls):  # 过滤短链接
            data = None
            
            if "xiaohongshu.com" in url:
                data = xiaohongshu.XiaohongshuParser.parse(url)
            elif "mp.weixin.qq.com" in url:
                data = weixin.WeixinParser.parse(url)
            
            if data:
                self._save_to_notion(data)

    def _save_to_notion(self, data: Dict[str, Any]):
        """格式化保存到Notion"""
        properties = {
            "标题": {"title": [{"text": {"content": data["title"]}}]},
            "来源": {"select": {"name": data["platform"]}},
            "链接": {"url": data["url"]},
            "内容": {"rich_text": [{"text": {"content": data["content"]}}]}
        }
        if self.notion.create_page(properties):
            print(f"✅ 已保存: {data['title']}")