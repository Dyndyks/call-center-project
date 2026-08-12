from gigachat import GigaChatAsyncClient
from gigachat.models import Chat

from token_ai import GigaToken

import os
from dotenv import load_dotenv

#этот промт как пример, надо подумать над ним
prompt = "Ты клиент, тебе звонят с целью продажи, отвечай как хочешь, но не используя знаки препинания"

load_dotenv()
giga_tk = GigaToken(os.environ.get("CLIENT_ID"), os.environ.get("CLIENT_SECRET"))
history = [{"role": "system", "content": prompt}]
    

async def get_otvet(text):
    """
    реальзовать json для сохранения диалога пока он не завершился, 
    обдумать об реализации ответов из бд, чтобы меньше использовать ии/возможно развернуть ии на пк(обудмать)
    также обрезать до 128000 токенов чтобы ии помннила и если много сообщений в себе хранит прощается
    также из самого юнити клиента получать именно: что надо/процент и само сообщение
    """
    token = await giga_tk.get_tk()
    async with GigaChatAsyncClient(
        base_url="https://api.giga.chat/v1",
        model="GigaChat-2",
        access_token=token,
        scope="GIGACHAT_API_PERS",
    ) as giga:
        
        history.append({"role": "user", "content": text})
        
        messages = Chat(messages=history)

        response = await giga.achat(messages)
        history.append({"role": "assistant", "content": response.choices[0].message.content})
        
        return response.choices[0].message.content