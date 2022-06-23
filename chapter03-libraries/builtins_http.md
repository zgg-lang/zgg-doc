# ZGG内置标准库 - http

http库提供了各种常用的http功能，包括：服务端、客户端、websocket

## 作为客户端时：
* [func get](#get)
* [func getJson](#getJson)
* [func postForm](#postForm)
* [func postJson](#postJson)
* [type Request](#Request)

## 作为服务端时：
* [func createServe](#createServe)
* [func serve](#serve)
* [type RequestContext](#RequestContext)

## 函数文档

### <div id="get">func get(url, headers?)</div>
用GET方法请求指定url的资源，返回一个Bytes值

若请求失败时，抛出异常

### <div id="getJson">func getJson(url, headers?)</div>
用GET方法请求指定url的资源，并将返回内容按json格式解析为一个ZGG的值

若请求失败时，抛出异常

### <div id="postForm">func postForm(url, form, headers?)</div>

以x-www-form-urlencoded方式往指定URL发起一次Post Form请求。若请求失败则抛出异常。

#### Examples
```
zgg> @http.postForm('https://httpbin.org/post', {
....   name: 'zgg',
....   values: [1, 2, 3],
.... }, {
....   Authorization: 'Bearer HelloWorld',
.... })
{
  "args": {}, 
  "data": "", 
  "files": {}, 
  "form": {
    "name": "zgg", 
    "values": [
      "1", 
      "2", 
      "3"
    ]
  }, 
  "headers": {
    "Accept-Encoding": "gzip", 
    "Authorization": "Bearer HelloWorld", 
    "Content-Length": "35", 
    "Content-Type": "application/x-www-form-urlencoded", 
    "Host": "httpbin.org", 
    "User-Agent": "Go-http-client/2.0", 
    "X-Amzn-Trace-Id": "Root=1-62b404ea-7271f822152de246228bd973"
  }, 
  "json": null, 
  "origin": "137.59.101.43", 
  "url": "https://httpbin.org/post"
}
```

### <div id="postJson">func postJson(url, jsonValue, headers?)</div>

往指定URL发起一次Post Json请求。若请求失败则抛出异常。

#### Examples
```
zgg> @http.postJson('https://httpbin.org/post', {
....   name: 'zgg',
....   values: [1, 2, 3],
.... }, {
....   'X-My-Header': 'My Value lalala',
.... })
{
  "args": {}, 
  "data": "{\"name\":\"zgg\",\"values\":[1,2,3]}", 
  "files": {}, 
  "form": {}, 
  "headers": {
    "Accept-Encoding": "gzip", 
    "Content-Length": "31", 
    "Content-Type": "application/json", 
    "Host": "httpbin.org", 
    "User-Agent": "Go-http-client/2.0", 
    "X-Amzn-Trace-Id": "Root=1-62b40554-306f51a40a6b9ee901489c05", 
    "X-My-Header": "My Value lalala"
  }, 
  "json": {
    "name": "zgg", 
    "values": [
      1, 
      2, 
      3
    ]
  }, 
  "origin": "137.59.101.43", 
  "url": "https://httpbin.org/post"
}
```

### <div id="Request">type Request</div>

### <div id="serve">func serve(listenAddr, handleFunc)</div>

功能：启动一个web服务器，监听listenAddr地址（格式同go的http.ListenAndServe的第一个参数），并用handleFunc处理每个请求。

serve函数是一个非常简便的提供http服务的方法，适用于对外提供简单服务。
