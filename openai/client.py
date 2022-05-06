from email import header
import aiohttp
from enum import Enum

class Engine(Enum):
    """
    Engine names
    """

    # openAI models
    Davinci = "text-davinci-001"
    Curie = "text-curie-001"
    Babbage = "text-babbage-001"
    Ada = "text-ada-001"

    # gooseAI models
    Neo = "gpt-neo-20b"
    Fairseq125m = "fairseq-125m"
    Fairseq13b = "fairseq-1-3b"
    GPTJ = "gpt-j-6b"


class Client:
    """
    an async client class for the OpenAI API
    """

    def __init__(self, token: str, base: str = "https://api.openai.com", version: int = 1, default_engine: Engine = Engine.Davinci) -> None:
        self.base = base
        self.version = version
        self.token = token
        self.default_engine = default_engine

    async def request(self, method: str, path: str, data: dict = None) -> dict:
        async with aiohttp.ClientSession(headers={'Authorization': f"Bearer {self.token}"}) as session:
            async with session.request(method, f"{self.base}/v{self.version}{path}", json=data) as resp:
                return await resp.json()

    async def complete(
        self, 
        prompt: str,
        engine: Engine = None, 
        max_tokens: int = 1000,
        temperature: float = 1,
        top_p: float = 1,
        n: int = 1,
        stream: bool = False,
        stop: str | list = None,
        presence_penalty: float = 0.0,
        frequency_penalty: float = 0.0,
        full_response: bool = False,
    ) -> str:

        if engine is None:
            engine = self.default_engine

        try:
            data = await self.request("POST", "/engines/{}/completions".format(engine.value), {
                "prompt": prompt,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": top_p,
                "n": n,
                "stream": stream,
                "stop": stop,
                "presence_penalty": presence_penalty,
                "frequency_penalty": frequency_penalty,
            })

            print(data)

            if full_response:
                return data

            choices = data.get("choices", [])
            return choices[0].get("text", "")
        except Exception as e:
            print(e)
            return "Alright it's time for me to go i think..."
