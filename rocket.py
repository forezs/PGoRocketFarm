from detector import *


end = False

if __name__ == '__main__':
    detector = MainDetector()
    action = MainAction()

    get_invasion()
    reopen_timer = time()
    next_timer = time()

    while True:
        ending = time()

        if keyboard.is_pressed('l'):
            sys.exit()

        if detector.detect_close_stop() or detector.detect_feed():
            action.click_back()
            sleep(1)
            action.click_back()

        if detector.detect_stop():
            action.open_stop()

        if detector.detect_battle_screen():
            action.open_backpack()

        if detector.detect_poke():
            sleep(1)
            reopen_timer = time()
            next_timer = time()
            print('[INFO] ROCKET BEATEN')
            action.click_back()
            end = True

        if end:
            get_invasion()
            sleep(2)
            end = False

        if ending - reopen_timer > 120:
            action.reopen()
            reopen_timer = time()
            next_timer = time()
            end = False

        if ending - next_timer > 30:
            end = True
            next_timer = time()
