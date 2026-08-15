from gigachat import GigaChatAsyncClient
from gigachat.models import Chat

from classes_ai import GigaToken, DialogManager

from config import CLIENT_ID, CLIENT_SECRET



giga_tk = GigaToken(CLIENT_ID, CLIENT_SECRET)
chat = DialogManager()
    

async def get_otvet(text):
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
        
        await chat.add_history("user", text)
        
        messages = Chat(messages=await chat.get_history())

        response = await giga.achat(messages)

        await chat.add_history("assistant", response.choices[0].message.content)

        return response.choices[0].message.content