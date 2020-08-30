from imagerepo import app
import os

if __name__ == '__main__':
    if not os.path.exists('static'):
        os.makedirs('static')

    # start app
    app.run()
