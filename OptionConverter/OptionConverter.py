# -*- coding:UTF-8 -*-

"""
Author : zhaojie 
Created at: 2021-04-23
Copyright (c) 2008—2021 Free Technologies Co., Ltd. All rights reserved.
"""

import sys
import hashlib
import os
import tkinter.messagebox
import base64
from tkinter import *
from icon import img

# ********* The Build Parameters Area Start >> *********

# 常量区
TITLE = 'DHCP_IPOX SDV KIT'
AUTH_VER = 'Author:z00574552 ver.2.0'
WARNING_MID = '*小软件未对参数做边界检查，请确保输入字符为ASCII表所支持的字符，否则程序可能发生异常.'
COPY_INFO = '已复制到剪贴板'

# Build Info : pyinstaller -F(w) -i hw_icon.ico OptionConverter.py


# ico = "D:\\SourceCode\\Python\\VSCode\\hw_icon.ico"
# logo = "D:\\SourceCode\\Python\\VSCode\\hw_full.png"

# >>>打包图标文件解决方案1 [base64转码方案],仅打包时放开
# 将图标用base64编码方式打包成py文件
# 打开图标文件
# open_icon = open("hw_icon.ico", "rb")
# 读取文件并转为base64编码
# b64str = base64.b64encode(open_icon.read())
# 关闭文件
# open_icon.close()
# write_data = "img=%s" % b64str
# f = open("icon.py", "w+")
# f.write(write_data)
# f.close()
# <<<打包图标文件解决方案1

# >>>打包图标文件解决方案2 [SPEC生成资源文件方式],废弃
# 生成资源文件目录访问路径
# def resource_path(relative_path):
#   if getattr(sys, 'frozen', False):  # 是否Bundle Resource
#        base_path = sys._MEIPASS
#    else:
#        base_path = os.path.abspath(".")
#    return os.path.join(base_path, relative_path)
# <<<打包图标文件解决方案2 [SPEC生成资源文件方式]

# hw_icon = resource_path(os.path.join("res", "hw_icon.ico"))
# ico = hw_icon
# hw_full = resource_path(os.path.join("res", "hw_full.png"))
# logo = hw_full

# ********* The Build Parameters Area End << *********


class Converter(object):
    # 转换内核
    # 定义2个静态方法，不用将类实例化就可调用
    @staticmethod
    def str_to_ascii_hex(s):
        list_h = []
        for c in s:
            list_h.append(str(hex(ord(c))[2:]))
        return ''.join(list_h)

    @staticmethod
    def ascii_hex_to_str(h):
        list_s = []
        for i in range(0, len(h), 2):
            list_s.append(chr(int(h[i:i+2], 16)))
        return ''.join(list_s)


class MD5(object):
    # MD5生成内核
    @staticmethod
    def md5_generator(source):
        creator = hashlib.md5()
        creator.update(source.encode(encoding='utf8'))
        return creator.hexdigest()


def warner(dis_lab, info, color):
    dis_lab.config(text=info)
    dis_lab.config(fg=color)


def gen_md5(obj_source_lab, obj_target_lab):
    # 清空MD5输入框
    obj_target_lab.delete(0, END)
    # 调用接口，写入结果
    obj_target_lab.insert(0, MD5.md5_generator(obj_source_lab.get()))


def chk_md5(obj_source_lab_str, obj_source_lab_md5, obj_res_lab):

    if obj_source_lab_str.get() == '':
        # 检查字符串输入框
        warner(obj_res_lab, '字符串为空', 'red')
    elif len(obj_source_lab_md5.get()) != 32:
        # 检查MD5合法性
        warner(obj_res_lab, 'MD5码长度非32位HEX', 'red')
    else:
        if MD5.md5_generator(obj_source_lab_str.get()) == obj_source_lab_md5.get():
            warner(obj_res_lab, 'Check Success!', 'green')
        else:
            warner(obj_res_lab, 'Check Fail!', 'red')


def calc_byte_len(obj_source_lab, obj_target_lab):
    # 置长度框可写
    obj_target_lab.configure(state='normal')
    # 初始化写入文本框
    obj_target_lab.delete(0, END)
    # 将字节长度写入长度框
    obj_target_lab.insert(0, len(obj_source_lab.get()))
    # 置长度框只读
    obj_target_lab.configure(state='readonly')


def convert_str_ascii(obj_source_lab, obj_target_lab, obj_len_lab):
    # 初始化非输入文本框
    obj_target_lab.delete(0, END)
    # 调用接口，写入结果
    obj_target_lab.insert(0, Converter.str_to_ascii_hex(obj_source_lab.get()))
    # 写入长度
    calc_byte_len(obj_source_lab, obj_len_lab)


