VerbalTrick = ['上班#', '拓展联盟商#', '案场跟进#', '回访联盟商#', '踩盘#', '下班#', '联盟商培训#']
VerbalTrickType = ['上班', '拓展联盟商', '案场跟进', '回访联盟商', '踩盘', '下班', '联盟商培训']
VerbalTrickType1 = ['上班1', '拓展联盟商1', '案场跟进1', '回访联盟商1', '踩盘', '下班', '联盟商培训']
# for index in range(len(VerbalTrick)):
#     # print("下标", index)
#     # print("对应值", VerbalTrick[index])
#     for index1 in range(len(VerbalTrickType)):
#         if index == index1:
#             print("对应值", VerbalTrick[index], VerbalTrickType[index1])


for x, y, z in zip(VerbalTrick, VerbalTrickType, VerbalTrickType1):
    print(x, y, z)
