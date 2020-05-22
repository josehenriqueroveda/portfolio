import csv
from flask import Flask, render_template, url_for, request, redirect, send_from_directory
app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/<string:page_name>')
def nav_page(page_name):
    return render_template(page_name)


def write_to_file(data):
    try:
        with open('database.txt', mode='a') as database:
            email = data['email']
            subject = data['subject']
            message = data['message']
            file = database.write(f'\n{email},{subject},{message}')
    except FileNotFoundError as e:
        print(f'Error: {e}')


def write_csv(data):
    try:
        with open("./database.csv", mode='a', newline="" ) as csvfile:
            email = data['email']
            subject = data['subject']
            message = data['message']
            csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([email,subject,message])
    except OSError as err:
        print(f'Something went wrong: {err}')
                        


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_csv(data)
            return redirect('/thanks.html')
        except:
            return 'It did not save to database'
    else:
        return 'Error on request method'


if __name__=="__main__":
    app.run(debug=True)
    app.add_url_rule('/favicon.ico',
                 redirect_to=url_for('static', filename='favicon.ico'))