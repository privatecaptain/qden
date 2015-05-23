from flask import Flask, request, make_response, redirect, render_template


app = Flask(__name__,static_url_path="")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name = name)

if __name__ == '__main__':
    app.run(debug = True)
    # app.run()