from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/getResponse")
def getResponse():
    user_message = request.args.get("user_message")
    print(user_message)
    print(type(user_message))
    return {"message": "test"}

if __name__ == "__main__":
    app.run()