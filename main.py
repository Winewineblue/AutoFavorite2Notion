import sys
from src.wechat_processor import WeChatProcessor

def main():
    processor = WeChatProcessor()
    
    # 微信登录
    if not processor.wx.start_wx():
        print("❌ 微信初始化失败")
        sys.exit(1)
    
    processor.wx.wait_login()
    
    # 命令行交互
    while True:
        cmd = input("\n请输入命令: [scan/exit] ").strip().lower()
        if cmd == "scan":
            print("🔄 正在扫描微信消息...")
            processor.process_recent_messages()
        elif cmd == "exit":
            processor.wx.stop_wx()
            break

if __name__ == "__main__":
    main()