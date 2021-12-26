#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
import hashlib
import time
import numpy as np 
import copy
from collections import OrderedDict

LOG_LINE_NUM = 0

class MY_GUI():
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name
        self.ranks=["A", "B", "C", "D", "E"]
        self.rank_num=len(self.ranks)
        self.names=["科目\评价等级", "分数下限", "分数上限"]+self.ranks
        self.subjects=["主题内涵","目的地","行程安排","旅游六要素","格式"]

    #设置窗口
    def set_init_window(self):
        self.init_window_name.title("成绩计算小程序")          #窗口名
        #self.init_window_name.geometry('320x160+10+10')      #290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window_name.geometry('600x320+100+100')
        #self.init_window_name["bg"] = "pink"                 #窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887
        #self.init_window_name.attributes("-alpha",0.9)       #虚化，值越小虚化程度越高

        # 标签
        self.label_ranks=[]
        for i in range(len(self.names)):
            self.label_ranks.append(Label(self.init_window_name, text=self.names[i])) 
            self.label_ranks[i].grid(row=0, column=i )
        del i

        self.scores = Label(self.init_window_name, text="分数")
        self.scores.grid(row=0, column=len(self.names) )

        self.subjects_txt=[]
        for i in range(len(self.subjects)):
            # self.subject1 = Label(self.init_window_name, text=self.subjects[i])
            # self.subject1.grid(row=1+i, column=0 )
            self.subjects_txt.append(Entry(self.init_window_name, width=7))
            self.subjects_txt[i].grid(row=1+i, column=0, rowspan=1, columnspan=1)
        del i

        #分数上下限文本框
        self.score_subject_up_down=[]
        for i in range(len(self.subjects)):
            self.score_subject_up_down.append(Entry(self.init_window_name, width=5))  #, height=1
            self.score_subject_up_down[2*i].grid(row=1+i, column=1, rowspan=1, columnspan=1)  # 
            self.score_subject_up_down.append(Entry(self.init_window_name, width=5))  # , height=1
            self.score_subject_up_down[2*i+1].grid(row=1+i, column=2, rowspan=1, columnspan=1)

        # 等级
        self.rank_subjects_whole=[]
        self.rank_vars=[]
        for i in range(len(self.subjects)):
            self.rank_vars.append(StringVar())
            self.rank_vars[i].set(" ")
            self.rank_subjects=[]
            for j, mode in enumerate(self.ranks):
                self.rank_subjects.append(Radiobutton(self.init_window_name, text=mode, variable=self.rank_vars[i], value=mode))
                self.rank_subjects[j].grid(row=1+i, column=3+j)
            self.rank_subjects_whole.append(self.rank_subjects)
        del i

        self.score_subjects=[]
        for i in range(len(self.subjects)):
            self.score_subjects.append(Text(self.init_window_name, width=5, height=1))   #原始数据录入框
            self.score_subjects[i].grid(row=1+i, column=8, rowspan=1, columnspan=1)

        self.score_total = Text(self.init_window_name, width=5, height=1)  #处理结果展示
        self.score_total.grid(row=6, column=8, rowspan=1, columnspan=1)
        self.log_data_Text = Text(self.init_window_name, width=66, height=9)  # 日志框
        self.log_data_Text.grid(row=13, column=0, columnspan=10)

        #按钮
        self.button_set = Button(self.init_window_name, text="设定科目及分数", bg="lightblue", width=10, command=self.set_par)  # 调用内部方法  加()为直接调用
        self.button_set.grid(row=6, column=1)
        self.button_cal = Button(self.init_window_name, text="计算成绩", bg="lightblue", width=10, command=self.compute_score)  # 调用内部方法  加()为直接调用
        self.button_cal.grid(row=6, column=4)

    # set parameter
    def set_par(self):
        self.object_score_list=[15,15,30,30,10]
        self.object_score_down_list=[]
        for i in range(len(self.subjects)):
            score_down_str = self.score_subject_up_down[2*i].get()
            score_up_str = self.score_subject_up_down[2*i+1].get()

            if score_down_str != '':
                self.object_score_down_list.append(int(score_down_str))
            else:
                self.object_score_down_list.append(0)
            
            if score_up_str != '':
                self.object_score_list[i]=int(score_up_str)
            
            subject_txt = self.subjects_txt[i].get()
            if subject_txt != '':
                self.subjects[i]=subject_txt

    #功能函数
    def compute_score(self):
        try:
            scores_dict=OrderedDict()
            object_score_list2=[]
            for object_score_down, object_score in zip(self.object_score_down_list, self.object_score_list):
                assert object_score//self.rank_num, "rank_num 不能整除"
                tmp = np.arange(object_score, object_score_down, -1).reshape(self.rank_num, -1)
                
                for index, grade in enumerate(self.ranks):
                    scores_dict[grade]=tmp[index]
                object_score_list2.append(copy.deepcopy(scores_dict))
                scores_dict.clear()

            del index, tmp
            
            input_grades=[]
            for subject_rank in self.rank_vars:
                input_grades.append(subject_rank.get())

            out_score_list=[]
            for index, input_grade in enumerate(input_grades):
                tmp = object_score_list2[index][input_grade]
                i = np.random.randint(0, len(tmp), 1)
                out_score_list.append(tmp[int(i)])
                self.score_subjects[index].delete(1.0,END)
                self.score_subjects[index].insert(1.0,tmp[int(i)])

            self.score_total.delete(1.0,END)
            self.score_total.insert(1.0,sum(out_score_list))
            self.write_log_to_Text(
                "INFO:\n{0}：{1}分，{2}：{3}分，{4}：{5}分，{6}：{7}分，{8}：{9}分，总分：{10}分".format(
                    self.subjects[0], out_score_list[0],
                    self.subjects[1], out_score_list[1],
                    self.subjects[2], out_score_list[2],
                    self.subjects[3], out_score_list[3],
                    self.subjects[4], out_score_list[4],
                    sum(out_score_list)
                )
            )
        except:
            self.score_total.delete(1.0,END)
            self.score_total.insert(1.0,"字符串转MD5失败")

    #获取当前时间
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return current_time

    #日志动态打印
    def write_log_to_Text(self,logmsg):
        global LOG_LINE_NUM
        current_time = self.get_current_time()
        logmsg_in = str(current_time) +" " + str(logmsg) + "\n"      #换行
        if LOG_LINE_NUM <= 7:
            self.log_data_Text.insert(END, logmsg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.log_data_Text.delete(1.0,2.0)
            self.log_data_Text.insert(END, logmsg_in)


def gui_start():
    init_window = Tk()              #实例化出一个父窗口
    ZMJ_PORTAL = MY_GUI(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()

    init_window.mainloop()          #父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


gui_start()