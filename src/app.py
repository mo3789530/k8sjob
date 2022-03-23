from logging import getLogger
import logging
from k8sClient import k8sClient
from flask import Flask,render_template

app = Flask(__name__)

logger = getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@app.route("/")
async def root():
    return {"message": "Hello World"}

@app.route("/api/health")
async def health():
    return {"message": "Hello World"}


if __name__ == "__main__":
    app.run(debug=True)