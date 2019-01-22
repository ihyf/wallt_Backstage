# coding:utf-8
from wallet.create_app import app
import wallet.views


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000)
    # app.run(host="localhost", port=7000)

