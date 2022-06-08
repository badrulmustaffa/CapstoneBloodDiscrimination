# Done by Muhammad Mustaffa

from my_app import create_app, config

app = create_app(config.DevelopmentConfig)

if __name__ == '__main__':
    app.run(host='capstonebloodtester.com')
