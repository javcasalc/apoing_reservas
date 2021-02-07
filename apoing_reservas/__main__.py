import argparse

from apoing_reservas.apoing_reservas import DoLogin, InitLoginPage

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--user", type=str, help="apoing username")
    parser.add_argument("-pass", type=str, help="apoing user password")
    parser.add_argument(
        "--day",
        metavar=("Lunes", "Martes", "Miércoles", "Jueves", "Sábado", "Domingo"),
        help="Day of the week to book",
    )
    parser.add_argument(
        "--hour",
        type=str,
        help="Hour range to book, for example: 10:00-11:00 or 16:00-17:00",
    )
    parser.add_argument(
        "--tuple_args",
        type=tuple,
        default=("ctl00$user", "pass", "Button2"),
        help="Tuple to search in html code. Default =  (ctl00$user, pass, Button2)",
    )
    args = parser.parse_args()

    my_driver = InitLoginPage("https://www.apoing.com/es/index.aspx")
    my_login = DoLogin(
        my_driver,
        args["user"],
        args["pass"],
        args["tuple_args"],
        args["day"],
        args["hour"],
    )
