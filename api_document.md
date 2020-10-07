### Flat_Form_List (```/flat_form_list```)

##### Request

- method
>- GET

##### Response
```json
{
    "code": 200,
    "message": [
        "naver",
        "daum"
    ],
    "status": "OK"
}
```

---

### Category_List (```/flat_form_list/<flat_form>```)

##### Request 

- method
> - GET

- prams
> - flat_form

##### Response
```json
{
    "code": 200,
    "message": [
        "baseball",
        "wbaseball",
        "basketball",
        "general",
        "volleyball",
        "football",
        "esports",
        "golf",
        "wfootball"
    ],
    "status": "OK"
}
```

---

### News_List (```/flat_form_list/<category>```)

##### Request

- method
> - GET

- parmas
> - flat_form_list
> - category

##### Response
```json
{
    "code": 200,
    "message": {
        "1": {
            "title": "[롤드컵] TES '카사', \"우리는 가장 강한 리그의 1시드팀...우승 목표로 해야\"",
            "url": "https://sports.news.naver.com//news.nhn?oid=442&aid=0000123948"
        },
        "10": {
            "title": "LCK의 날, 서포터의 날 [롤드컵]",
            "url": "https://sports.news.naver.com//news.nhn?oid=005&aid=0001367420"
        },
        "2": {
            "title": "英 축구스타 베컴의 e스포츠 팀, 런던 증시 상장… 620억 원 규모",
            "url": "https://sports.news.naver.com//news.nhn?oid=109&aid=0004283941"
        },
        "3": {
            "title": "[오늘의 롤드컵 10.3] 담원 앞에선 처신 잘하라고….",
            "url": "https://sports.news.naver.com//news.nhn?oid=502&aid=0000000412"
        },
        "4": {
            "title": "[Oh!쎈 LOL] 말파이트로 탑 약세 버틴 로그, ‘너구리’ 앞에선?",
            "url": "https://sports.news.naver.com//news.nhn?oid=109&aid=0004283922"
        },
        "5": {
            "title": "[롤드컵] LGD 게이밍 '피넛', \"젠지와 대결, 한타 조금만 잘했더라면...\"",
            "url": "https://sports.news.naver.com//news.nhn?oid=442&aid=0000123949"
        },
        "6": {
            "title": "'베릴' 조건희 \"징동의 예측불허 움직임, 매서웠지만 우리가 더 잘했어\" [일문일답]",
            "url": "https://sports.news.naver.com//news.nhn?oid=311&aid=0001208239"
        },
        "7": {
            "title": "[포모스 롤드컵 영상] '클리드' 김태민, \"해야할 플레이 못한 건 아쉽다\"",
            "url": "https://sports.news.naver.com//news.nhn?oid=236&aid=0000206966"
        },
        "8": {
            "title": "'클리드' 김태민 \"중이염 걸린 '룰러', 아픈데도 잘해줘서 대견해\" [일문일답]",
            "url": "https://sports.news.naver.com//news.nhn?oid=311&aid=0001208298"
        },
        "9": {
            "title": "롤드컵 16강 첫 경기부터 시청자 '폭증'",
            "url": "https://sports.news.naver.com//news.nhn?oid=347&aid=0000147512"
        }
    },
    "status": "OK"
}
```
