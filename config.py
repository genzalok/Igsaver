import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
FORCE_SUB_CHANNEL = os.getenv("FORCE_SUB_CHANNEL", "YourChannelUsername")
DUMP_CHANNEL_ID = int(os.getenv("DUMP_CHANNEL_ID", "123456789"))
