from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
#import undetected_chromedriver.v2 as uc
import undetected_chromedriver as uc
import time
import random
import os
from selenium.webdriver.common.keys import Keys
from pydub import AudioSegment
from vosk import Model, KaldiRecognizer
import wave
import soundfile as sf
import librosa
import json
from selenium.webdriver.chrome.options import Options
import sys

from common.functions_of_checking import check_xpath, check_class
from common.secondary_functions import delay, close_windows
import subprocess

def main(driver_path):

    options = uc.ChromeOptions()
    # options.user_data_dir ="/home/hacker/.config/google-chrome/Default"
    # options.emulate_touch = True
    options.add_argument('--disable-notifications')
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('useAutomationExtension', False)
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36")
    # options.add_argument('--headless')

    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-first-run")
    options.add_argument("--disable-fre")

    options.add_argument("--no-default-browser-check")
    options.add_argument('--no-sandbox')
    # options.add_argument('start-maximized')
    # options.add_argument("window-size=900,600")
    options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
    # options.add_argument('--headless')
    driver = uc.Chrome(driver_executable_path=driver_path,
                       options=options)
    driver.set_window_size(900, 1000)
    action = webdriver.ActionChains(driver)
    driver.get('https://www.google.com/recaptcha/api2/demo')
    time.sleep(2)

    solving_recaptcha(driver, action, driver_path)

    driver.close(), driver.quit()

def solving_recaptcha(driver, action, driver_path):

    # start solve captcha
    element = driver.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]')
    action.move_to_element_with_offset(element, random.randint(0, 70), random.randint(0, 20)).click().perform()
    delay()
    # set all main variables
    wait = WebDriverWait(driver, 5)
    main_handle = driver.window_handles[0]
    try:
        if check_xpath(driver, '//iframe[@title="recaptcha challenge"]'):
            main_iframe = wait.until(ec.element_to_be_clickable((By.XPATH, '//iframe[@title="recaptcha challenge"]')))
        else:
            main_iframe = wait.until(ec.element_to_be_clickable((By.XPATH, '//iframe[@title="recaptcha challenge expires in two minutes"]')))
    except:
        action.move_to_element_with_offset(element, random.randint(0, 70), random.randint(0, 20)).click().perform()
        delay()
        if check_xpath(driver, '//iframe[@title="recaptcha challenge"]'):
            main_iframe = wait.until(ec.element_to_be_clickable((By.XPATH, '//iframe[@title="recaptcha challenge"]')))
        else:
            main_iframe = wait.until(
                ec.element_to_be_clickable((By.XPATH, '//iframe[@title="recaptcha challenge expires in two minutes"]')))

    # check fast solving of captcha
    driver.switch_to.frame(wait.until(ec.element_to_be_clickable((By.XPATH, '//iframe[@title="reCAPTCHA"]'))))
    xp = driver.find_element(By.ID, 'recaptcha-anchor').get_attribute('aria-checked')
    if xp == 'true':
        print('solved fast')
    else:
        # check if button of audio before clicked
        driver.switch_to.window(main_handle)
        driver.switch_to.frame(main_iframe)

        delay()
        xp = solve(driver, action, main_handle, main_iframe, driver_path)

        delay()
        while xp == 'false':
            xp = solve(driver, action, main_handle, main_iframe, driver_path)

            delay()
    driver.switch_to.default_content()
