from alipay import AliPay

alipay_public_key_string = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvu8nR/GDlBxY2/J4nwHxsKabC+WeCf1N0xzOXMwFfo7Fj6zsNnGSASWnMIMzF9/jqy6ypsbX/xP+b9534fHlftja3CaJ+uCHqF4g1fdH0S46tWy9yIZHaq5d7EqMIVHLaYHR/TSFPSgqpmTtk83oiUGShqtE2tDl68/mOIjqN91jCAPcTF8XXK1Tqw2+SZn4zWVTZotoIG11F3x+TWpR+yPpswXfOhZ6JMWZP7uu0wIPDL1l4sSZovYjI1v38VxUPNEn/XbfBXe7KtUd1DXfBTbbmTrtFy7hJlSAw+xD50TqujCPU1xpN/D/EWJF7GCAMAxHyKUwjWQigzSPMLX/PQIDAQAB
-----END PUBLIC KEY-----"""

app_private_key_string = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAvu8nR/GDlBxY2/J4nwHxsKabC+WeCf1N0xzOXMwFfo7Fj6zsNnGSASWnMIMzF9/jqy6ypsbX/xP+b9534fHlftja3CaJ+uCHqF4g1fdH0S46tWy9yIZHaq5d7EqMIVHLaYHR/TSFPSgqpmTtk83oiUGShqtE2tDl68/mOIjqN91jCAPcTF8XXK1Tqw2+SZn4zWVTZotoIG11F3x+TWpR+yPpswXfOhZ6JMWZP7uu0wIPDL1l4sSZovYjI1v38VxUPNEn/XbfBXe7KtUd1DXfBTbbmTrtFy7hJlSAw+xD50TqujCPU1xpN/D/EWJF7GCAMAxHyKUwjWQigzSPMLX/PQIDAQABAoIBAQC559vkZdjKposypTUjBV6RtLa0b79gVJ2pF5wqqJAU+OiNiz53iD80FLhkOOrPrTRc4dwbHPMErzAHNqKdgc0FpBn9Txz8BBCyM+xeySXJG+0X5ygmjfANhHd48eDdNGoNcdTHaJLuyCQ23YChcFShCBKmQy6Iq+uinku38j+zYZAjNbUP1QtHZkIrR36bLUfHJPfz403SV8Jz9VQ9jx6iq0KTPoEeDDm28+6Vdzqssp0zOUdUUtQJnHtmBNFvhwasJiX+rzAM62zc0cD+QCCaEuwO0y6EQapowri4RxA4MKcZn9fb6iAZ7E6YAsLMfccrcEwu7NcEeR3/xppNhoD1AoGBAPSpVIRX+pQNvzYwL0zHyfvoP24SDsetN63+6UDHFOHGreOJu4AqCsHbobBBYajtNxr8WOZh0fu4bwDx9tbL0Lja+BptEGNnccUTnynf1dxlYZMO5goDTrRaraVuPwoXFnsWP8HKvut5QvhgnE3Tv1bJOMWSRqeLDA0QAV9q+S8jAoGBAMfIZtkwraDerjVJwdn1+t7llhpQqJLeCgqXqtdbABXhB/Q7/UpOoyLOvHhznVyAbaRo0d3oeANrCYvxeCnzhxzmZmflPwPwfjBwIHpwkb7nT2Q1ArslXdn5JUa0KRoGvTBBj/V9FdCARA4cdTkzD7CB/hiOM1gIARbISOkTOy4fAoGBAKjoYjX/+znNh83kVDNg1vx3qZrXEqcd2gvgqa4UA0GgBZrKEs13uPd/JtBlQwP5yQpzXvimXe63tMLlSXGfQljsq06rLx5BY1UYp9Cj/KRsxYFeTsho4iQ3WhyU0SapK9cMVDX5P/eXPvn00NQWNMm4n94ej3LJ1ycJfrkeRCwbAoGAPsEaXVrHD2MjQaXbeIWlueJQFhAEA64vZUhi56a0DitTfkphs7ej0skxtnxKj8XfqucqFRRyrlAu/YBqCHNwm4lb3YLLGoeue7Sc3xkBDwBFlep44yRHqLJ0HRN2XbCEOOY/PBOAiK/hsLULtV3urbkHgdsZEavh+7AKBvx9eG0CgYBc4HqfA7+Lcg6FhW6corRXXlV3JfandQ7VcPKpQbHRJprjZjxKrZ/2heCTuaveM9XmBvp7xHljMN4PWqCkOia2rAl7QvOMhCNznfYck/OyeFB+ODz+7/SGQGhhiYjZybmxe5Oglm+zrl65aQiqQIM857AcwQM7SIbme7dnmJU/IQ==
-----END RSA PRIVATE KEY-----"""

alipay = AliPay(
    appid = "2016101000652528",
    app_notify_url = None,
    app_private_key_string = app_private_key_string,
    alipay_public_key_string = alipay_public_key_string,
    sign_type= "RSA2"
)

#发起支付请求
order_string = alipay.api_alipay_trade_page_pay(
    out_trade_no="3345666", #订单号
    total_amount=str(1000.01),#支付金额
    subject="生鲜交易", #交易主题
    return_url=None,
    notify_url=None
)

print("https://openapi.alipaydev.com/gateway.do?"+order_string)