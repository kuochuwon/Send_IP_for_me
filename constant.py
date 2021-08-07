

class LineConstant:
    access_tokens = {
        "7PCT_helper": "qipp53w9dsKIjaDG3D5eYswChigJUmYdgD6ilha3BCHjF4rJmG8dVjj3kMqpBy4TvTnYODobZelFc5bsSz9ycEx09y/XU3aZO42Bp2o0+9f9TRJBFMeUih6Oi2YB77ET4+u5z/miOF5FRihh5ubRTgdB04t89/1O/w1cDnyilFU=",  # noqa
        "IP_service": "V0Vq9b39WAp5bjhmNHocicMN5brm1SO3aKc8g/CdhUxzf/4ZwIL0xiSoVDeqkcGGZTWwutn7rCveQUwZvPd/lVZqRzLc4EkKeO/2iQWECvBvJ46B09IBQ4MKyVSjV9mFERXx65kAFVBg8tTcAVzScQdB04t89/1O/w1cDnyilFU="  # noqa
    }

    secret_tokens = {
        "7PCT_helper": "6fd6a21c86d311aaf115d9588cc5fc46",
        "IP_service": "e2db01227b4a5ffaaf71f328d16f93e5"
    }

    OFFICIAL_PUSH_API = "https://api.line.me/v2/bot/message/push"
    OFFICIAL_NOTIFY_API = "https://notify-api.line.me/api/notify"
    OFFICIAL_OAUTH_API = "https://notify-bot.line.me/oauth/token"
    OFFICIAL_REPLY_API = "https://api.line.me/v2/bot/message/reply"
    OFFICIAL_CONTENT_API = "https://api-data.line.me/v2/bot/message/<file_id>/content"

    def generate_push_or_reply_header(self, token_identifier):
        # HINT 此Header可兼容於push and reply
        header = {
            'Content-Type': 'application/json; charset=UTF-8',
            'Authorization': f'Bearer {self.access_tokens.get(token_identifier)}'}
        return header

    notify_header = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }

    Register_Notify = dict(
        CLIENT_ID="UulwSUMmf5M9zY1HSTR8xy",
        SECRET="MDuIohlUsEsPRKP2VXq0weJAW3cYwbb24gfeixTDmVC",
        Linux="https://linebot-kuochuwon.herokuapp.com/api/v1/linebot/callback",
        Windows="http://127.0.0.1:5000/api/v1/linebot/callback"
    )

    PUSH = dict(
        Linux="https://linebot-kuochuwon.herokuapp.com/api/v1/linebot/push",
        Windows="http://127.0.0.1:5000/api/v1/linebot/push"
    )

    NOTIFY = dict(
        Linux="https://linebot-kuochuwon.herokuapp.com/api/v1/linebot/notify",
        Windows="http://127.0.0.1:5000/api/v1/linebot/notify"
    )
