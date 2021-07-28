import asyncio
import datetime
import pickle
import re
import time

from selenium import webdriver

import config


class Spider(object):
    def __init__(self, baseurl: str, page_length: int = 0) -> None:
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
        self.pageLength = int(re.search("共(\d+)页", self.driver.find_element_by_id("managerList_info").text).group(
            1)) if not page_length else page_length
        self.datalist = []

        self.loop = asyncio.get_event_loop()

    def browse(self) -> None:
        """
        模拟用户浏览界面行为，爬取所有数据
        """

        index_page_handle = self.driver.window_handles[0]
        tasks = []
        startTime = datetime.datetime.now()

        for page in range(self.pageLength):

            self.driver.switch_to.window(index_page_handle)
            name_a = self.driver.find_element_by_id("managerList").find_elements_by_tag_name("a")

            for index, a in enumerate(name_a):
                a.click()
                new_page_handle = self.driver.window_handles[-1]
                task = self._getInfo(new_page_handle)
                tasks.append(asyncio.ensure_future(task))

            self.driver.find_element_by_class_name("next").click()
            # time.sleep(0.5) 新窗口会在等待子窗口内容提取中加载完毕
            self.loop.run_until_complete(asyncio.wait(tasks))

            print(f"\rPage {page + 1} \ {self.pageLength}",end="",flush=True)

        endTime = datetime.datetime.now()
        print(f"Total time cost: {(endTime-startTime).seconds} s")


    async def _getInfo(self, handle: str) -> None:
        """
        爬取内容页面数据
        :param handle: 页面句柄
        """
        await asyncio.sleep(1)
        try:

            self.driver.switch_to.window(handle)
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

        except Exception as e:
            print(e)

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
    spider = Spider(config.BASE_URL, 10)
    spider.browse()
    spider.save_cache(config.CATCH_PATH)
    spider.close()
