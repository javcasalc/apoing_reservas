from apoing_reservas.apoing_reservas import DoLogin, InitLoginPage


def test_DoLogin() -> None:
    my_driver = InitLoginPage("https://www.apoing.com/es/index.aspx")
    try:
        assert (
            DoLogin(
                my_driver,
                "error@gmail.com",
                "error",
                ("ctl00$user", "pass", "Button2"),
                "error",
                "error",
            )
            is not None
        )
    finally:
        my_driver.quit()
