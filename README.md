# InternetSearch_HttpAgent
用于代理本地http服务，进而实现联网搜索
使用Cherry Studio的时候设置地址为http://127.0.0.1:8080/v1/chat/completions
但是需要注意的是由于api使用的时候不会直接包含base_url，所以需要使用本地代理时，要指定服务商才行，这点需要注意，目前默认使用的是硅基流动的base_url
需要自行去找博查搜索api的密钥，https://open.bochaai.com/
也可以使用别的Web Search服务商的密钥，但是需要改动代码中的json文本解析方式

Cherry studio中不如直接使用MCP服务器进行
