import random
import time
import numpy
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import json

# 问卷地址
url = 'https://www.wjx.cn/vm/Q0IdCwo.aspx'
number = 10
# 滑动轨迹
tracks = [i for i in range(1, 50, 3)]

option = webdriver.EdgeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_experimental_option('useAutomationExtension', False)
option.add_experimental_option('detach', True)  #不自动关闭浏览器
driver = webdriver.Edge(options=option)
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                       {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
                        })
# 设置浏览器的大小和位置
driver.set_window_size(800, 700)
driver.set_window_position(x=400, y=50)
# 访问问卷链接
driver.get(url)

def read_json():
    with open('./config.json', 'r', encoding='utf-8') as configs:
        content = json.load(configs)
        return content['configs']
configs = read_json()
# 单选


# def radio(config, index):
#     xpath = f'//*[@id="div{index}"]/*[@class="ui-controlgroup column1"]/div'
#     a = driver.find_elements(By.XPATH, xpath)
#     r = numpy.random.choice(a=numpy.arange(1, len(a) + 1), p=config['PR'])
#     driver.find_element(By.CSS_SELECTOR,
#                         f'#div{index} > div.ui-controlgroup > div:nth-child({r})').click()
def radio(config, index):
    xpath = f'//*[@id="div{index}"]/*[@class="ui-controlgroup column1"]/div'
    a = driver.find_elements(By.XPATH, xpath)
    r = numpy.random.choice(a=numpy.arange(1, len(a) + 1), p=config['PR'])
    element = driver.find_element(By.CSS_SELECTOR, f'#div{index} > div.ui-controlgroup > div:nth-child({r})')

    # 创建一个 ActionChains 对象
    actions = ActionChains(driver)

    # 使用 move_to_element 方法将视口滚动到元素
    actions.move_to_element(element).perform()

    # 点击元素
    element.click()
# 多选


def check(config, index):
    xpath = f'//*[@id="div{index}"]/*[@class="ui-controlgroup column1"]/div'
    a = driver.find_elements(By.XPATH, xpath)
    q = numpy.random.choice(a=numpy.arange(
        1, len(a) + 1), size=config['option'], p=config['PR'], replace=False)
    q.sort()
    for r in q:
        driver.find_element(
            By.CSS_SELECTOR,   f'#div{index} > div.ui-controlgroup > div:nth-child({r})').click()

# 矩阵


def matrix(config, index):
    xpath = f'//*[@id="div{index}"]/div/table/tbody/tr[@tp="d"]'
    a = driver.find_elements(By.XPATH, xpath)
    topic_nums = len(a)
    for item in range(0, topic_nums):
        option_nums = len(a[item].find_elements(By.XPATH, f'td'))
        r = numpy.random.choice(a=numpy.arange(
            2, option_nums + 2), p=config['PR'])
        print('----------------')
        print(r)
        driver.find_element(
            By.CSS_SELECTOR, f'#drv{index}_{item + 1} > td:nth-child({r})').click()

# 滑动


def slide(config, index):
    interval = config['intervals']
    score = random.randint(interval[0], interval[1])
    driver.find_element(By.CSS_SELECTOR, f'#q{index}').send_keys(score)

# 填空


def fill(config, index):
    driver.find_element(By.CSS_SELECTOR, f'#q{index}').send_keys(1)

# 排序


def sort(config, index):
    xpath = f'//*[@id="div{index}"]/ul/li'
    a = driver.find_elements(By.XPATH, xpath)
    q = numpy.random.choice(a=numpy.arange(
        1, len(a) + 1),size=config['option'], replace=False, p=config['PR'])
    element_arr = []
    for b in q:
        element_arr.append(driver.find_element(
            By.CSS_SELECTOR, f'#div{index} > ul > li:nth-child({b})'))
    for div in element_arr:
        div.click()
        time.sleep(0.4)

# 量表


def fun1(config, index):
    xpath = f'//*[@id="div{index}"]/div/div/ul/li'
    a = driver.find_elements(By.XPATH, xpath)
    q = numpy.random.choice(a=numpy.arange(1, len(a) + 1), p=config['PR'] )
    driver.find_element(
        By.CSS_SELECTOR, f'#div{index} > div.scale-div > div > ul > li:nth-child({q})').click()


def run():
    index = 0
    for config in configs:
        index += 1
        match(config['t-type']):
            case 1:
                radio(config, index)
            case 2:
                check(config, index)
            case 3:
                matrix(config, index)
            case 4:
                slide(config, index)
            case 5:
                fill(config, index)
            case 6:
                sort(config, index)
            case 7:
                fun1(config, index)
            #提交
    driver.find_element(By.XPATH, '//*[@id="ctlNext"]').click()
    time.sleep(1)
    try:
        driver.find_element(
            By.XPATH, '//*[@id="layui-layer1"]/div[3]/a[1]').click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, '//*[@id="SM_BTN_1"]').click()
        time.sleep(4)
    except:
        pass
    # 滑块验证
    try:
        slider = driver.find_element(
            By.XPATH, '//*[@id="nc_1__scale_text"]/span')
        if str(slider.text).startswith("请按住滑块"):
            width = slider.size.get('width')
            ActionChains(driver).drag_and_drop_by_offset(
                slider, width, 0).perform()
    except:
        pass
    time.sleep(2000)
    handles = driver.window_handles
    driver.switch_to.window(handles[0])
    driver.close()

count = 0
while count < number:
    count += 1
    run()
