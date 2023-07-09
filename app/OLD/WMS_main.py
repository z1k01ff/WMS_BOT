import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from TRASH.selenium_to_txt import selenium_to_text

url = "http://wms_ub1rds.berta.corp:8080/safena/start?lang=russian&theme=classic&app=wmsprod"
# chrome_path = '/Users/admin/Downloads/chromedriver'
chrome_path = 'C:\chromedriver1\chromedriver.exe'
s = Service(executable_path=chrome_path)

# Прихований режим
# options = Options()
# options.add_argument("--headless=new")

result = {}

def driver():
    driver = webdriver.Chrome(service=s)
    try:
        driver.maximize_window()
        driver.get(url)

    except Exception as ex:
        print(ex)

    finally:
        print("Driver initialised")
        return driver

# test = driver()


def wms_login(driver):
    # driver = webdriver.Chrome(service=s)

    try:
        driver.maximize_window()
        driver.get(url)

        # Логін
        # user_input = driver.find_element(By.ID, 'user').clear() poprobuvaty!!!!!!!
        user_input = driver.find_element(By.ID, 'user')
        user_input.clear()
        user_input.send_keys("TEST3")

        # Пароль
        pwd_input = driver.find_element(By.ID, 'pwd')
        pwd_input.clear()
        pwd_input.send_keys("TEST3")
        pwd_input.send_keys(Keys.ENTER)
        time.sleep(2)
        try:
            # Повідомлення про те що користувач вже залогінений
            warning_mess = driver.find_element(By.ID, 'SINGLE_LOGIN_WARNING-yes-btnInnerEl')
            if warning_mess:
                ActionChains(driver).click(warning_mess).perform()
                time.sleep(2)
        except Exception as ex:
            print(ex)


    except Exception as ex:
        print(ex)

    finally:
        print("Sucesfull login")
        return driver




def wms_tp_fast(driver):
    try:
        # Кнопка старт
        start_btm = driver.find_element(By.ID, 'button-1084-btnInnerEl')
        ActionChains(driver).click(start_btm).perform()
        # time.sleep(2)

        # Кнопка Транспортние поручения
        menu_tr_btm = driver.find_element(By.ID, 'MENU-F_ZLECENIA_TRANSPORT_MENU-textEl')
        ActionChains(driver).click(menu_tr_btm).perform()
        time.sleep(2)

        # Кнопка Текущие транспортние поручения
        tr_btm = driver.find_element(By.ID, 'MENU-TR_TRANSPORTS_FAST_F-textEl')
        ActionChains(driver).click(tr_btm).perform()
        time.sleep(3)

    except Exception as ex:
        print(ex)

    finally:
        print("TP successful opening")


def wms_vidpravka(driver) -> object:
    try:

        # Pole TIP POROCHENIYA
        pole_type_tp = driver.find_element(By.ID, 'TR_TRANSPORTS_FAST_F-0-F_F_TRANSPORT_TYPE-inputEl')
        ActionChains(driver).click(pole_type_tp).perform()
        pole_type_tp.clear()
        pole_type_tp.send_keys("Відправка")

        # Knopka Search
        search_btm = driver.find_element(By.ID, 'TR_TRANSPORTS_FAST_F-0-_0_GRID-PAGING_SEARCH-btnIconEl')
        ActionChains(driver).click(search_btm).perform()
        time.sleep(5)

        # Poshuk vsih elementiv po uchastku
        tp_pole_uchastok = driver.find_elements(By.XPATH,
                                                "//td[@class='x-grid-cell x-grid-td x-grid-cell-qgridcolumn-1143']")
        selenium_to_text(tp_pole_uchastok, "kilkist_vidpravok")

    except Exception as ex:
        print(ex)

    finally:
        print("TP vidpravka Succesfull")


