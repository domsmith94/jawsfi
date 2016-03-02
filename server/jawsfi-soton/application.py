from flask import Flask
import pi

# EB looks for an 'application' callable by default.
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello'

@app.route('/register', methods=['POST'])
def register_pi():
    if request.method == 'POST':
        print 'We recieved a POST request on register'
        content = request.json
        print content


@app.route('/send-data', methods=['POST'])
def send_data():
    if request.method == 'POST':
        do_the_login()
        content = request.json
        print 'We recieved a POST request on send-data'
        return 'POST request for send data'


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = True
    app.run()