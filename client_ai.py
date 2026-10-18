from gigachat import GigaChatAsyncClient
from gigachat.models import Chat

from classes_ai import GigaToken, chat

from config import CLIENT_ID, CLIENT_SECRET


giga_tk = GigaToken(CLIENT_ID, CLIENT_SECRET)
    

async def get_otvet(websocket, text):
    """
    из самого юнити клиента получать именно: что надо/процент и само сообщение
    """
    token = await giga_tk.get_tk()
    async with GigaChatAsyncClient(
        base_url="https://api.giga.chat/v1",
        model="GigaChat-2",
        access_token=token,
        scope="GIGACHAT_API_PERS",
    ) as giga:
        
        await chat.add_history(websocket, "user", text)
        
        messages = Chat(messages=await chat.get_history(websocket))

        response = await giga.achat(messages)

        await chat.add_history(websocket, "assistant", response.choices[0].message.content)
        return response.choices[0].message.content