def wms_vidpravka_marshrut(driver) -> object:
    try:

        # Pole TIP POROCHENIYA
        pole_type_tp = driver.find_element(By.ID, 'TR_TRANSPORTS_FAST_F-0-F_F_TRANSPORT_TYPE-inputEl')
        ActionChains(driver).click(pole_type_tp).perform()
        pole_type_tp.clear()
        pole_type_tp.send_keys("Відправка")

        # Pole nomer artykula id="TR_TRANSPORTS_FAST_F-0-F_F_PRODUCT_NR-inputEl"
        pole_artikul_nr = driver.find_element(By.ID, 'TR_TRANSPORTS_FAST_F-0-F_F_PRODUCT_NR-inputEl')
        ActionChains(driver).click(pole_artikul_nr).perform()
        pole_artikul_nr.clear()
        pole_artikul_nr.send_keys("0*")

        # Knopka Search TR_TRANSPORTS_FAST_F-0-_0_GRID-PAGING_SEARCH-btnIconEl
        search_btm = driver.find_element(By.ID, 'TR_TRANSPORTS_FAST_F-0-_0_GRID-PAGING_SEARCH-btnIconEl')
        ActionChains(driver).click(search_btm).perform()
        time.sleep(5)

        vidpravka_berta = driver.find_elements(By.XPATH,
                                            "//td[@class='x-grid-cell x-grid-td x-grid-cell-qgridcolumn-1143']")

        selenium_to_text(vidpravka_berta, "vidpravka_berta")

        # Pole nomer artykula id="TR_TRANSPORTS_FAST_F-0-F_F_PRODUCT_NR-inputEl"
        pole_artikul_nr = driver.find_element(By.ID, 'TR_TRANSPORTS_FAST_F-0-F_F_PRODUCT_NR-inputEl')
        ActionChains(driver).click(pole_artikul_nr).perform()
        pole_artikul_nr.clear()
        pole_artikul_nr.send_keys("МС*")

        # Knopka Search TR_TRANSPORTS_FAST_F-0-_0_GRID-PAGING_SEARCH-btnIconEl
        search_btm = driver.find_element(By.ID, 'TR_TRANSPORTS_FAST_F-0-_0_GRID-PAGING_SEARCH-btnIconEl')
        ActionChains(driver).click(search_btm).perform()
        time.sleep(5)

        vidpravka_blyzenko = driver.find_elements(By.XPATH,
                                            "//td[@class='x-grid-cell x-grid-td x-grid-cell-qgridcolumn-1143']")

        selenium_to_text(vidpravka_blyzenko, "vidpravka_blyzenko")




    except Exception as ex:
        print(ex)

    finally:
        print("TP vidpravka marshrut Succesfull")


def wms_popovn(driver) -> object:
    global kilkist_popovn
    try:

        # Pole TIP POROCHENIYA TR_TRANSPORTS_FAST_F-0-F_F_TRANSPORT_TYPE-inputEl
        pole_type_tp = driver.find_element(By.ID, 'TR_TRANSPORTS_FAST_F-0-F_F_TRANSPORT_TYPE-inputEl')
        ActionChains(driver).click(pole_type_tp).perform()
        pole_type_tp.clear()
        pole_type_tp.send_keys("Поповнення збору")

        #Pole nomer artykula id="TR_TRANSPORTS_FAST_F-0-F_F_PRODUCT_NR-inputEl"
        pole_artikul_nr = driver.find_element(By.ID, 'TR_TRANSPORTS_FAST_F-0-F_F_PRODUCT_NR-inputEl')
        ActionChains(driver).click(pole_artikul_nr).perform()
        pole_artikul_nr.clear()
        pole_artikul_nr.send_keys("0*")


        # Knopka Search TR_TRANSPORTS_FAST_F-0-_0_GRID-PAGING_SEARCH-btnIconEl
        search_btm = driver.find_element(By.ID, 'TR_TRANSPORTS_FAST_F-0-_0_GRID-PAGING_SEARCH-btnIconEl')
        ActionChains(driver).click(search_btm).perform()
        time.sleep(5)

        popovn_berta = driver.find_elements(By.XPATH,
                                           "//td[@class='x-grid-cell x-grid-td x-grid-cell-qgridcolumn-1143']")

        selenium_to_text(popovn_berta, "popovn_berta")

        # Pole nomer artykula id="TR_TRANSPORTS_FAST_F-0-F_F_PRODUCT_NR-inputEl"
        pole_artikul_nr = driver.find_element(By.ID, 'TR_TRANSPORTS_FAST_F-0-F_F_PRODUCT_NR-inputEl')
        ActionChains(driver).click(pole_artikul_nr).perform()
        pole_artikul_nr.clear()
        pole_artikul_nr.send_keys("МС*")

        # Knopka Search TR_TRANSPORTS_FAST_F-0-_0_GRID-PAGING_SEARCH-btnIconEl
        search_btm = driver.find_element(By.ID, 'TR_TRANSPORTS_FAST_F-0-_0_GRID-PAGING_SEARCH-btnIconEl')
        ActionChains(driver).click(search_btm).perform()
        time.sleep(5)

        popovn_blyzenko = driver.find_elements(By.XPATH,
                                            "//td[@class='x-grid-cell x-grid-td x-grid-cell-qgridcolumn-1143']")

        selenium_to_text(popovn_blyzenko, "popovn_blyzenko")

    except Exception as ex:
        print(ex)

    finally:
        print("TP popovnenya Succesfull")

