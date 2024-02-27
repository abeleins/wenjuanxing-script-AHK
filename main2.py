import logging
import numpy
from selenium.common import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver import ActionChains
from selenium import webdriver
import time
import json

# 问卷地址
url = 'https://www.wjx.cn/vm/PS4amwz.aspx'
number = 50

option = webdriver.EdgeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_experimental_option('useAutomationExtension', False)
option.add_experimental_option('detach', False)  #不自动关闭浏览器
driver = webdriver.Edge(options=option)
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                       {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
                        })
# 设置浏览器的大小和位置
driver.set_window_size(1600, 1400)
driver.set_window_position(x=0, y=0)


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

# 量表
def run():
    index = 0
    for config in configs:
        index += 1
        match(config['t-type']):
            case 1:
                radio(config, index)
            #提交
    driver.find_element(By.XPATH, '//*[@id="ctlNext"]').click()
    time.sleep(1)

    try:
        WebDriverWait(driver, 15).until(
            ec.url_changes(url)
        )
    except TimeoutException:
        slider_move(count, dest=380)
        # try:
    #     # driver.find_element(
    #     #     By.XPATH, '//*[@id="layui-layer1"]/div[3]/a[1]').click()
    #     # time.sleep(0.5)
    #     # driver.find_element(By.XPATH, '//*[@id="SM_BTN_1"]').click()
    #     # time.sleep(4)
    # except:
    #     pass
    # 滑块验证
    # try:
    #     slider = driver.find_element(
    #         By.XPATH, '//*[@id="nc_1__scale_text"]/span')
    #     if str(slider.text).startswith("请按住滑块"):
    #         width = slider.size.get('width')
    #         ActionChains(driver).drag_and_drop_by_offset(
    #             slider, width, 0).perform()
    # except:
    #     pass
    try:
        time.sleep(2)
        handles = driver.window_handles
        driver.switch_to.window(handles[0])
    except:
        pass
    # driver.close()

# def close_all_windows(driver):
#     for handle in driver.window_handles:
#         driver.switch_to.window(handle)
#         driver.close()
def slider_move(loop_index, dest=380):
    """
    :param loop_index: int
    :param dest: int # A position where you want to move.
    """
    try:
        el_slider = WebDriverWait(driver, 10).until(
            presence_of_element_located(
                (By.XPATH, "//*[@id='nc_1__scale_text']/span"))
        )
        ActionChains(driver).click_and_hold(el_slider).perform()
        ActionChains(driver).move_by_offset(xoffset=dest, yoffset=0).perform()
        ActionChains(driver).release().perform()
    except (TimeoutException, ElementClickInterceptedException):
        logging.error(f"第 {loop_index} 次请求执行失败！")




count = 0
while count < number:
    # 访问问卷链接
    driver.get(url)
    count += 1
    run()
    print(f"第 {count} 次任务执行成功。")
    if number == count:
        driver.close()
