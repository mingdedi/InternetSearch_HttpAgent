import requests

# 读取密钥文件
#为了防止密钥泄露直接将密钥放到SEARCH_API_KEY.txt文件中
with open('SEARCH_API_KEY.txt', 'r', encoding='utf-8') as file:
    SEARCH_API_KEY = file.read()

def WebSearch(query,txt_count=5):

    headers = {
        "Authorization": f"Bearer {SEARCH_API_KEY}",  # 替换为你的实际 API Key
        "Content-Type": "application/json"
    }

    payload = {
        "query": f"{query}",
        "freshness": "noLimit",
        "count": txt_count,
        "answer": False,
        "stream": False
    }

    Webtxt=""

    try:
        print("开始联网搜索")
        response = requests.post(
            "https://api.bochaai.com/v1/web-search",
            headers=headers,
            json=payload
        )
        response.raise_for_status()  # 检查 HTTP 错误
        i=0
        for value in response.json()["data"]["webPages"]["value"]:
            Webtxt=Webtxt+f"参考资料id：{i}\n"+value["snippet"]+"\n"
            i+=1
         # 解析并叠加响应
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except ValueError as e:
        print(f"Failed to parse JSON response: {e}")
    return Webtxt

if __name__ == '__main__':
    print(WebSearch("今天上海的天气是？",txt_count=5))