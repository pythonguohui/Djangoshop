from django.test import TestCase


str="charset=utf-8&out_trade_no=1000001&method=alipay.trade.page.pay.return&total_amount=12.00&sign=ms94VLiCiLkdqrwx6mBbuwAHfES0eJW3lHzUaERssn2ThK9bPkPYtegB4dcgtyQV8W5GwlHkx8WUnz8CniP0f%2BMvbN0QD%2FJ2xewZrQwI6sRbauJfSNLWDFCU9SNKEuZcin0tI8Wwd966isR3YUduJaq%2Bqz4c7zfC2gysd%2FVR%2Bp33Hqo%2B%2FvVPpJWzKAGTgIouiEnXAqQmFZAVP4IpHacuzrhPp9p9XDXlqmVRxpHpIDtpPDyBSvQHJ47xGbUIduC%2Fc2tPXhaypetkNOFZaAGgsyp7j4HEf7K4hI3o5rB7dnNi8ByK0rX3nSq23FiT9WmQfBLcudP0IUknRN9dDSgB0A%3D%3D&trade_no=2019072722001422311000052906&auth_app_id=2016101000652528&version=1.0&app_id=2016101000652528&sign_type=RSA2&seller_id=2088102178923106&timestamp=2019-07-27+13%3A56%3A35"
print(str.split("&"))
# Create your tests here.
