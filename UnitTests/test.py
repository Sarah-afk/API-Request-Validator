import requests
import unittest

class Testing(unittest.TestCase):
    
    def test_validate_success(self):
        data = {
            "customerID":1,
            "tagID":2,
            "userID":"aaaaaaaa-bbbb-cccc-1111-222222222222",
            "remoteIP":"123.234.56.78",
            "timestamp":1500000000
        }
        r = requests.post(url='http://127.0.0.1:8000/validate', data=data)
        self.assertEqual(r.text, 'Processing Done')
        self.assertEqual(r.status_code, 200)

    def test_validate_ip_block(self):
        data = {
            "customerID":1,
            "tagID":2,
            "userID":"aaaaaaaa-bbbb-cccc-1111-222222222222",
            "remoteIP":"0.0.0.0",
            "timestamp":1500000000
        }
        r = requests.post(url='http://127.0.0.1:8000/validate', data=data)
        self.assertEqual(r.text, 'IP is blocked')
        self.assertEqual(r.status_code, 401)
        
    def test_validate_customer_inactive(self):
        data = {
            "customerID":3,
            "tagID":2,
            "userID":"aaaaaaaa-bbbb-cccc-1111-222222222222",
            "remoteIP":"123.234.56.78",
            "timestamp":1500000000
        }
        r = requests.post(url='http://127.0.0.1:8000/validate', data=data)
        self.assertEqual(r.text, 'Customer is inactive')
        self.assertEqual(r.status_code, 401)
        
    def test_validate_ua_block(self):
        data = {
            "customerID":1,
            "tagID":2,
            "userID":"aaaaaaaa-bbbb-cccc-1111-222222222222",
            "remoteIP":"123.234.56.78",
            "timestamp":1500000000
        }
        r = requests.post(url='http://127.0.0.1:8000/validate', data=data, headers={'User-Agent': 'A6-Indexer'})
        self.assertEqual(r.text, 'User-Agent is blocked')
        self.assertEqual(r.status_code, 401)
        
    def test_validate_missing_parameter(self):
        data = {
            "customerID":1,
            "tagID":2,
            "remoteIP":"123.234.56.78",
            "timestamp":1500000000
        }
        r = requests.post(url='http://127.0.0.1:8000/validate', data=data)
        self.assertEqual(r.text, 'Invalid Request')
        self.assertEqual(r.status_code, 400)
        
    def test_validate_wrong_format_parameter(self):
        data = {
            "customerID":1,
            "tagID":2,
            "userID":"aaaaaaaa-bbbb-cccc-1111-222222222222",
            "remoteIP":"test",
            "timestamp":1500000000
        }
        r = requests.post(url='http://127.0.0.1:8000/validate', data=data)
        self.assertEqual(r.text, 'Invalid Request')
        self.assertEqual(r.status_code, 400)
        
    def test_validate_customer_not_found(self):
        data = {
            "customerID":10,
            "tagID":2,
            "userID":"aaaaaaaa-bbbb-cccc-1111-222222222222",
            "remoteIP":"123.234.56.78",
            "timestamp":1500000000
        }
        r = requests.post(url='http://127.0.0.1:8000/validate', data=data)
        self.assertEqual(r.text, 'Customer does not exist')
        self.assertEqual(r.status_code, 404)


    def test_stats_success(self):
        data = {
            "customerID":1,
            "day":'15/7/2017'
        }
        r = requests.get(url='http://127.0.0.1:8000/getStats', data=data)
        self.assertTrue(('customer' in r.json()) and ('daily_stats_total' in r.json()))
        self.assertEqual(r.status_code, 200)
        
    def test_stats_customer_not_found(self):
        data = {
            "customerID":10,
            "day":'15/7/2017'
        }
        r = requests.post(url='http://127.0.0.1:8000/getStats', data=data)
        self.assertEqual(r.text, 'Customer does not exist')
        self.assertEqual(r.status_code, 404)
        
    def test_stats_invalid_day(self):
        data = {
            "customerID":10,
            "day":'15/15/2017'
        }
        r = requests.post(url='http://127.0.0.1:8000/getStats', data=data)
        self.assertEqual(r.text, 'Invalid Request')
        self.assertEqual(r.status_code, 400)

if __name__ == '__main__':
    unittest.main()