
from XFP.PubilcAPI.webApi import *


class flowPath:
    """"""
    def __init__(self, *args, **kwargs):
        super(flowPath, self).__init__(*args, **kwargs)
        self.XfpRequest = appApi()
        self.appApi = self.XfpRequest
        # self.appApi.appText = GlobalMap()
        # self.webText = GlobalMap()
        self.flowPathText = GlobalMap()
        self.XfpwebRequest = webApi()
        self.webApi = self.XfpwebRequest

    def client_list_non_null(self):
        """客户列表--非空"""
        self.appApi.ClientList()                # 客户列表
        if self.appApi.appText.get('total') == 0:
            self.clue_non_null()
            self.appApi.ClueInfo()
            # self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
            #                            loanSituation='这个是贷款情况')
            # if self.appApi.appText.get('data') == '该线索未首电,不能转化为有效线索!':
            try:
                self.appApi.phone_log(callee_num=self.appApi.appText.get('cluePhone'),
                                      is_own_call=0, talk_time=12000,
                                      call_time=time.strftime("%Y-%m-%d %H:%M:%S"))
            except:
                self.appApi.ClueFollowList()
                self.appApi.ClueFollowSave(taskEndTime=time.strftime("%Y-%m-%d") + ' 22:00:00')
            else:
                pass
            self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
                                       loanSituation='这个是贷款情况')
            self.appApi.ClientList()  # 客户列表
            if self.appApi.appText.get('total') == 0:
                print('线索转客户异常？')
                raise RuntimeError(self.appApi.appText.get('ApiXfpUrl'))

    def clue_non_null(self):
        """线索列表---非空"""
        self.appApi.my_clue_list()  # 线索列表
        if self.appApi.appText.get('total') == 0:
            self.appApi.SeaList()  # 公海列表
            if self.appApi.appText.get('total') == 0:
                print('公海列表为空？')
                raise RuntimeError(self.appApi.appText.get('ApiXfpUrl'))
            else:
                self.appApi.clue_Assigned()  # 领取线索
                self.appApi.my_clue_list()  # 线索列表
                if self.appApi.appText.get('total') == '0':
                    print('领取线索失败？')
                    raise RuntimeError(self.appApi.appText.get('ApiXfpUrl'))

    def add_visit(self):
        """创建带看"""
        self.client_list_non_null()
        self.appApi.GetMatchingAreaHouse()
        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        self.flowPathText.set_map('time', dome)
        self.appApi.ClientVisitAdd(projectAId=self.appApi.appText.get('houseId'),
                                   appointmentTime=dome)
        while self.appApi.appText.get('data') == '已申请客户带看,正在审核中!' or self.appApi.appText.get('data') == '该客户已申请客户带看跟进审核,正在审核中!':
            self.appApi.GetLabelList(labelNo='SZGJYY', labelName='客户已成交')
            self.appApi.client_exile_sea(labelId=self.appApi.appText.get('labelId'))
            self.client_list_non_null()
            self.appApi.ClientVisitAdd(projectAId=self.appApi.appText.get('houseId'),
                                       appointmentTime=dome)

    def accomplish_visit(self):
        """完成带看"""
        self.visit_status(status='进行中')
        self.appApi.ClientTask(taskTypeStr='带看行程')
        if self.appApi.appText.get('total') < 1:
            raise RuntimeError(self.appApi.appText.get('ApiXfpUrl'))
        self.appApi.visit_info()
        self.appApi.VisitFlow1()
        self.appApi.ClientTask()
        if self.appApi.appText.get('total') >= 2:
            raise RuntimeError(self.appApi.appText.get('ApiXfpUrl'))
        self.appApi.Task_Visit_List(appointmentTime=self.flowPathText.get('time'))
        assert self.appApi.appText.get('visiteStatus'), '1'
        assert self.appApi.appText.get('visiteStatusStr'), '已完成'

    def client_exile_sea(self):
        """客户流放公海"""
        self.appApi.GetLabelList(labelNo='SZGJYY', labelName='客户已成交')
        self.appApi.client_exile_sea(labelId=self.appApi.appText.get('labelId'))

    def clue_exile_sea(self):
        """线索流放公海"""
        self.appApi.GetLabelList(labelNo='SZGJYY', labelName='客户已成交')
        self.appApi.ExileSea(labelId=self.appApi.appText.get('labelId'))

    def advance_over_visit(self):
        """提前结束带看"""
        self.appApi.ClientTask(taskTypeStr='带看行程')
        self.appApi.visit_info()
        self.appApi.OverVisit()  # 提前结束代办
        self.appApi.ClientTask()
        if self.appApi.appText.get('total') > 1:
            print('提前结束带看，任务还存在')
            raise RuntimeError(self.appApi.appText.get('ApiXfpUrl'))
        self.appApi.ClientFollowList()
        assert self.appApi.appText.get('followContent'), '提前结束带看'

    def visit_status(self, status):
        """带看状态"""
        self.appApi.Task_Visit_List(appointmentTime=self.flowPathText.get('time'))
        if status == '进行中':
            assert self.appApi.appText.get('visiteStatus') == '0', '状态异常'
            assert self.appApi.appText.get('visiteStatusStr') == '进行中', '状态异常'
        elif status == '已取消':
            assert self.appApi.appText.get('visiteStatus') == '2', '状态异常'
            assert self.appApi.appText.get('visiteStatusStr') == '已取消', '状态异常'
        elif status == '已完成':
            assert self.appApi.appText.get('visiteStatus') == '1', '状态异常'
            assert self.appApi.appText.get('visiteStatusStr') == '已完成', '状态异常'
        elif status == '已驳回':
            assert self.appApi.appText.get('visiteStatus') == '2', '状态异常'
            assert self.appApi.appText.get('visiteStatusStr') == '已驳回', '状态异常'
        elif status == '申请中':
            assert self.appApi.appText.get('visiteStatus') == '3', '状态异常'
            assert self.appApi.appText.get('visiteStatusStr') == '申请中', '状态异常'
        elif status == '审核中':
            assert self.appApi.appText.get('visiteStatus') == '3', '状态异常'
            assert self.appApi.appText.get('visiteStatusStr') == '审核中', '状态异常'
            
    def suspend_follow(self):
        """暂缓跟进"""
        try:
            self.client_list_non_null()
            self.appApi.GetLabelList(labelNo='SQZHGJ', labelName='其他')
            self.appApi.ClientTaskPause()
            while self.appApi.appText.get('data') == '该客户已被暂缓!':
                self.appApi.GetLabelList(labelNo='SZGJYY', labelName='客户已成交')
                self.appApi.ExileSea(labelId=self.appApi.appText.get('labelId'))
                self.client_list_non_null()
                self.appApi.GetLabelList(labelNo='SQZHGJ', labelName='其他')
                self.appApi.ClientTaskPause()
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.appApi.appText.get('ApiXfpUrl'))

    def apply_status(self, status):
        dome = self.appApi.appText.get('clueId')
        self.appApi.follow_apply()
        if status == '进行中':
            assert self.appApi.appText.get('auditStatueApp') == 0, '状态异常'
            assert self.appApi.appText.get('auditStatueStr') == '进行中', '状态异常'
        elif status == '已取消':
            assert self.appApi.appText.get('auditStatueApp') == 2, '状态异常'
            assert self.appApi.appText.get('auditStatueStr') == '已取消', '状态异常'
        elif status == '已同意':
            assert self.appApi.appText.get('auditStatueApp') == 1, '状态异常'
            assert self.appApi.appText.get('auditStatueStr') == '已同意', '状态异常'
        elif status == '已驳回':
            assert self.appApi.appText.get('auditStatueApp') == 2, '状态异常'
            assert self.appApi.appText.get('auditStatueStr') == '已驳回', '状态异常'
        elif status == '申请中':
            assert self.appApi.appText.get('auditStatueApp') == 0, '状态异常'
            assert self.appApi.appText.get('auditStatueStr') == '申请中', '状态异常'
        elif status == '审核中':
            assert self.appApi.appText.get('auditStatueApp') == 1, '状态异常'
            assert self.appApi.appText.get('auditStatueStr') == '审核中', '状态异常'
        assert self.appApi.appText.get('clueId') == dome, '跟进申请-无记录'
    
    def add_deal(self):
        """录入成交"""
        try:
            self.appApi.deal_List()
            dome = self.appApi.appText.get('total')
            self.client_list_non_null()
            self.appApi.GetMatchingAreaHouse()             # 匹配楼盘
            assert 0 != self.appApi.appText.get('total'), '匹配楼盘为空？'
            self.appApi.GetLabelList(labelNo='CJX', labelName='认购')
            self.appApi.add_deal()                  # 录入成交
            if self.appApi.appText.get('data') == '已申请客户成交,正在审核中!':
                self.clue_non_null()
                self.appApi.ClueInfo()
                self.appApi.phone_log(callee_num=self.appApi.appText.get('cluePhone'),
                                      is_own_call=0, talk_time=12000,
                                      call_time=time.strftime("%Y-%m-%d %H:%M:%S"))
                self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
                                           loanSituation='这个是贷款情况')
                self.appApi.ClientList()  # 客户列表
                self.appApi.GetMatchingAreaHouse()  # 匹配楼盘
                assert 0 != self.appApi.appText.get('total'), '匹配楼盘为空？'
                self.appApi.GetLabelList(labelNo='CJX', labelName='认购')
                self.appApi.add_deal()  # 录入成交
            self.appApi.deal_List()
            assert dome != self.appApi.appText.get('total')
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.appApi.appText.get('ApiXfpUrl'))

    def deal_status(self, status):
        """成交状态"""
        dome = self.appApi.appText.get('clueId')
        self.appApi.deal_List()
        if status == '0' or status == 0:
            assert self.appApi.appText.get('transStatus') == 0, '状态异常'
        elif status == '1' or status == 1:
            assert self.appApi.appText.get('transStatus') == 1, '状态异常'
        elif status == '2' or status == 2:
            assert self.appApi.appText.get('transStatus') == 2, '状态异常'
        assert self.appApi.appText.get('clueId') == dome, '跟进申请-无记录'

    def first_phone_non_null(self):
        """首电不为空"""
        self.clue_non_null()
        self.appApi.ClueInfo()
        self.appApi.TodayClue(keyWord=self.appApi.appText.get('cluePhone'))
        while self.appApi.appText.get('isFirst') == 1:
            self.clue_exile_sea()
            self.clue_non_null()
            self.appApi.ClueInfo()
            self.appApi.TodayClue(keyWord=self.appApi.appText.get('cluePhone'))

    def add_new_clue(self):
        """新增一条线索"""
        try:
            self.appApi.GetLabelList(labelNo='XSLY', labelName='百度小程序')
            if self.appApi.appText.get('labelId') is None:
                self.webApi.add_label(labelName='百度小程序', labelId=self.appApi.appText.get('LabelId'),
                                      pid=self.appApi.appText.get('LabelId'))
                self.appApi.GetLabelList(labelNo='XSLY', labelName='百度小程序')
            self.appApi.GetUserLabelList(userLabelType='线索标签')
            if self.appApi.appText.get('total') == 0:
                self.appApi.AddUserLabel()
                self.appApi.GetUserLabelList(userLabelType='线索标签')
            self.appApi.ClueSave(clueNickName=self.appApi.RandomText(textArr=surname),
                                 sourceId=self.appApi.appText.get('labelId'),
                                 keyWords=self.appApi.appText.get('labelData'))
            # 在搜索列表进行查找
            globals()['CluePhone'] = self.appApi.appText.get('cluePhone')
            self.appApi.ClueList(keyWord=(self.appApi.appText.get('cluePhone')))
            assert self.appApi.appText.get('cluePhone') == globals()['CluePhone'], '新增线索列表异常'
            """今日上户上进行查看"""
            self.appApi.TodayClue(keyWord=self.appApi.appText.get('cluePhone'))
            assert self.appApi.appText.get('isFirst') == 0, '新增线索是未首电'
            time.sleep(2)
            # self.test_4_ExileSea()
        except BaseException as e:
                print("错误，错误原因：%s" % e)
                raise RuntimeError(self.appApi.appText.get('ApiXfpUrl'))



