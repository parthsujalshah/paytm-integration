from flask import Flask, render_template
app = Flask(__name__)
from dotenv import load_dotenv
from os import path, environ
import secrets
# import ChecksumApp
import paytmchecksum

basedir = path.abspath(path.dirname(path.dirname(__file__)))
load_dotenv(path.join(basedir, '.env'))

@app.route('/payment/make', methods=['GET', 'POST'])
def payment_make():
    paytmParams = {
        "MID" : environ.get('PAYTM_MERCHANT_ID'),
        "WEBSITE" : "WEBSTAGING",
        "ORDER_ID" : str(secrets.token_hex(16)), # change this everytime
        "CUST_ID" : "1",
        "MOBILE_NO" : "1234567890",
        "EMAIL" : "abc@gmail.com",
        "INDUSTRY_TYPE_ID" : "Retail",
        'CHANNEL_ID':'WAP',
        # 'CHANNEL_ID':'WEB',
        "TXN_AMOUNT" : "200",
        "CALLBACK_URL" : "http://127.0.0.1:5000/payment/callback",
    }
    merchant_key = environ.get('PAYTM_MERCHANT_KEY')
    paytmParams['CHECKSUMHASH'] = str(paytmchecksum.generateSignature(paytmParams, merchant_key))
    # for Staging
    url = "https://securegw-stage.paytm.in/order/process"
    # for Production
    # url = "https://securegw.paytm.in/order/process"
    return render_template('paytm_view.html', paytmParams=paytmParams, url=url)

@app.route('/payment/callback', methods=['GET', 'POST'])
def payment_callback():
    print(request)
    return 'hi'


if __name__ == "__main__":
    app.run(debug=True)