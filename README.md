# 噗浪轉噗機器人

## 關於這個專案

這個程式會基於給定的 keyword，搜尋最近 30 筆以 keyword 作為 hashtag 的噗。概念與設計都非常簡單，也因此還有許多可以新增的功能。

## 相依套件

Python 3.8+（Python3 其餘版本尚未測試，不過應該可以）
噗浪的 oauth 登入使用：https://github.com/clsung/plurk-oauth
logging 使用：https://github.com/Delgan/loguru

若有使用 pdm，直接 `pdm install` 即可安裝相依套件。若沒有：

```bash
pip install git+https://github.com/clsung/plurk-oauth.git
pip install loguru
```

## 使用說明

1. 取得 Plurk OAuth Key，請參考：https://www.plurk.com/API/2
2. 建立 key file: https://github.com/clsung/plurk-oauth#apikeys
3. 執行程式：`python replurker.py <key-file> <keyword>`

比如說存了一個 `dummy.keys` 的 key-file，想要轉噗有 `#replurk-test` hashtag 的噗：
`python replurker.py dummy.keys replurk-test`

### 額外的參數說明：

在指令中加上 `-a` 允許轉噗匿名噗，如：`python replurker.py -a dummy.keys replurk-test`

## Todos

- 取代第三方的 plurk-oauth
  - plurk-oauth 幾乎已停止維護，接下來應該會換掉
- 新增 daemon mode
  - 目前設計依賴 crontab 才能固定一段時間跑一次，或許可以加上 daemon mode 讓程式持續執行，減少設置的複雜度
- 測試 Windows 上的執行狀況
  - 目前只有在 Linux（Gentoo and Ubuntu）上執行過，尚未在 Windows 上測試
- 歡迎各位開各種 feature request!

## FAQ

- 噗浪有 `/APP/Realtime/getUserChannel` API 以 event driven 的方式提供即時的訊息，為什麼不用？
  - 如果我理解沒有錯誤，這樣轉噗機器人就只會轉有加機器人好友/粉絲的噗，但是目前有轉噗匿名噗的需求，當初設計的概念也是不希望強制要求加機器人好友才會轉噗（雖然希望被轉的應該都會加）

- 為什麼搜尋結果只有 30 筆？
  - 目前有使用本機器人的幾個河道相關噗量都沒有那麼多，因此就沒有對搜尋 API 的預設值多做調整，或許可以加上參數來改善這段。
