import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

DRIVER_PATH = "/usr/bin/chromedriver"


def InitLoginPage(site_url: str = "https://www.apoing.com/es/index.aspx") -> WebDriver:
    try:
        driver = webdriver.Firefox()
        driver.get(site_url)
        return driver

    except Exception:
        return None


def DoLogin(
    driver: WebDriver,
    username: str,
    password: str,
    user_pass_login_tuple: tuple,
    dia_deseado: str,
    hora_deseada: str,
) -> WebElement:
    print("driver: ", driver)
    print("username: ", username)

    try:
        print("Iniciando proceso de autenticación....")
        content = driver.find_element_by_link_text("Identifícate")
        content.click()

        username_field = driver.find_element_by_name(user_pass_login_tuple[0])
        password_field = driver.find_element_by_id(user_pass_login_tuple[1])
        login_button = driver.find_element_by_id(user_pass_login_tuple[2])

        print("Esperando a que salga ventana de autenticación....")
        time.sleep(1)

        print("Autenticando....")
        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()
        print("Autenticado.")

        print("Entrando en reservas....")
        try:
            reservar_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "MainContent_btn_reservar"))
            )
        except Exception as e:
            print(e)
            driver.quit()
            raise ()

        if reservar_button.is_enabled:
            driver.execute_script("arguments[0].click()", reservar_button)
        else:
            driver.quit()
            raise ("reservar_button not enabled")

        driver.page_source

        print("Buscando siguiente semana...")
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "MainContent_next1"))
            )
        except Exception as e:
            print(e)
            print(driver.page_source)
            driver.quit()
            raise ()

        if next_button.is_enabled:
            driver.execute_script("arguments[0].click()", next_button)
            time.sleep(5)
        else:
            driver.quit()
            raise ("next_button not enabled")

        driver.page_source

        matrix_horario = dict()

        table_id = driver.find_element_by_id("MainContent_GridView1")
        rows = table_id.find_elements(By.TAG_NAME, "tr")
        for row in rows[:-1]:
            cols = row.find_elements(By.TAG_NAME, "td")
            for col in zip(
                (
                    "Lunes",
                    "Martes",
                    "Miércoles",
                    "Jueves",
                    "Viernes",
                    "Sábado",
                    "Domingo",
                ),
                cols[1:],
            ):
                if col[1].text != "No disponible":
                    hora = col[1].text.split("\n")[0]
                    estado = col[1].text.split("\n")[1]
                else:
                    hora = "No disponible"
                    estado = "No disponible"

                dia = col[0]

                print(dia, hora, estado)
                if hora in matrix_horario.keys():
                    matrix_horario[hora][dia] = estado
                else:
                    matrix_horario[hora] = dict()
                    matrix_horario[hora][dia] = estado

        if matrix_horario[hora_deseada][dia_deseado] == "LIBRE":
            print("Disponible")
        else:
            print("Ocupado: ", matrix_horario[hora_deseada][dia_deseado])

    except Exception as e:
        print(e)
        driver.quit()

    return login_button
