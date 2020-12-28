from PubilcAPI.webApi import *
from datetime import date, timedelta


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
        self.appApi.ClientList()  # 客户列表
        if self.appApi.appText.get('total') == 0:
            self.clue_non_null()
            try:
                self.appApi.phone_log(callee_num=self.appApi.appText.get('cluePhone'),
                                      is_own_call=0, talk_time=12000,
                                      call_time=time.strftime("%Y-%m-%d %H:%M:%S"))
                self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
                                           loanSituation='这个是贷款情况')
            except:
                self.appApi.ClueFollowList()
                self.appApi.ClueFollowSave(taskEndTime=time.strftime("%Y-%m-%d %H:%M:%S"))
                self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
                                           loanSituation='这个是贷款情况')
            self.appApi.ClientList()  # 客户列表
            if self.appApi.appText.get('total') == 0:
                print('线索转客户异常？')
                raise RuntimeError(self.appApi.appText.get('ApiXfpUrl'))
        self.appApi.client_info()

    def clue_non_null(self):
        """线索列表---非空"""
        self.appApi.my_clue_list()  # 线索列表
        if self.appApi.appText.get('total') == 0:
            self.appApi.SeaList()  # 公海列表
            if self.appApi.appText.get('total') == 0:
                self.add_new_clue()
                self.appApi.my_clue_list()  # 线索列表
                if self.appApi.appText.get('total') == 0:
                    print('新增线索失败？')
            else:
                self.appApi.clue_Assigned()  # 领取线索
                self.appApi.my_clue_list()  # 线索列表
                if self.appApi.appText.get('total') == 0:
                    print('领取线索失败？')
        self.appApi.ClueInfo()

    def add_visit(self, dome=None):
        """创建带看"""
        if dome is None:
            dome = time.strftime("%Y-%m-%d %H:%M:%S")
        self.client_list_non_null()
        self.flowPathText.set_map('time', dome)
        self.appApi.ClientTask(taskType='3')
        if self.appApi.appText.get('total') == 2:
            self.advance_over_visit()
            if self.appApi.appText.get('code') != 200:
                self.clue_non_null()
                self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
                                           loanSituation='这个是贷款情况')
                self.client_list_non_null()
        self.appApi.ClientVisitAdd(projectAId=self.appApi.appText.get('houseId'),
                                   appointmentTime=dome,
                                   seeingConsultant=self.appApi.appText.get('consultantId'),
                                   appointConsultant=self.appApi.appText.get('consultantId'))

    def accomplish_visit(self):
        """完成带看"""
        # self.visit_status(status='无需审核')
        self.appApi.ClientTask(taskType='3')
        if self.appApi.appText.get('total') < 1:
            raise RuntimeError(self.appApi.appText.get('ApiXfpUrl'))
        self.appApi.visit_info()

        self.appApi.VisitFlow1(agencyId=self.appApi.appText.get('DLGS'),
                               receptionName=self.appApi.RandomText(textArr=surname),
                               houseId=self.appApi.appText.get('houseId'),
                               receptionPhone='1' + str(int(time.time())))
        self.appApi.ClientTask()
        if self.appApi.appText.get('total') >= 2:
            raise RuntimeError(self.appApi.appText.get('ApiXfpUrl'))
        self.appApi.Task_Visit_List(appointmentTime=self.flowPathText.get('time'))
        assert self.appApi.appText.get('visitStatusName') == '已完成', '状态异常'

    def advance_over_visit(self):
        """取消带看"""
        self.appApi.ClientTask(taskType='3')
        self.appApi.visit_info()
        self.appApi.visit_cancel()  # 取消带看
        self.appApi.ClientTask()
        if self.appApi.appText.get('total') > 1:
            print('取消带看，任务还存在')
            raise RuntimeError(self.appApi.appText.get('ApiXfpUrl'))
        self.appApi.ClientFollowList()
        assert (self.appApi.appText.get('followContent'))[:4] == '带看取消', '取消带看无跟进'

    def visit_status(self, status):
        """带看状态"""
        self.appApi.Task_Visit_List(appointmentTime=self.flowPathText.get('time'))
        if status == '进行中':
            assert self.appApi.appText.get('visitStatus') == '2', '状态异常'
            assert self.appApi.appText.get('visitStatusName') == '带看中', '状态异常'
        elif status == '已取消':
            assert self.appApi.appText.get('visitStatus') == '4', '状态异常'
        elif status == '已完成':
            assert self.appApi.appText.get('visitStatus') == '3', '状态异常'
        elif status == '已驳回':
            assert self.appApi.appText.get('visitAuditStatus') == '3', '状态异常'
            assert self.appApi.appText.get('visitAuditStatusName') == '已驳回', '状态异常'
            assert self.appApi.appText.get('visitStatus') == '4', '状态异常'
        elif status == '审核中':
            assert self.appApi.appText.get('visitAuditStatus') == '0', '状态异常'
            assert self.appApi.appText.get('visitAuditStatusName') == '进行中', '状态异常'
        elif status == '无需审核':
            assert self.appApi.appText.get('visitAuditStatus') == '6', '状态异常'
            assert self.appApi.appText.get('visitAuditStatusName') == '无需审核', '状态异常'
        elif status == '队长审核中':
            assert self.appApi.appText.get('visitAuditStatus') == '1', '状态异常'
            assert self.appApi.appText.get('visitAuditStatusName') == '队长审核中', '状态异常'
        elif status == '已同意':
            assert self.appApi.appText.get('visitAuditStatus') == '2', '状态异常'
            assert self.appApi.appText.get('visitAuditStatusName') == '已同意', '状态异常'
        elif status == '总监审核中':
            assert self.appApi.appText.get('visitAuditStatus') == '1', '状态异常'
            assert self.appApi.appText.get('visitAuditStatusName') == '总监审核中', '状态异常'
            assert self.appApi.appText.get('visitStatus') == '2', '状态异常'

    def suspend_follow(self):
        """暂缓跟进"""
        try:
            self.appApi.ClientTaskPause()
            while self.appApi.appText.get('data') == '该客户已被暂缓!':
                self.appApi.ClientFollowList()
                self.appApi.ClueFollowSave(followType='客户', taskEndTime=time.strftime("%Y-%m-%d") + ' 22:00:00')
                self.appApi.ClientFollowList()
                self.appApi.ClientTaskPause()
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.appApi.appText.get('ApiXfpUrl'))

    def apply_status(self, status, vlue=0, keyWord=None):
        dome = self.appApi.appText.get('clueId')
        self.appApi.follow_apply(vlue=vlue, keyWord=keyWord)
        if status == '申请中':
            assert self.appApi.appText.get('auditStatueApp') == 0, '状态异常'
            assert self.appApi.appText.get('auditStatueStr') == '申请中', '状态异常'
        elif status == '已同意':
            assert self.appApi.appText.get('auditStatueApp') == 1, '状态异常'
            assert self.appApi.appText.get('auditStatueStr') == '已同意', '状态异常'
        elif status == '已驳回':
            assert self.appApi.appText.get('auditStatueApp') == 2, '状态异常'
            assert self.appApi.appText.get('auditStatueStr') == '已驳回', '状态异常'

        assert self.appApi.appText.get('clueId') == dome, '跟进申请-无记录'

    def add_deal(self):
        """录入成交"""
        try:
            self.appApi.deal_List()
            dome = self.appApi.appText.get('total')
            self.client_list_non_null()
            if self.appApi.appText.get('code') != 200:
                self.clue_non_null()
                self.appApi.ClueInfo()
                self.appApi.phone_log(callee_num=self.appApi.appText.get('cluePhone'),
                                      is_own_call=0, talk_time=12000,
                                      call_time=time.strftime("%Y-%m-%d %H:%M:%S"))
                self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
                                           loanSituation='这个是贷款情况')
                self.appApi.ClientList()  # 客户列表
                self.appApi.client_info()
            self.appApi.visitProject_list()
            if self.appApi.appText.get('web_total') == 0:
                self.add_visit()
                self.accomplish_visit()
                self.appApi.visitProject_list()
            self.appApi.add_deal()  # 录入成交
            self.appApi.deal_List()
            assert dome != self.appApi.appText.get('total'), '录入成交总数不变？'
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.appApi.appText.get('ApiXfpUrl'))

    def add_deal_new(self):
        """录入成交"""
        self.client_list_non_null()
        # self.appApi.client_info()
        self.appApi.visitProject_list()
        self.appApi.add_deal()  # 录入成交

    def deal_status(self, status, keyWord):
        """成交状态"""
        dome = self.appApi.appText.get('clueId')
        self.appApi.deal_List(ApplyStatus=status, keyWord=keyWord)
        if status == '0' or status == 0:
            assert self.appApi.appText.get('transStatus') == '0', '状态异常'
        elif status == '1' or status == 1:
            assert self.appApi.appText.get('transStatus') == '1', '状态异常'
        elif status == '2' or status == 2:
            assert self.appApi.appText.get('transStatus') == '2', '状态异常'
        assert self.appApi.appText.get('clueId') == dome, '跟进申请-无记录'

    def first_phone_non_null(self):
        """首电不为空"""
        self.appApi.TodayClue(isFirst=0)
        if self.appApi.appText.get('Total') < 1:
            self.appApi.ClueSave(clueNickName=self.appApi.RandomText(textArr=surname),
                                 sourceId=self.appApi.appText.get('XSLY'),
                                 keyWords=self.appApi.appText.get('XSBQ'))
            self.appApi.TodayClue(isFirst=0)
        globals()['r.text'] = json.loads(json.dumps(self.appApi.appText.get('records')))
        while globals()['r.text'][0]['isFirst'] == '1':
            print('创建线索后首电 isFirst != 0')
            self.appApi.appText.set_map('clueId', globals()['r.text'][0]['clueId'])
            self.appApi.ExileSea()
            self.clue_non_null()
            self.appApi.TodayClue(isFirst=None)
            globals()['r.text'] = json.loads(json.dumps(self.appApi.appText.get('records')))
        self.appApi.appText.set_map('clueId', globals()['r.text'][0]['clueId'])
        self.appApi.ClueInfo()

    def clue_exile_sea(self):
        """线索流放公海"""
        self.appApi.ClueFollowList()
        self.appApi.ClueFollowSave(taskEndTime=time.strftime("%Y-%m-%d") + ' 22:00:00')
        time.sleep(1)
        self.appApi.ExileSea()

    def add_new_clue(self):
        """新增一条线索"""
        try:
            self.appApi.ClueSave(clueNickName=self.appApi.RandomText(textArr=surname),
                                 sourceId=self.appApi.appText.get('XSLY'),
                                 keyWords=self.appApi.appText.get('XSBQ'))
            # 在搜索列表进行查找
            globals()['CluePhone'] = self.appApi.appText.get('cluePhone')
            self.appApi.ClueList(keyWord=(self.appApi.appText.get('cluePhone')))
            assert self.appApi.appText.get('cluePhone') == globals()['CluePhone'], '新增线索列表异常'
            """今日上户上进行查看"""
            self.appApi.TodayClue()
            dome1 = 0
            globals()['r.text'] = json.loads(json.dumps(self.appApi.appText.get('records')))
            while globals()['r.text'][dome1]['clueNoHiddenPhone'] != self.appApi.appText.get('cluePhone'):
                # print(dome1)
                dome1 = dome1 + 1
            assert globals()['r.text'][dome1]['isFirst'] == '0', '新增线索是未首电'
            time.sleep(1)
        except BaseException as e:
            print("错误，错误原因：%s" % e)
            raise RuntimeError(self.appApi.appText.get('ApiXfpUrl'))

    def get_label(self, labelNo, labelName, newlabelName):
        """查询标签"""
        self.appApi.GetLabelList(labelNo=labelNo, labelName=newlabelName)
        if self.appApi.appText.get('data') == []:
            self.webApi.add_label(labelName=labelName, labelId=0, pid=0)
            self.appApi.GetLabelList(labelNo=labelNo, labelName=newlabelName)
        if self.appApi.appText.get('labelId') is not None:
            pass  # 存在标签---不创建
        else:
            self.webApi.add_label(labelName=newlabelName, labelId=self.appApi.appText.get('LabelId'),
                                  pid=self.appApi.appText.get('LabelId'))



