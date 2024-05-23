VNPAY_RETURN_URL = 'http://localhost:8000/payment_return'  # get from config
VNPAY_PAYMENT_URL = 'https://sandbox.vnpayment.vn/paymentv2/vpcpay.html'  # get from config
VNPAY_API_URL = 'https://sandbox.vnpayment.vn/merchant_webapi/api/transaction'
VNPAY_TMN_CODE = 'CYZU49BC'  # Website ID in VNPAY System, get from config
VNPAY_HASH_SECRET_KEY = 'CEQDYXLUXTVTRNRBWKXWHAQXLFVBWOYM'  # Secret key for create checksum,get from config

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'cskhvavshop@gmail.com'
EMAIL_HOST_PASSWORD = 'vwup lvga wsim smuy' 