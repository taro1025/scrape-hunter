# scrape-hunter
申し込み可能な猟銃等初心者講習があった場合にtwilioを使って電話通知をします。

監視するページは[こちら](https://www.keishicho-gto.metro.tokyo.lg.jp/keishicho-u/reserve/offerList_movePage)です。

電話番号はTwilioのWebサイト上で一つまで無料で取得でき、自分の電話に対してであれば無料で音声通話を発信することができます。

## 使い方
1. 環境変数のセット
    - TWILIO_ACCOUNT_SID: TwilioのアカウントSID
    - TWILIO_AUTH_TOKEN: Twilioの認証トークン
    - FROM_PHONE_NUMBER: Twilioの電話番号
    - TO_PHONE_NUMBER: 自分の電話番号

2. イメージのビルド
    ```bash
    make build
    ```

3. イメージの実行
    ```bash
    make run
    ```

講習は毎月9日か10日の12時ちょうどに更新される傾向にあるのでその前後に定期実行することをおすすめします。
サーバーに過度に負荷のかかるような使い方は避けてください。
