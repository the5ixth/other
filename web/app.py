from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('hello.html')

if __name__ == "__main__":
    try:
        os.system('ln -s /home/mint/static static')
    except:
        pass
    app.run()
