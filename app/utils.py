import hashlib
import hmac
import json
from datetime import datetime
import random as rand

import requests
from flask import request

from app import settings
from app.vnpay import vnpay

datetime_f = '%Y-%m-%d %H:%M'

def str_datetime(date):
    date = date.replace('%3A', ':')
    date = date.replace('T', ' ')
    return date

def vnpt_payment(amount, order_info, order_id, ip, cb_id):
        vnp = vnpay()
        vnp.requestData['vnp_Version'] = '2.1.0'
        vnp.requestData['vnp_Command'] = 'pay'
        vnp.requestData['vnp_TmnCode'] = settings.VNPAY_TMN_CODE
        vnp.requestData['vnp_Amount'] = amount * 100
        vnp.requestData['vnp_CurrCode'] = 'VND'
        vnp.requestData['vnp_TxnRef'] = order_id
        vnp.requestData['vnp_OrderInfo'] = order_info
        vnp.requestData['vnp_OrderType'] = 'order'
        vnp.requestData['vnp_Locale'] = 'vn'
        vnp.requestData['vnp_CreateDate'] = datetime.now().strftime('%Y%m%d%H%M%S')
        vnp.requestData['vnp_IpAddr'] = '127.0.0.1'
        vnp.requestData['vnp_ReturnUrl'] = settings.VNPAY_RETURN_URL
        vnpay_payment_url = vnp.get_payment_url(settings.VNPAY_PAYMENT_URL, settings.VNPAY_HASH_SECRET_KEY)
        return vnpay_payment_url

def payment_return(request):
    inputData = request
    if inputData:
        vnp = vnpay()
        vnp.responseData = dict(inputData)
        order_id = inputData['vnp_TxnRef']
        amount = int(inputData['vnp_Amount']) / 100
        order_desc = inputData['vnp_OrderInfo']
        vnp_TransactionNo = inputData['vnp_TransactionNo']
        vnp_ResponseCode = inputData['vnp_ResponseCode']
        vnp_TmnCode = inputData['vnp_TmnCode']
        vnp_PayDate = inputData['vnp_PayDate']
        vnp_BankCode = inputData['vnp_BankCode']
        vnp_CardType = inputData['vnp_CardType']
        if vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY):
            if vnp_ResponseCode == "00":
                return  {"title": "Kết quả thanh toán",
                                                               "result": "Thành công", "order_id": order_id,
                                                               "amount": amount,
                                                               "order_desc": order_desc,
                                                               "vnp_TransactionNo": vnp_TransactionNo,
                                                               "vnp_ResponseCode": vnp_ResponseCode,
                                                                'status': 1}
            else:
                return  {"title": "Kết quả thanh toán",
                                                               "result": "Lỗi", "order_id": order_id,
                                                               "amount": amount,
                                                               "order_desc": order_desc,
                                                               "vnp_TransactionNo": vnp_TransactionNo,
                                                               "vnp_ResponseCode": vnp_ResponseCode,
                                                                'status': 0}
        else:
            return {"title": "Kết quả thanh toán", "result": "Lỗi", "order_id": order_id, "amount": amount,
                           "order_desc": order_desc, "vnp_TransactionNo": vnp_TransactionNo,
                           "vnp_ResponseCode": vnp_ResponseCode, "msg": "Sai checksum"}
    else:
        return {"title": "Kết quả thanh toán", "result": ""}




if __name__ == '__main__':
    n = str(rand.randint(10 ** 11, 10 ** 12 - 1)) + datetime.now().strftime('%Y%m%d%H%M%S')
    n_str = str(n)
    print(vnpt_payment(int(1270000.0), 'Thanh toán demo', n_str, '127.0.0.1', cb_id=2))