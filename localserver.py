from flask import Flask, request

app = Flask(__name__)

@app.route('/instagram/callback/')
def handle_callback():
    # logic to handle instagram request after authorization
    return 'Authorization success!'

if __name__ == '__main__':
    app.run(port=8000)
