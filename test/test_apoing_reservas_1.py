from apoing_reservas.apoing_reservas import InitLoginPage


def test_InitLoginPage() -> None:
    try:
        my_driver = InitLoginPage("https://www.apoing.com/es/index.aspx")
        assert my_driver is not None

    finally:
        my_driver.quit()
