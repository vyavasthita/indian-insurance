from apps import create_app


if __name__ == '__main__':
    application = create_app()
    application.run()
else:
    application = create_app()
