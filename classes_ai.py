import httpx
import uuid
import base64
import time


class GigaToken():

    def __init__(self, client_id, client_secret):
        self.start_mono = 0
        self.token = None
        self.client_id = client_id
        self.client_secret = client_secret

    async def get_tk(self):

        auth_string = f"{self.client_id}:{self.client_secret}"
        auth_bytes = auth_string.encode("utf-8")
        basic_auth = base64.b64encode(auth_bytes).decode("utf-8")
        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': str(uuid.uuid4()),
            'Authorization': f"Basic {basic_auth}"
            }
        data = "scope=GIGACHAT_API_PERS"

        if self.token is None or int(time.monotonic() - self.start_mono) // 60 >= 25:
            async with httpx.AsyncClient(verify="certs/chain.pem") as client:
                    try:
                        resp = await client.post(url, headers=headers, data=data)
                        resp.raise_for_status()
                        self.token = resp.json()["access_token"]
                        self.mono = time.monotonic()
                    except httpx.HTTPStatusError as e:
                        print(f"статус: {e.response.status_code}\nтекст{e.response.text}")
                    except httpx.ConnectError as e:
                        print("проблема с подключением")
        return self.token


class DialogManager():
    PROMPT = "Ты клиент, тебе звонят с целью продажи, отвечай как хочешь, но не используя знаки препинания"

    def __init__(self):
        self.history = [{"role": "system", "content": self.PROMPT}]


    async def add_history(self, role, content):
        self.history.append({"role": role, "content": content})


    async def clear_history(self):
        self.history = [{"role": "system", "content": self.PROMPT}]


    async def get_history(self):
        return self.history