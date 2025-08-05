from notion_client import Client
from config.private_config import NOTION

class NotionHelper:
    def __init__(self):
        self.client = Client(auth=NOTION["api_key"])
    
    def create_page(self, properties: dict) -> bool:
        """安全写入Notion"""
        try:
            self.client.pages.create(
                parent={"database_id": NOTION["database_id"]},
                properties=properties
            )
            return True
        except Exception as e:
            print(f"❗ Notion写入失败: {str(e)[:100]}...")  # 截断错误信息避免泄露敏感数据
            return False