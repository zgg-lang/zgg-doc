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
### <div id="postJson">func postJson(url, jsonValue, headers?)</div>
### <div id="Request">type Request</div>