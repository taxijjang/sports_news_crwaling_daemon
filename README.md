# sports_news_crwaling_daemon



### 목적

- 인터넷 스포츠 뉴스를 많이보는데 뉴스를 보기 위해 매번 브라우저를 통하는 번거러움을 해소 하기 위함

### 개요

- 네이버, 다음의 카테고리별 인기 있는 스포츠 뉴스를 크롤링

- 일정 시간마다 크롤링을 하여 뉴스를 최신화 하기 위하여 daemon을 이용

### 구성요소

- 클라이언트 ( 웹 or 안드로이드)

- 서버 (flask, daemon, redis)

### 작동 원리

- daemon을 통하여 일정시간 마다 스포츠 뉴스를 크롤링 한다.
- 크롤링한 뉴스를 redis에  key {플랫폼:카테고리} : value {뉴스 제목 : 뉴스 링크}로 저장
- flask를 이용하여 redis에 저장되어 있는 데이터를 rest api를 통하여 클라이언트에게 제공

### Redis를 선정한 이유

- 추후 업데이트 예쩡

# 결과


### response api

- Api Url

>- hostname/(flatform)/(category)

- Response_Data

![Response Data](/image/api.PNG)


### Redis Data keys

- Redis에 저장된 key의 목록

![redis_keys](/image/redis_keys.PNG)


### Daemon 실행에 따른 pid

- Daemon 실행에 따른 pid

![daemon_pid](image/daemon_pid.PNG)

