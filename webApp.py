from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def linkEntered():
    this_link = ''
    if request.method == 'POST':
        this_link = request.form['link']

    return render_template('index.html', link=this_link)


if __name__ == '__main__':
    app.run()
