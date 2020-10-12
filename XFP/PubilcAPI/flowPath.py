
from XFP.PubilcAPI.webApi import *


class flowPath:
    """"""
    def __init__(self, *args, **kwargs):
        super(flowPath, self).__init__(*args, **kwargs)
        self.XfpRequest = appApi()
        self.appApi = self.XfpRequest
        self.appText = GlobalMap()
        self.webText = GlobalMap()
        self.flowPathText = GlobalMap()

    def client_list_non_null(self):
        """客户列表--非空"""
        self.appApi.ClientList()                # 客户列表
        if self.appText.get('total') == 0:
            self.appApi.my_clue_list()          # 线索列表
            if self.appText.get('total') == 0:
                self.appApi.SeaList()           # 公海列表
                if self.appText.get('total') == 0:
                    print('公海列表为空？')
                    raise RuntimeError(self.appText.get('ApiXfpUrl'))
                else:
                    self.appApi.clue_Assigned()     # 领取线索
                    self.appApi.my_clue_list()      # 线索列表
                    if self.appText.get('total') == '0':
                        print('领取线索失败？')
                        raise RuntimeError(self.appText.get('ApiXfpUrl'))
            self.appApi.ClueInfo()
            self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
                                       loanSituation='这个是贷款情况')
            self.appApi.ClientList()  # 客户列表
            if self.appApi.appText.get('total') == 0:
                print('线索转客户异常？')
                raise RuntimeError(self.appText.get('ApiXfpUrl'))

    def add_visit(self):
        """创建带看"""
        self.client_list_non_null()
        self.appApi.GetMatchingAreaHouse()
        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        self.flowPathText.set_map('time', dome)
        self.appApi.ClientVisitAdd(projectAId=self.appText.get('houseId'),
                                   appointmentTime=dome)
        while self.appText.get('data') == '该客户已申请客户带看跟进,正在审核中!':
            self.appApi.GetLabelList(labelNo='SZGJYY', labelName='客户已成交')
            self.appApi.client_exile_sea(labelId=self.appText.get('labelId'))
            self.client_list_non_null()
            self.appApi.ClientVisitAdd(projectAId=self.appText.get('houseId'),
                                       appointmentTime=dome)

    def accomplish_visit(self):
        """完成带看"""
        self.visit_status(status='进行中')
        self.appApi.ClientTask(taskTypeStr='带看行程')
        if self.appText.get('total') < 1:
            raise RuntimeError(self.appText.get('ApiXfpUrl'))
        self.appApi.visit_info()
        self.appApi.VisitFlow1()
        self.appApi.ClientTask()
        if self.appText.get('total') >= 2:
            raise RuntimeError(self.appText.get('ApiXfpUrl'))
        self.appApi.Task_Visit_List(appointmentTime=self.flowPathText.get('time'))
        assert self.appText.get('visiteStatus'), '1'
        assert self.appText.get('visiteStatusStr'), '已完成'

    def client_exile_sea(self):
        """客户流放公海"""
        self.appApi.GetLabelList(labelNo='SZGJYY', labelName='客户已成交')
        self.appApi.client_exile_sea(labelId=self.appText.get('labelId'))

    def advance_over_visit(self):
        """提前结束带看"""
        self.appApi.ClientTask(taskTypeStr='带看行程')
        self.appApi.visit_info()
        self.appApi.OverVisit()  # 提前结束代办
        self.appApi.ClientTask()
        if self.appText.get('total') > 1:
            print('提前结束带看，任务还存在')
            raise RuntimeError(self.appText.get('ApiXfpUrl'))
        self.appApi.ClientFollowList()
        assert self.appText.get('followContent'), '提前结束带看'

    def visit_status(self, status):
        """带看状态"""
        self.appApi.Task_Visit_List(appointmentTime=self.flowPathText.get('time'))
        if status == '进行中':
            assert self.appText.get('visiteStatus') == '0', '状态异常'
            assert self.appText.get('visiteStatusStr') == '进行中', '状态异常'
        elif status == '已取消':
            assert self.appText.get('visiteStatus') == '2', '状态异常'
            assert self.appText.get('visiteStatusStr') == '已取消', '状态异常'
        elif status == '已完成':
            assert self.appText.get('visiteStatus') == '1', '状态异常'
            assert self.appText.get('visiteStatusStr') == '已完成', '状态异常'
        elif status == '已驳回':
            assert self.appText.get('visiteStatus') == '2', '状态异常'
            assert self.appText.get('visiteStatusStr') == '已驳回', '状态异常'
        elif status == '申请中':
            assert self.appText.get('visiteStatus') == '3', '状态异常'
            assert self.appText.get('visiteStatusStr') == '申请中', '状态异常'
        elif status == '审核中':
            assert self.appText.get('visiteStatus') == '3', '状态异常'
            assert self.appText.get('visiteStatusStr') == '审核中', '状态异常'