def solve(driver, action, main_handle, main_iframe, driver_path):
    # check if button of audio before clicked

    time.sleep(3)
    if check_class('rc-button-audio', driver):
        try:

            button_audio = driver.find_element(By.CLASS_NAME, 'rc-button-audio')
            action.move_to_element_with_offset(button_audio, random.randint(5, 7),
                                               random.randint(5, 7)).click().perform()
            delay()
            # check if your computer send bla bla bala bal
            print('the capcha open in images')
        except:
            print('the capcha open in audio')
    else:
        print('the capcha open in audio')
    # go to new window to download audio
    # input('Write new code')

    if check_xpath(driver, '//div[contains(text(), "Try again later")]'):
        # copy key

        driver.switch_to.window(main_handle)
        action.move_to_element_with_offset(main_iframe, - 10, -10).perform()
        site_key = driver.find_element(By.XPATH, '//*[@data-sitekey]').get_attribute('data-sitekey')


        # driver.execute_script("arguments[0].setAttribute('data-sitekey',arguments[1])",
        #                       driver.find_element(By.XPATH, '//*[@id="g-recaptcha-response"]'), input('Hilelelelelele'))

        # close iframe-        options = uc.ChromeOptions()
        new_options = uc.ChromeOptions()

        new_options.add_argument('--disable-notifications')
        # new_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # new_options.add_experimental_option('useAutomationExtension', False)
        # new_options.add_argument(
        #     "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36")

        new_options.add_argument("--disable-blink-features=AutomationControlled")
        new_options.add_argument("--disable-infobars")
        new_options.add_argument("--disable-extensions")
        new_options.add_argument("--no-first-run")
        new_options.add_argument("--disable-fre")
        new_options.add_argument("--no-default-browser-check")
        new_options.add_argument('--no-sandbox')
        new_options.add_argument('--headless')

        new_options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
        new_options.add_argument('--headless')
        browser = uc.Chrome(driver_path, options=new_options)
        browser.set_window_size(900, 1000)
        action = webdriver.ActionChains(driver)
        browser.get('https://www.google.com/recaptcha/api2/demo')
        time.sleep(5)
        browser.execute_script("document.querySelector('#g-recaptcha-response').value = '"+site_key+"'")
        delay()
        solving_recaptcha(browser, action)

        # copy value
        answer = browser.execute_script("document.querySelector('#g-recaptcha-response').value")
        browser.close()
        browser.quit()
        # passte copy
        driver.execute_script("document.querySelector('#g-recaptcha-response').value = '"+answer+"'")
        # return
        print('I"m all')
        return
    try:
        click_dowm = WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.CLASS_NAME, 'rc-audiochallenge-tdownload-link')))
        action.move_to_element(click_dowm).click().perform()
    except:input('Stop')
    delay()
    try:
        window_after = driver.window_handles[1]
    except:
        click_dowm = driver.find_element(By.CLASS_NAME, 'rc-audiochallenge-tdownload-link')
        action.move_to_element(click_dowm).click().perform()
        window_after = driver.window_handles[1]
    window_before = driver.window_handles[0]

    driver.switch_to.window(window_after)
    delay()
    # download audio

    action.move_to_element(driver.find_element(By.TAG_NAME, 'video')).move_by_offset(random.randint(110, 130),
                                                                                     random.randint(40,
                                                                                                    60)).click().perform()
    action.key_down(Keys.UP).key_up(Keys.UP).key_down(Keys.ENTER).key_up(Keys.ENTER).perform()
    delay()

    driver.close()
    driver.switch_to.window(window_before)
    delay()
    close_windows(driver, main_handle)
    driver.switch_to.frame(main_iframe)
    frase = recognize_audio()
    if frase == '' or frase == None:
        again = driver.find_element(By.ID, 'recaptcha-reload-button')
        action.move_to_element(again).click().perform()
    else:
        print(frase)

        inputs = driver.find_element(By.ID, 'audio-response')
        action.move_to_element(inputs).click().send_keys(frase).perform()

        delay()

        button_verify = driver.find_element(By.ID, 'recaptcha-verify-button')
        action.move_to_element(button_verify).click().perform()
    delay()


    os.remove('/home/hacker/Downloads/audio.wav')
    delay()
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]'))
    xp = driver.find_element(By.ID, 'recaptcha-anchor').get_attribute('aria-checked')
    driver.switch_to.default_content()
    driver.switch_to.frame(main_iframe)
    return xp

def recognize_audio():
    excepts = True
    try:
        sound = AudioSegment.from_file('/home/hacker/Downloads/audio.mp3')
        directory = '/home/hacker/Downloads/audio.mp3'

    except:
        excepts = False
    if excepts == False:
        for path in sys.path:
            try:
                sound = AudioSegment.from_file(path + '/audio.mp3')
                directory = path + '/audio.mp3'
                break
            except:
                pass
    sound.export('/home/hacker/Downloads/audio.wav', format="wav")
    os.remove(directory)
    # change to the file directory
    # librosa.output.write_wav('tests.wav', 'test1.wav', sr=8000)
    a, b = librosa.load('/home/hacker/Downloads/audio.wav', sr=24000)
    # librosa.output.write_wav('tests.wav', a, b)
    sf.write('/home/hacker/Downloads/audio.wav', a, b)
    # SetLogLevel(0)
    wf = wave.open('/home/hacker/Downloads/audio.wav', "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print("Audio file must be WAV format mono PCM.")
        return ''
    model = Model("model")
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.PartialResult())
            frase_in_audio = res["partial"]
            return frase_in_audio
