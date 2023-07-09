from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from vosk import Model, KaldiRecognizer
from pydub import AudioSegment
import soundfile as sf
import librosa
import wave

import random
import json
import sys
import os

from common import Driver

def main(driver_path):

    driver = Driver(driver_path=driver_path, headless=False)

    driver.driver_.set_window_size(900, 1000)

    driver.driver_.get('https://www.google.com/recaptcha/api2/demo')

    driver.delay()

    solving_recaptcha(driver)

    driver.stop()

def solving_recaptcha(driver):

    # start solve captcha
    element = driver.get_element('//iframe[@title="reCAPTCHA"]')
    driver.actions.move_to_element_with_offset(element, random.randint(0, 70), random.randint(0, 20)).click().perform()

    driver.delay()

    # set all main variables
    main_handle = driver.driver_.window_handles[0]
    try:
        if driver.check_xpath('//iframe[@title="recaptcha challenge"]'):
            main_iframe = driver.get_element('//iframe[@title="recaptcha challenge"]', condition="clickable")

        else:
            main_iframe = driver.get_element('//iframe[@title="recaptcha challenge expires in two minutes"]', condition="clickable")

    except:
        driver.actions.move_to_element_with_offset(element, random.randint(0, 70), random.randint(0, 20)).click().perform()
        driver.delay()

        if driver.check_xpath('//iframe[@title="recaptcha challenge"]'):
            main_iframe = driver.get_element('//iframe[@title="recaptcha challenge"]', condition="clickable")

        else:
            main_iframe = driver.get_element('//iframe[@title="recaptcha challenge expires in two minutes"]', condition="clickable")

    # check fast solving of captcha
    driver.driver_.switch_to.frame(driver.get_element('//iframe[@title="reCAPTCHA"]', condition='clickable'))
    xp = driver.get_element('recaptcha-anchor', By.ID).get_attribute('aria-checked')

    if xp == 'true':
        print('solved fast')

    else:

        # check if button of audio before clicked
        driver.driver_.switch_to.window(main_handle)
        driver.driver_.switch_to.frame(main_iframe)

        driver.delay()
        xp = solve(driver, main_handle, main_iframe)

        driver.delay()
        while xp == 'false':
            xp = solve(driver, main_handle, main_iframe)

            driver.delay()
    driver.driver_.switch_to.default_content()

def solve(driver, main_handle, main_iframe):
    # check if button of audio before clicked

    driver.delay()
    if driver.check_class('rc-button-audio'):
        try:

            button_audio = driver.get_element('rc-button-audio', By.CLASS_NAME)
            driver.actions.move_to_element_with_offset(button_audio, random.randint(5, 7),
                                               random.randint(5, 7)).click().perform()
            driver.delay()
            # check if your computer send bla bla bala bal
            print('the capcha open in images')
        except:
            print('the capcha open in audio')
    else:
        print('the capcha open in audio')

    # go to new window to download audio
    try:
        click_dowm = driver.get_element('rc-audiochallenge-tdownload-link', By.CLASS_NAME, 'clickable')
        driver.actions.move_to_element(click_dowm).click().perform()
    except:input('Stop')
    driver.delay()
    try:
        window_after = driver.driver_.window_handles[1]
    except:
        click_dowm = driver.get('rc-audiochallenge-tdownload-link', By.CLASS_NAME)

        driver.actions.move_to_element(click_dowm).click().perform()

        window_after = driver.driver_.window_handles[1]
    window_before = driver.driver_.window_handles[0]

    driver.driver_.switch_to.window(window_after)
    driver.delay()
    # download audio

    driver.actions.move_to_element(driver.get_element('video', By.TAG_NAME)).move_by_offset(random.randint(110, 130),
                                                                                     random.randint(40,
                                                                                                    60)).click().perform()
    driver.actions.key_down(Keys.UP).key_up(Keys.UP).key_down(Keys.ENTER).key_up(Keys.ENTER).perform()

    driver.delay(), driver.driver_.close()

    driver.driver_.switch_to.window(window_before)

    driver.delay()

    driver.close_windows(main_handle)
    driver.driver_.switch_to.frame(main_iframe)

    frase = recognize_audio()
    if frase == '' or frase == None:
        again = driver.get_element('recaptcha-reload-button', By.ID)
        driver.actions.move_to_element(again).click().perform()
    else:
        print(frase)

        inputs = driver.get_element('audio-response', By.ID)
        driver.actions.move_to_element(inputs).click().send_keys(frase).perform()

        driver.delay()

        button_verify = driver.get_element('recaptcha-verify-button', By.ID)
        driver.actions.move_to_element(button_verify).click().perform()
    driver.delay()

    os.remove('/home/hacker/Downloads/audio.wav')
    driver.delay()
    driver.driver_.switch_to.default_content()
    driver.driver_.switch_to.frame(driver.get_element('//iframe[@title="reCAPTCHA"]', By.XPATH))

    xp = driver.get_element('recaptcha-anchor', By.ID).get_attribute('aria-checked')

    driver.driver_.switch_to.default_content(), driver.driver_.switch_to.frame(main_iframe)

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
    a, b = librosa.load('/home/hacker/Downloads/audio.wav', sr=24000)
    sf.write('/home/hacker/Downloads/audio.wav', a, b)
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
