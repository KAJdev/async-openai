# async-openai
An async GPT-3 API wrapper written in python

# Installation

`pip install git+https://github.com/kajdev/async-openai`

# Usage

The wrapper is pretty simple at the moment.

```py
from os import getenv
import openai
import asyncio

client = openai.Client(getenv('token'))

async def main():
    print(await client.complete("What is the capital of Italy?"))

if __name__ == "__main__":
    asyncio.run(main())
```
