import time
import random


def close_windows(driver, main_handle):
    # function of closing not necessary windows
    for handle in driver.window_handles:
        try:

            if handle != main_handle:
                driver.switch_to.window(handle)
                driver.close()
                time.sleep(1)
        except:
            continue
    driver.switch_to.window(main_handle)
def delay():
    # function of waiting
    # create number to wait
    t = random.randint(500000000, 3000000000)

    t = t  / 1000000000
    # wait
    time.sleep(t)

def emitate_human(driver, action ):
        # function of emitating human

        speed = 20

        current_scroll_position, new_height = 0, 1
        action.move_by_offset(0, 0).perform()
        for rite in range(5):
            random_number = random.randint(1, 2)
            if random_number == 1:
                action.move_by_offset(0, 0).perform()
            if random_number == 2:

                try:

                    current_scroll_position += speed
                    driver.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
                    new_height = driver.execute_script("return document.body.scrollHeight")
                except:
                    continue
            # if random_number == 3:
            #     action.click().perform()
            time.sleep(1)
