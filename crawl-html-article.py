import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import random

class Crawl_Paper():
    def __init__(self):
        print('...准备爬虫...')
    
    def write_to_file(self, title, content):
        with open(title+'.txt', 'a', encoding='utf-8') as f:
            f.write()

    def send_key_words(self, browser, journal_name): #仅起到一个搜索功能，可修改搜索内容
        browser.get("https://www.cnki.net")
        print('...进入知网...')
        ele_input1 = browser.find_element(By.XPATH, '//*[@id="DBFieldBox"]/div[1]/i')
        ele_input1.click()
        browser.implicitly_wait(2)
        ele_input2 = browser.find_element(By.XPATH, '//li[@value="LY"]')
        ele_input2.click()
        
        browser.implicitly_wait(12)
        print('...正在搜索 '+ journal_name +' 相关的论文...')
        ele_search_paper_input = browser.find_element(By.XPATH, '//input[@id="txt_SearchText"]')
        ele_search_paper_input.send_keys(journal_name) # 这里可以修改想要搜索的内容
        browser.implicitly_wait(3)
        ele_search_paper_confirm = browser.find_element(By.XPATH, '//input[@type="button"]')
        ele_search_paper_confirm.click()
        print('...搜索成功...')
        return browser, journal_name

    def get_documents(self, browser, journal_name): #得到论文库
        time.sleep(random.randint(4,5))
        ele_all_papers = browser.find_elements(By.XPATH, '//td[@class="name"]/a[@class="fz14"]') #找到所有目录的element
        papers_list = [] #一页里所有论文的链接存进去
        verify_box_locator = (By.CLASS_NAME, "verifybox")  

        for ele_all_paper in ele_all_papers:
            papers_list.append(ele_all_paper.get_attribute("href"))
        browser.execute_script("window.open('about:blank', '_blank');")
        handles = browser.window_handles
        browser.switch_to.window(handles[-1])

        for paper in papers_list: #一页的论文
            browser.get(paper)
            browser.implicitly_wait(random.randint(9,13))
            try:
                browser.find_element(verify_box_locator)
                # 循环等待直到验证码元素消失
                while True:
                    # 检查验证码元素是否存在
                    verify_box = browser.find_element(verify_box_locator)
                    if len(verify_box) > 0:
                        # 等待一段时间后再进行下一次检查
                        time.sleep(300)
                    else:
                        # 如果验证码元素不存在，跳出循环
                        break
            except:
                print("没有验证码")
                pass

            try:
                ele_html_btn = browser.find_element(By.XPATH, '//li[@class="btn-html"]/a[@target="_blank"]')
                ele_html_btn.click()
                browser.implicitly_wait(6)
                handles = browser.window_handles
                browser.switch_to.window(handles[-1])
                current_url = browser.current_url
                # print(current_url)
                browser.get(current_url)
                browser.implicitly_wait(10)
                try:
                    ele_top_title = browser.find_element(By.XPATH, '//h1[@class="title"]/span[@class="vm"]')
                    top_title = ele_top_title.text
                    print(top_title)
                    texts = browser.find_elements(By.XPATH, '//div[@class="p1"]/p')
                    print("Texts have been found!")
                    with open('./papers_dir/'+ journal_name + "/"+ top_title +'.txt', 'a', encoding='utf-8') as f: # 存入文件夹的路径
                        for txt in texts:
                            # print(txt.text)
                            f.write(txt.text+"\n")
                except:
                    print("找不到正文")
                browser.implicitly_wait(5)
            except:
                continue
    
        try:   # 先跳转到目录页
            handles = browser.window_handles
            browser.switch_to.window(handles[0])
            browser.implicitly_wait(10)
            page_next = browser.find_element(By.XPATH, '//div[@class="pages"]/a[@id="PageNext"]')
            print(page_next.text)
            page_next.click()
            # page_next.send_key(Keys.LEFT)
            print("跳转成功！")
            self.get_documents(browser, journal_name)
        except:
            print("已到达目录末尾")

    def main(self):
        browser = webdriver.Chrome()
        browser.maximize_window()
        journal_names = '（模式识别与人工智能）' # 期刊名称
        browser, journal_name = self.send_key_words(browser, journal_names)
        journal_name = journal_name.replace('（', '').replace('）', '') # 去掉括号
        print(journal_name)
        time.sleep(random.randint(5,10))
        # page_next = browser.find_element(By.XPATH, '//div[@class="pages"]/a[@id="page4"]')
        # page_next.click()
        self.get_documents(browser, journal_name)

if __name__ == '__main__':
    crawler_Paper = Crawl_Paper()
    crawler_Paper.main()
