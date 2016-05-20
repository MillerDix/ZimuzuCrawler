# !usr/bin/env python3
# -- coding:utf-8 --

import urllib.request
import re
import threading
import time
import socket
import os


# 调度
class SpiderMan:

    def __init__(self, root_url):
        # 入口路径
        self.root_url = root_url
        # 任务list
        self.task_list = []
        # 历史list
        self.done_list = []
        # 子线程list
        self.slaves_list = []
        # 图片list
        self.img_list = []
        self.downloader_list = []
        self.flag = True

        response = urllib.request.urlopen(self.root_url).read().decode()
        # 正则处理并去重
        temp = list(set(re.findall(r'href="(http://www.ugirls.*?)"', response)))
        # temp = list(map(lambda x: self.root_url+x, temp))
        # 找到图片
        temp_img = list(set(re.findall(r'<img.+?="(http://.+?)"', response)))
        self.img_list = temp_img
        print("找到图片:{}个".format(self.img_list.__len__()))
        # for i in self.img_list:
        #     print(i)
        self.task_list = temp

        print("共有任务{}个".format(self.task_list.__len__()))
        self.done_list.append(self.root_url)
        # for i in self.task_list:
        #     print(i)

        # t = threading.Thread(self.downloader.set_new_image(self.img_list.pop(0)))
        # t.start()
    def begingtask(self):
        # 创建slave运行
        # slave = WorkingSlaves(self.root_url)
        # slave.start()
        # self.done_list.append(self.root_url)

        while self.task_list.__len__() > 0:

            # 图片下载处理
            if self.img_list.__len__() > 0 and self.downloader_list.__len__() < 3:
                downloader = ImageDownloader()
                self.downloader_list.append(downloader)
                downloader.url = self.img_list.pop(0)
                downloader.start()

            else:
                for item in self.downloader_list:
                    if item.download_finish:
                        self.downloader_list.remove(item)
                # self.downloader.set_new_image(self.img_list.pop(0))

            # 任务分发处理
            if self.slaves_list.__len__() < 5:
                # 取出第一个任务
                task_next = self.task_list.pop(0)
                print("进行任务:{}".format(task_next))
                if task_next not in self.done_list:
                    self.done_list.append(task_next)
                    print("已完成--------{}个".format(self.done_list.__len__()))
                    slave = WorkingSlaves(task_next)
                    slave.start()
                    self.slaves_list.append(slave)
            else:
                for sl in self.slaves_list:
                    if sl.finish:
                        print("子线程找到url:{}个".format(sl.found_list.__len__()))
                        print("子线程找到img:{}个".format(sl.found_img_list.__len__()))
                        self.task_list.extend(sl.found_list)
                        self.task_list = list(set(self.task_list))

                        self.img_list.extend(sl.found_img_list)
                        self.img_list = list(set(self.img_list))
                        print(">>>>>>>>>>>>>>>当前还有任务:{}个".format(self.task_list.__len__()))
                        print(">>>>>>>>>>>>>>>已找到图片:{}个".format(self.img_list.__len__()))
                        self.slaves_list.remove(sl)
                    else:
                        continue
        # 退出机制
        # for item in self.slaves_list:
        #     if not item.finish:
        #         break


class ImageDownloader(threading.Thread):

    def __init__(self):
        super(ImageDownloader, self).__init__()
        self.url = ''
        self.download_finish = False
        self.filePath = '/Users/MillerD/Desktop/未命名文件夹/images/'
        # self.count = count
        if not os.path.exists(self.filePath):
            os.mkdir(self.filePath)
        else:
            pass

    def run(self):
        time.sleep(1)
        # 下载
        try:
            # print("-----------------正在下载第{}张图片".format(self.count))
            urllib.request.urlretrieve(self.url, self.filePath + self.url.replace('/', '_'))
        except Exception as e:
            print("图片下载错误:{}".format(e))
        finally:
            self.download_finish = True


# 爬虫处理
class WorkingSlaves(threading.Thread):

    def __init__(self, url):
        super(WorkingSlaves, self).__init__()
        # 任务地址
        self.url = url
        # 找到的地址list
        self.found_list = []
        # 图片list
        self.found_img_list = []
        # 完成标记
        self.finish = False
        global enter_url

    def run(self):
        # 睡眠
        try:
            time.sleep(5)
            # 收到文本
            response = urllib.request.urlopen(self.url).read().decode()
            # 正则处理并去重
            temp = list(set(re.findall(r'href="(http://www.ugirls.*?)"', response)))
            temp_img = list(set(re.findall(r'<img.+?="(http://.+?)"', response)))
            # 拼接根路径
            # self.found_list = list(map(lambda x: enter_url+x, temp))
            self.found_list = temp
            self.found_img_list = temp_img
            self.finish = True
            # 输出信息
        except Exception as e:
            print("发生错误:{}".format(e))
            self.found_list = []
            self.found_img_list = []
        finally:
            self.finish = True

    # def __init__(self, image):
    #     super(ImageDownloader, self).__init__()
    #     self.images_list = image
    #     self.download_finish = False
    #
    # def assignNewTasks(self, images):
    #     self.images_list = images
    #
    # def getNewTasks(self):
    #     return self.images_list
    #
    # def run(self):
    #     while True:
    #         #下载图片
    #         if self.images_list.__len__() > 0:
    #             for item in self.images_list:
    #                 try:
    #                     urllib.request.urlretrieve(item)
    #                 except Exception as e:
    #                     print("图片下载错误{}".format(e))
    #                     continue


socket.setdefaulttimeout(5)
enter_url = r'http://www.ugirls.com'
spider = SpiderMan(enter_url)
spider.begingtask()
print("nice to meet you")