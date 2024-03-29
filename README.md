# 社区可回收资源分类辅助及回收管理平台

## 一、项目说明

本课题开发了一个社区可回收资源分类辅助及回收管理平台。

该平台不仅能够实现资源分类“智能化、精确化、便捷化”和回收过程的“程序化、 可控化、可视化”，还通过实时监控可回收资源的生产情况，利用可视化信息化 管理、大数据分析，构建智能服务体系。在提高可回收资源的识别率、回收率及 利用率的同时为政府决策提供有力支持。 

**系统面向的用户分为三类**：系统管理员、回收人员、小区住户。

**主要功能包括**：垃圾查询、智能识别、分类排行、知识问答、呼叫上门、预约查询、积分商 城、购物车、社区数据可视化等。

## 二、功能结构

### 2.1 社区用户

<img src="https://s2.loli.net/2024/03/03/GHT5ySXm6DYhzef.png" alt="image.png" style="zoom: 67%;" />

### 2.2 系统管理员

<img src="https://s2.loli.net/2024/03/03/wxR1oGvlXBnfsVh.png" alt="image.png" style="zoom: 67%;" />

### 2.3 社区回收员

<img src="https://s2.loli.net/2024/03/03/pgNw8h6leWMnHrU.png" alt="image.png" style="zoom:67%;" />

## 三、关键技术 

### 3.1 数据可视化 

1. 数据的收集及缓存策略

   用户使用垃圾查询和拍照识别功能时，系统会记录用户的本次行为，包括垃圾名称、垃圾类别、用户所在社区、时间。系统将本次记录发送到可视化服务提供者，可视化服务器提供者将根据请求的类型决定数据的处理方式。

   为了降低服务器的负载压力，系统将可视化图例保存到 Redis 中，而缓存的有效时间设为一个小时。每当前端请求可视化数据时，系统先判断缓存的状态， 如果缓存过期，将重新请求可视化服务提供者获取最新的可视化图例，并且图例 保存到缓存中。如果缓存未过期，系统将会直接从缓存中获取图例数据返回给前端。 

   **数据收集和缓存策略的实现流程**

<img src="https://s2.loli.net/2024/03/03/jWFrf34zI6YeZRC.png" alt="image-20240303085800638.png" style="zoom:80%;" />

**可视化服务提供者执行流程**

<img src="https://s2.loli.net/2024/03/03/HTc3FZugyGJeMVS.png" alt="image.png" style="zoom:80%;" />

### 3.2 Shiro Redis JWT完成用户认证与授权

#### 3.2.1 登录验证与授权

说明：由于前端采用微信小程序开发，用户的登录过程由微信官方处理，因此，本项目无需再设置账号密码系统，但是需要进行登录验证和操作授权处理。（登录验证是检测用户是否授权本系统使用微信账号，操作授权是检测用户登录后，是否具有某些操作或查看某些页面的权限。）

技术栈：Springboot、Shiro、Redis、Mybatis、JWT

- 用户登录时（即启动小程序时）进行身份认证，之后每次请求数据时，进行授权。

  身份认证只在用户进入小程序和缓存过期时进行。

  授权会在除身份认证外的每一次请求中都会进行。

- 身份认证流程
  - 对所有用户请求进行拦截。
  - 通过请求中包含的openid，查询数据库。
  - 不存在时：说明此用户是一个新用户，调用注册模块接口，进行注册。完成后，缓存角色和相关数据。
  - 存在时：直接缓存数据库返回的角色类型和相关数据。
- 授权流程：
  - 用户发出请求，后台根据请求类型拦截；
  - 解析请求头携带的数据，获取缓存块id（sessionid）；
  - 根据sessionid，获取其中的数据（此数据时在身份认证时存入的），进而进行授权。

#### 3.2.2 缓存流程

缓存是在用户打开小程序（即身份认证）时创建的，在打开小程序后，前端发送login登录请求，后端从数据库中查询，并在redis中建立缓存块。

技术栈：Redis、Mybatis、JWT

- 身份认证时，会将用户的微信账号作为缓存块id，缓存块中存放用户账号、openid、id、角色、缓存块创建时间、有效时长。
- token：一串加密的字符串。保存有：用户账号、token生成时间、有效时长。
- 缓存内容获取流程：
  - 每次用户请求数据时，都要携带token；
  - 后台解密token，获取用户账户、token生产时间和有效时长；
  - 先判断token是否过期。若过期，重新调用登录验证接口，重新进行身份认证；若未过期，则利用token中的账号，找到服务端存储的缓存块，获取缓存块内容。

**身份认证、注册、缓存机制**

<img src="https://s2.loli.net/2024/03/03/i8l4HIg3q9AJjnM.png" alt="image-20240303084134898.png" style="zoom: 80%;" />

## 四、页面展示

![image.png](https://s2.loli.net/2024/03/03/GftPWnKoQ8cAS9s.png)

![image.png](https://s2.loli.net/2024/03/03/x2y8LepM4713szw.png)

![image.png](https://s2.loli.net/2024/03/03/hox9C2Jic5IeupM.png)

![image.png](https://s2.loli.net/2024/03/03/dk1Pqo4A69MxICs.png)

![pAd8sUanIqewuXQ.png](https://s2.loli.net/2024/03/03/RgLJKUVh5Qd9AiD.png)

![image.png](https://s2.loli.net/2024/03/03/YMZyAjshG8adt3X.png)

## 更多详细信息，请看项目文档。
