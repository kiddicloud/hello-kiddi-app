import time
from flask import Flask, request, jsonify, current_app, g as app_ctx

app = Flask(__name__)

@app.before_request
def logging_before():
    # Store the start time for the request
    app_ctx.start_time = time.perf_counter()

@app.after_request
def logging_after(response):
    # Get total time in milliseconds
    total_time = time.perf_counter() - app_ctx.start_time
    # Log the time taken for the endpoint 
    current_app.logger.info('%0.4f ms %s %s %s', total_time, request.method, request.path, dict(request.args))
    response.headers["X-EXECUTION-TIME"] = f'{total_time:0.4f}'
    return response

@app.get('/')
def hello_world():
    time.sleep(1.5)
    return "Hello World!"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
