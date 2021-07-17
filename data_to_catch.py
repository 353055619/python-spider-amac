"""
Description: 爬取数据写入缓存
Version: 1.0
Author: 魏苏航
email: godw2017@163.com
"""
import pickle
import re
import time

from selenium import webdriver

import config


class Spider(object):
    def __init__(self, baseurl):
        """
        初始化ChromeDriver、httpRequest
        进入主页面
        """
        print("Initialize...")

        self.driver = webdriver.Chrome()
        self.driver.get(baseurl)
        self.driver.maximize_window()
        time.sleep(5)
        self.driver.find_element_by_class_name("layui-layer-btn0").click()
        self.driver.refresh()  # 刷新保证获取td中的数据
        time.sleep(1)
        # 获取页面长度
        self.pageLength = int(re.search("共(\d+)页", self.driver.find_element_by_id("managerList_info").text).group(1))
        self.datalist = []

    def browse(self):
        """
        模拟用户浏览界面行为，爬取所有数据
        """
        print("Browse...")
        for i in range(self.pageLength):

            name_a = self.driver.find_element_by_id("managerList").find_elements_by_tag_name("a")

            for index, a in enumerate(name_a):
                try:
                    a.click()

                    handles = self.driver.window_handles
                    self.driver.switch_to.window(handles[1])
                    self.driver.implicitly_wait(1)  # 等待界面加载

                    fund_info = self.driver.find_element_by_class_name("section").text

                    nameRes = re.search("基金管理人全称\(中文\)\s?(.*)", fund_info)
                    registerDateRes = re.search("登记时间\s?(.*)", fund_info)
                    okRes = re.search("是否为符合提供投资建议条件的第三方机构\s?(.*)", fund_info)
                    scaleRes = re.search("管理规模区间\s?(.*)", fund_info)

                    name = nameRes.group(1) if nameRes else ""
                    registerDate = registerDateRes.group(1) if registerDateRes else ""
                    ok = okRes.group(1) if okRes else ""
                    scale = scaleRes.group(1) if scaleRes else ""

                    data = {
                        "name": name,
                        "registerDate": registerDate,
                        "ok": ok,
                        "scale": scale
                    }
                    self.datalist.append(data)

                    self.driver.close()
                    self.driver.switch_to.window(handles[0])

                    print(f"\rPage {i + 1} \ {self.pageLength}: line {index + 1} \ {len(name_a)}", end="", flush=True)
                except Exception as e:
                    print(e)
            self.driver.find_element_by_class_name("next").click()
            time.sleep(0.5)  # 等待界面加载

        print("Done!")

    def save_cache(self, path: str):
        """
        序列化爬取的的数据
        :param path: 存储路径
        """
        print("Saving to cache...")
        with open(path, "wb+") as f:
            pickle.dump(self.datalist, f)

    def close(self):
        self.driver.quit()


if __name__ == '__main__':
    spider = Spider(config.BASE_URL)
    spider.browse()
    spider.save_cache(config.CATCH_PATH)
    spider.close()
