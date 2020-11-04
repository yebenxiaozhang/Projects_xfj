# -*- coding: utf-8 -*-
# @Time    : 2019/12/24 9:57
# @Author  : 潘师傅
# @File    : RandomText.py

import random


def randomText(textArr):

	length = len(textArr)
	if length < 1:
		return ''
	if length == 1:
		return str(textArr[0])
	randomNumber = random.randint(0,length-1)
	return str(textArr[randomNumber])
