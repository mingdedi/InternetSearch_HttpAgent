from flask import Flask, request, jsonify, Response
import time
import json
import requests
from WebSearch_api_test import WebSearch
app = Flask(__name__)

def QueryHandle(query):
    query_handle=f"根据参考资料回答问题，并使用脚注格式引用数据来源。请忽略无关的参考资料。\n\n## 脚注格式：\n\n1. **脚注标记**：在正文中使用 [^数字] 的形式标记脚注，例如 [^1]。\n2. **脚注内容**：在文档末尾使用 [^数字]: 脚注内容 的形式定义脚注的具体内容\n3. **脚注内容**：应该尽量简洁\n## 我的问题是：{query}\n\n## 参考资料：\n\n"
    query_handle=query_handle+WebSearch(query,txt_count=10)
    return query_handle

@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    # 解析请求数据（可根据需要处理参数）
    auth_header = request.headers.get("Authorization")
    request_data = request.json#格式为字典
    stream = request_data.get("stream", False)
    # print(request_data["messages"][-1]["content"])
    request_data["messages"][-1]["content"]=QueryHandle(request_data["messages"][-1]["content"])
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': f'{auth_header}'
    }
    base_url="https://api.siliconflow.cn/v1/chat/completions"
    #base_url不会自动进行获取，其余的密钥和模型id都会自动进行获取
    # 构建符合OpenAI API规范的响应
    if stream:
        def generate_stream():
            # 发起流式请求
            with requests.post(
                base_url,
                headers=headers,
                json=request_data,
                stream=True
            ) as response:
                # 转发流式数据
                for chunk in response.iter_lines():
                    # 过滤保持连接的心跳信息
                    if chunk:
                        decoded_chunk = chunk.decode('utf-8')
                        
                        # 直接透传deepseek的原始数据
                        if decoded_chunk.startswith('data: '):
                            yield decoded_chunk + '\n\n'
                            
                        # 结束标记处理
                        if decoded_chunk == 'data: [DONE]':
                            yield 'data: [DONE]\n\n'
        return Response(generate_stream(), mimetype='text/event-stream')
    else:
        #请求中的信息进行信息补充，如同知识库的使用那样
        response = requests.post(base_url, headers=headers, json=request_data)
        return jsonify(response.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    #print(QueryHandle("2024年2月8日，北京市天气如何？"))