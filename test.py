# BoCha AI Search Python SDK
import requests, json
from typing import Iterator

# 读取密钥文件
#为了防止密钥泄露直接将密钥放到SEARCH_API_KEY.txt文件中
with open('SEARCH_API_KEY.txt', 'r', encoding='utf-8') as file:
    SEARCH_API_KEY = file.read()


def bocha_ai_search(
    query: str,
    api_key: str,
    api_url: str = "https://api.bochaai.com/v1/ai-search",
    freshness: str = "noLimit",
    answer: bool = False,
    stream: bool = False
):
    """ 博查AI搜索 """
    data = {
        "query": query,
        "freshness": freshness,
        "answer": answer,
        "stream": stream
    }

    resp = requests.post(
        api_url,
        headers={"Authorization": f"Bearer {SEARCH_API_KEY}"},
        json=data,
        stream=stream
    )

    if stream:
        return (json.loads(line) for line in parse_response_stream(resp.iter_lines()))
    else:
        if resp.status_code == 200:
            return resp.json()
        else:
            return { "code": resp.code, "msg": "bocha ai search api error." }

def parse_response_stream(resp: Iterator[bytes]) -> Iterator[str]:
    """将stream的sse event bytes数据解析成line格式"""
    for line in resp:
        if line:
            if line.startswith(b"data:"):
                _line = line[len(b"data:"):]
                _line = _line.decode("utf-8")
            else:
                _line = line.decode("utf-8")
            yield _line
if __name__ == '__main__':
    BOCHA_API_URL = "https://api.bochaai.com/v1/ai-search"

    response = bocha_ai_search(
        api_url=BOCHA_API_URL,
        api_key=SEARCH_API_KEY,
        query="天空为什么是蓝色的",
        freshness="noLimit",
        answer=False,
        stream=False
    )

    print(response)