import requests
 
class MobSMS:
    def __init__(self, appkey):
        self.appkey = appkey
        self.verify_url = 'https://webapi.sms.mob.com/sms/verify'
 
    def verify_sms_code(self, zone, phone, code, debug=False):
        if debug:
            return 200
 
        data = {'appkey': self.appkey, 'phone': phone, 'zone': zone, 'code': code}
        req = requests.post(self.verify_url, data=data, verify=debug)
        if req.status_code == 200:
            j = req.json()
            return j.get('status', 500)
 
        return 500
 
if __name__ == '__main__':
    mobsms = MobSMS('148f6c0a15c12')
    print mobsms.verify_sms_code(86, 13900000000, '1234', True)