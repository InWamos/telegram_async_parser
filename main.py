from pyrogram import Client
import asyncio, json

class Parser:

    def __init__(self) -> None:

        with open('config.json', 'r') as config_file:
            self.config_data = json.loads(config_file.read())

    async def parse(self, chat_id):
        self.chat_id = chat_id
        self.usernames = []

        async with Client("my_account", self.config_data["api_id"], self.config_data["api_hash"]) as app:
            
            async for message in app.get_chat_history(self.chat_id):

                try:
                    if message.from_user.username in self.usernames or message.from_user.username == None: continue
                    else:

                        with open('text.txt', 'a', encoding='utf-8') as text_file:
                            text_file.write(f'@{message.from_user.username}\n')

                        self.usernames.append(message.from_user.username)

                except:
                    pass
    
    async def get_chats(self):
        self.chats_obj = {}
        self.counter = 1

        async with Client("my_account", self.config_data["api_id"], self.config_data["api_hash"]) as app:

            print("Parse usernames among ", await app.search_global_count(), " messages")

            async for dialog in app.get_dialogs():

                try:
                    if str(dialog.chat.type) == "ChatType.SUPERGROUP" or str(dialog.chat.type) == "ChatType.GROUP":
                        self.chats_obj[str(self.counter)] = {}
                        self.chats_obj[str(self.counter)]["id"] = dialog.chat.id
                        self.chats_obj[str(self.counter)]["chat_type"] = dialog.chat.type
                        
                        print(f'|\n| - [{self.counter}] {dialog.chat.title} ({dialog.chat.id})\n|')
                        self.counter += 1
                except:
                    raise Exception

            self.target_chat_number = input("Enter the target number: ")
            print(self.chats_obj[self.target_chat_number]["id"], self.chats_obj[self.target_chat_number]["chat_type"])

def main():
    parser = Parser()
    asyncio.run(parser.get_chats())
    asyncio.run(parser.parse(parser.chats_obj[parser.target_chat_number]["id"]))

if __name__ == "__main__":
    main()

