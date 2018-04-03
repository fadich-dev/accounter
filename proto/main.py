from cli.app import Application


if __name__ == '__main__':

    Application.clear()
    app = Application()
    try:
        app.cmdloop()
    except KeyboardInterrupt:
        del app
        Application.clear()
