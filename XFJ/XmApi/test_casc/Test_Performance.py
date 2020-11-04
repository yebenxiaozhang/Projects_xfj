# -*- coding: utf-8 -*-
# @Time    : 2019/12/19 18:08
# @Author  : 潘师傅
# @File    : 补业绩补流水.py
from XFJ.PubilcAPI.FlowPath import *
import requests


class ResultsTheChangeTestCace(unittest.TestCase):
    """小秘----补业绩补流水"""
    def test_02(self):
        """"""
        dealId = [9644]
        dealIds = dealId
        z = 0
        while z < len(dealId):
            try:
                r = requests.post(url='http://api.xfj100.com/api/mobile/projectAdminService/repairPerformance',
                                  data={'agentToken': 'f690a96e-118d-4597-825e-b472beecc17b',
                                        'dealId': dealId[z]})
                time.sleep(0.2)
                globals()['r.text'] = json.loads(r.text)
                if r.status_code == 200 and 1 == globals()['r.text']['resultCode']:
                    try:
                        r = requests.post(url=
                                          'http://api.xfj100.com/api/mobile/projectAdminService/repairFlowing',
                                          data={'agentToken': 'f690a96e-118d-4597-825e-b472beecc17b',
                                                'dealId': dealId[z]})
                        time.sleep(0.2)
                        globals()['r.text'] = json.loads(r.text)
                        if r.status_code == 200 and 1 == globals()['r.text']['resultCode']:
                            dealIds.remove((dealId[z]))
                            print(dealIds)
                            z = z - 1
                    except Exception as e:
                        pass
                z = z + 1
            except Exception as e:
                pass
                print(e)
            continue
        print(dealId)


# try:
# #
# # except Exception as e:
# #     pass
# #     print(e)
# # continue