def convert_ascii_str(obj_source_lab, obj_target_lab, obj_len_lab):
    # 初始化非输入文本框
    obj_target_lab.delete(0, END)
    # 调用接口，写入结果
    obj_target_lab.insert(0, Converter.ascii_hex_to_str(obj_source_lab.get()))
    # 写入长度
    calc_byte_len(obj_target_lab, obj_len_lab)


def cp_from_entry(obj_tx):
    # DebugMark:访问剪贴板时先清空剪贴板，否则多次访问会无限扩展追加
    root.clipboard_clear()
    root.clipboard_append(obj_tx.get())
    tkinter.messagebox.showinfo(title='clipboard', message=COPY_INFO)


def gen_option82(obj_source_lab1, obj_source_lab2, obj_target_lab, obj_len_lab):
    # 置总长度框框可写
    obj_len_lab.configure(state='normal')
    # 初始化非输入文本框
    obj_target_lab.delete(0, END)
    obj_len_lab.delete(0, END)
    if len(obj_source_lab1.get()) > 255 or len(obj_source_lab2.get()) > 255:
        # 子option长度大于255会导致错误
        tkinter.messagebox.showinfo(title='Error', message='子option长度超过255')
    else:
        # 调用转换核转换并计算长度连接后输出
        # 转换和计算sub1
        hex_sub1 = Converter.str_to_ascii_hex(obj_source_lab1.get())
        len_sub1 = "%02x" % len(obj_source_lab1.get())
        # 转换和计算sub2
        hex_sub2 = Converter.str_to_ascii_hex(obj_source_lab2.get())
        len_sub2 = "%02x" % len(obj_source_lab2.get())
        # 连接
        if obj_source_lab1.get() == '':
            # sub1未输入
            tkinter.messagebox.showinfo(title='Error', message='至少输入1个子option')
            ret = 'Err'
        else:
            # sub1输入
            if obj_source_lab2.get() == '':
                # sub2未输入
                ret = '01' + len_sub1 + hex_sub1
            else:
                # sub1 sub2都输入
                ret = '01' + len_sub1 + hex_sub1 + '02' + len_sub2 + hex_sub2

        # 计算总长度并写入总长度框
        obj_target_lab.insert(0, ret)
        obj_len_lab.insert(0, int(len(ret) / 2))

        # 置长度框只读
        obj_len_lab.configure(state='readonly')


def clear_tx(*list_tx):
    for tx in list_tx:
        if tx.cget('state') == 'readonly':
            tx.configure(state='normal')
            tx.delete(0, END)
            tx.configure(state='readonly')
        else:
            tx.delete(0, END)


# ********* The GUI Layout Area *********

def center_window(w=300, h=200):
    # 定义窗口位置
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    root.geometry("%dx%d+%d+%d" % (w, h, x, y))


# 创建窗口
root = Tk()
root.title(TITLE)

# 创建图标
# root.iconbitmap(ico)


# >>>打包图标文件解决方案1
tmp = open('tmp.ico', 'wb+')
tmp.write(base64.b64decode(img))
tmp.close()
root.iconbitmap('tmp.ico')
os.remove('tmp.ico')
# <<<打包图标文件解决方案1


# 创建窗口
center_window(600, 500)
root.resizable(0, 0)
xPos = 70

# option字符串
LB_OptionStr = Label(root, text='Option 字符串 ', font='("宋体",20)')
LB_OptionStr.place(x=10, y=20)
# 字符串输入框
TX_OptionStr = Entry(root, state='normal', width=20, font=("Courier New", 12))
TX_OptionStr.place(x=150, y=20)
# 字符串复制按钮
BT_CopyStr = Button(root, activebackground='BLUE', text='复制', command=lambda: cp_from_entry(TX_OptionStr), width=10)
BT_CopyStr.place(x=400 + xPos, y=18)


# ASCII码
LB_OptionAsc = Label(root, text='Option ASCII', font='("宋体",20)')
LB_OptionAsc.place(x=10, y=60)
# ASCII输入输出框
TX_OptionAsc = Entry(root, state='normal', width=20, font=("Courier New", 12))
TX_OptionAsc.place(x=150, y=60)
# ASCII码复制按钮
BT_CopyAsc = Button(root, activebackground='BLUE', text='复制', command=lambda: cp_from_entry(TX_OptionAsc), width=10)
BT_CopyAsc.place(x=400 + xPos, y=58)


