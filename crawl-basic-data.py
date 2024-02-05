import time
from selenium import webdriver
from tqdm import tqdm
import random
from selenium.webdriver.common.by import By

class Crawler_Paper(object):
    def __init__(self):
        print('...准备爬虫...')
    
    def write_to_file(self,content, send_key_word):
        with open('./paper_basic_data/' + send_key_word + '.txt', 'a', encoding='utf-8') as f:
            f.write(content)

    def crawler_begin(self, browser, send_key_word):
        browser.get("https://www.cnki.net")
        print('...进入知网...')
        time.sleep(10)
        ele_input1 = browser.find_element(By.XPATH, '//*[@id="DBFieldBox"]/div[1]/i')
        ele_input1.click()
        time.sleep(random.randint(1,2))
        ele_input2 = browser.find_element(By.XPATH, '//li[@value="LY"]')
        ele_input2.click()
        time.sleep(10)
        print('...正在搜索 '+ send_key_word +' 相关的论文...')
        ele_search_paper_input = browser.find_element(By.XPATH, '//input[@id="txt_SearchText"]')
        ele_search_paper_input.send_keys(send_key_word) # 这里可以修改想要搜索的内容
        time.sleep(5)
        ele_search_paper_confirm = browser.find_element(By.XPATH, '//input[@type="button"]')
        ele_search_paper_confirm.click()
        print('...搜索成功...')
        time.sleep(11)
        ele_year_extend = browser.find_element(By.XPATH, '//*[@id="divGroup"]/dl[3]/dt/i[1]')
        ele_year_extend.click()
        time.sleep(4.5)
        ele_year = browser.find_element(By.XPATH, '//*[@id="divGroup"]/dl[3]/dd/div/ul/li[11]/a')
        ele_year.click()
        ele_search_total_num = browser.find_element(By.XPATH, "//span[@class='pagerTitleCell']/em")
        print("...共找到" + ele_search_total_num.text + "条结果...")
        print("...搜索的论文结果如下...")
        for i in tqdm(range(300)):
            time.sleep(0.5)
            eles = browser.find_elements(By.XPATH, "//table[@class='result-table-list']/tbody/tr")
            for ele in eles:
                ele_seq = ele.find_element(By.CLASS_NAME, 'seq')
                self.write_to_file(ele_seq.text + '\t', send_key_word)
                # print(ele_seq.text + '\t')
                ele_name = ele.find_element(By.CLASS_NAME,'fz14')
                self.write_to_file(ele_name.text + '\t', send_key_word)
                # print(ele_name.text + '\t')
                ele_author = ele.find_element(By.CLASS_NAME,'author')
                self.write_to_file(ele_author.text + '\t', send_key_word)
                # print(ele_author.text + '\t')
                ele_source = ele.find_element(By.CLASS_NAME,'source')
                self.write_to_file(ele_source.text + '\t', send_key_word)
                # print(ele_source.text + '\t')
                ele_date = ele.find_element(By.CLASS_NAME,'date')
                self.write_to_file(ele_date.text + '\t', send_key_word)
                # print(ele_date.text + '\t')
                ele_quote = ele.find_element(By.CLASS_NAME, 'quote')
                self.write_to_file(ele_quote.text + '\t', send_key_word)
                # print(ele_quote.text + '\t')
                ele_download = ele.find_element(By.CLASS_NAME, 'download')
                self.write_to_file(ele_download.text + '\t', send_key_word)
                # print(ele_download.text + '\t')
                # ele_html_reader = ele.find_element(By.XPATH, "//a[@title='HTML阅读']") # html登陆不进去的，没用
                # self.write_to_file(ele_html_reader.get_attribute("href")+ '\n')
                # print(ele_html_reader.get_attribute("href") + '\t')
                self.write_to_file('\n', send_key_word)
            print("...下一页...")
            time.sleep(random.randint(3,5))
            try:
                ele_nextpage = browser.find_element(By.LINK_TEXT, "下一页")
                ele_nextpage.click()
            except:
                print("已到达目录末尾")
            time.sleep(random.randint(5,7))
        print("论文结果写入完成")
        browser.quit()

    def main(self):
        browser = webdriver.Chrome()
        browser.maximize_window()
        journal_name = '文艺理论与批评' # 指定期刊的名字
        send_key_word = '（' + journal_name + '）' 
        self.crawler_begin(browser, send_key_word) 

if __name__ == '__main__':
    crawler_Paper = Crawler_Paper()
    crawler_Paper.main()