def full_info(driver) -> object:
    #BTM's in TP FAST
    pole_type_tp = driver.find_element(By.ID, 'TR_TRANSPORTS_FAST_F-0-F_F_TRANSPORT_TYPE-inputEl') # POLE TIP PORUCHENIYA
    pole_product_nr = driver.find_element(By.ID, 'TR_TRANSPORTS_FAST_F-0-F_F_PRODUCT_NR-inputEl') # POLE product
    pole_na_mesto = driver.find_element(By.ID, 'TR_TRANSPORTS_FAST_F-0-F_TXT_SP_TO-inputEl')
    search_btm = driver.find_element(By.ID, 'TR_TRANSPORTS_FAST_F-0-_0_GRID-PAGING_SEARCH-btnIconEl') # KNOPKA SEARCH
    kolonka_uchastok_zbora = "//td[@class='x-grid-cell x-grid-td x-grid-cell-qgridcolumn-1143']"


    ################ BERTA ##################

    #POPOVNENYA
    ActionChains(driver).click(pole_type_tp).perform()
    pole_type_tp.clear()
    pole_type_tp.send_keys("Поповнення збору")

    ActionChains(driver).click(pole_product_nr).perform()
    pole_product_nr.clear()
    pole_product_nr.send_keys("0*")

    ActionChains(driver).click(search_btm).perform()
    time.sleep(5)

    popovn_berta = driver.find_elements(By.XPATH, kolonka_uchastok_zbora)

    selenium_to_text(popovn_berta, "popovn_berta")

    #PEREPAKOVKA
    ActionChains(driver).click(pole_type_tp).perform()
    pole_type_tp.clear()
    pole_type_tp.send_keys("Перепакування")

    ActionChains(driver).click(search_btm).perform()
    time.sleep(5)

    perepakovka_berta = driver.find_elements(By.XPATH, kolonka_uchastok_zbora)

    selenium_to_text(perepakovka_berta, "perepakovka_berta")

    #VIDPRAVKA
    ActionChains(driver).click(pole_type_tp).perform()
    pole_type_tp.clear()
    pole_type_tp.send_keys("Відправка")

    ActionChains(driver).click(search_btm).perform()
    time.sleep(5)

    vidpravka_berta = driver.find_elements(By.XPATH, kolonka_uchastok_zbora)
    # Dodaty poshuk po marsruty!!!!

    selenium_to_text(vidpravka_berta, "vidpravka_berta")

    ################ BLYZENKO ##################

    # POPOVNENYA
    ActionChains(driver).click(pole_type_tp).perform()
    pole_type_tp.clear()
    pole_type_tp.send_keys("Поповнення збору")

    ActionChains(driver).click(pole_product_nr).perform()
    pole_product_nr.clear()
    pole_product_nr.send_keys("МС*")

    ActionChains(driver).click(search_btm).perform()
    time.sleep(5)

    popovn_blyzenko = driver.find_elements(By.XPATH, kolonka_uchastok_zbora)

    selenium_to_text(popovn_blyzenko, "popovn_blyzenko")

    # PEREPAKOVKA
    ActionChains(driver).click(pole_type_tp).perform()
    pole_type_tp.clear()
    pole_type_tp.send_keys("Перепакування")

    ActionChains(driver).click(search_btm).perform()
    time.sleep(5)

    perepakovka_blyzenko = driver.find_elements(By.XPATH, kolonka_uchastok_zbora)

    selenium_to_text(perepakovka_blyzenko, "perepakovka_blyzenko")

    # VIDPRAVKA
    ActionChains(driver).click(pole_type_tp).perform()
    pole_type_tp.clear()
    pole_type_tp.send_keys("Відправка")

    ActionChains(driver).click(search_btm).perform()
    time.sleep(5)

    vidpravka_blyzenko = driver.find_elements(By.XPATH, kolonka_uchastok_zbora)

    selenium_to_text(vidpravka_blyzenko, "vidpravka_blyzenko")

    # peremischenya na IN-CONV*
    ActionChains(driver).click(pole_type_tp).perform()
    pole_type_tp.clear()
    pole_type_tp.send_keys("Переміщення")

    ActionChains(driver).click(pole_na_mesto).perform()
    pole_na_mesto.clear()
    pole_na_mesto.send_keys("IN*")

    ActionChains(driver).click(search_btm).perform()
    time.sleep(8)

    peremischenya_na_in_blyzenko = driver.find_elements(By.XPATH, kolonka_uchastok_zbora)

    selenium_to_text(peremischenya_na_in_blyzenko, "peremischenya_na_in_blyzenko")

    # peremischenya na ST*

    ActionChains(driver).click(pole_na_mesto).perform()
    pole_na_mesto.clear()
    pole_na_mesto.send_keys("STO*")

    ActionChains(driver).click(search_btm).perform()
    time.sleep(7)

    peremischenya_na_st_blyzenko = driver.find_elements(By.XPATH, kolonka_uchastok_zbora)

    selenium_to_text(peremischenya_na_st_blyzenko, "peremischenya_na_st_blyzenko")



def test1(driver):
    # Knopka Search
    search_btm = driver.find_element(By.ID, 'TR_TRANSPORTS_FAST_F-0-_0_GRID-PAGING_SEARCH-btnIconEl')
    ActionChains(driver).click(search_btm).perform()
    time.sleep(5)
    progress_bar = "td.x-grid-cell x-grid-td x-grid-cell-qgridcolumn-1143"
    test_progress = driver.find_elements(By.CSS_SELECTOR, progress_bar)
    print(len(test_progress))






def wms_exit(driver):
    driver.close()
    driver.quit()


if __name__ == "__main__":
    cycle = 0

    while True:
        test = driver()
        wms_login(test)
        wms_tp_fast(test)
        test1(test)
        # full_info(test)
        # wms_vidpravka_marshrut(test)
        # wms_popovn(test)
        # wms_vidpravka(test)
        wms_exit(test)
        cycle += 1
        print("Kolo #", cycle)
        time.sleep(60)