# option字节长度
LB_OptionLen = Label(root, text='Option 字节长度', font='("宋体",20)')
LB_OptionLen.place(x=10, y=100)
# 字节长度输出框
TX_OptionLen = Entry(root, width=20, state='readonly', font=("Courier New", 12))
TX_OptionLen.place(x=150, y=100)


# 字符串翻译按钮
BT_Conv_Str_to_Asc = Button(root, activebackground='BLUE', text='转ASCII', command=lambda: convert_str_ascii(TX_OptionStr, TX_OptionAsc, TX_OptionLen), width=10)
BT_Conv_Str_to_Asc.place(x=310 + xPos, y=18)

# ASCII码翻译按钮
BT_Conv_Asc_to_Str = Button(root, activebackground='BLUE', text='转字符串', command=lambda: convert_ascii_str(TX_OptionAsc, TX_OptionStr, TX_OptionLen), width=10)
BT_Conv_Asc_to_Str.place(x=310 + xPos, y=58)

# 清除按钮
BT_Clear = Button(root, activebackground='BLUE', text='清除', command=lambda: clear_tx(TX_OptionStr, TX_OptionAsc, TX_OptionLen), width=10)
BT_Clear.place(x=310 + xPos, y=98)


# Op82_Sub1
LB_OptionSub1 = Label(root, text='Option82_sub1 ', font='("宋体",20)')
LB_OptionSub1.place(x=10, y=140)
TX_OptionSub1 = Entry(root, width=20, font=("Courier New", 12))
TX_OptionSub1.place(x=150, y=140)
# Op82_Sub2
LB_OptionSub2 = Label(root, text='Option82_sub2 ', font='("宋体",20)')
LB_OptionSub2.place(x=10, y=180)
TX_OptionSub2 = Entry(root, width=20, font=("Courier New", 12))
TX_OptionSub2.place(x=150, y=180)
# option82串
LB_OptionAppStr = Label(root, text='Option82 串 ', font='("宋体",20)')
LB_OptionAppStr.place(x=10, y=220)
TX_OptionAppStr = Entry(root, width=20, font=("Courier New", 12))
TX_OptionAppStr.place(x=150, y=220)
# option82总长度
LB_OptionAppLen = Label(root, text='Option82 总字节长 ', font='("宋体",20)')
LB_OptionAppLen.place(x=10, y=260)
TX_OptionAppLen = Entry(root, width=20, state='readonly', font=("Courier New", 12))
TX_OptionAppLen.place(x=150, y=260)
# 生成option串按钮
BT_GenOption = Button(root, activebackground='BLUE', text='生成Option串', command=lambda: gen_option82(TX_OptionSub1, TX_OptionSub2, TX_OptionAppStr, TX_OptionAppLen), width=10)
BT_GenOption.place(x=310 + xPos, y=210)

# MD5原始字符串
LB_MD5Str = Label(root, text='原始字符串 ', font=("宋体", 12))
LB_MD5Str.place(x=10, y=300)
# MD5字符串输入框
TX_MD5Str = Entry(root, width=20, font=("Courier New", 12))
TX_MD5Str.place(x=150, y=300)
# MD5码
LB_MD5Code = Label(root, text='MD5码(HEX)', font=("宋体", 12))
LB_MD5Code.place(x=10, y=340)
# MD5码生成、输入框
TX_MD5Code = Entry(root, width=32, font=("Courier New", 12))
TX_MD5Code.place(x=150, y=340)
# 输出label
# res = StringVar()
# res.set("*")
LB_CheckRes = Label(root, font=("宋体", 12))
LB_CheckRes.place(x=200, y=380)

# 生成MD5按钮
BT_GenMD5Code = Button(root, activebackground='BLUE', text='生成MD5', command=lambda: gen_md5(TX_MD5Str, TX_MD5Code), width=10)
BT_GenMD5Code.place(x=300 + xPos, y=300)


# 校验MD5按钮
BT_GenMD5 = Button(root, activebackground='BLUE', text='校验MD5', command=lambda: chk_md5(TX_MD5Str, TX_MD5Code, LB_CheckRes), width=10)
BT_GenMD5.place(x=390 + xPos, y=300)


# 软件底部logo布局
auth = Label(root, text=AUTH_VER)
auth.pack(side=BOTTOM, anchor='s')
# logo = PhotoImage(file=logo)
# imgLabel = Label(root, image=logo)
# imgLabel.pack(side=BOTTOM, anchor='s')


warn = Label(root, wraplength=400, text=WARNING_MID, font='("宋体",20)', fg="#FF0000")
warn.place(x=30, y=440)


# 进入消息循环
root.mainloop()
