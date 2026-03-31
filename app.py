import math
import socket
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def solve_quadratic(a, b, c):
    if a == 0:
        if b == 0:
            return {"roots": [], "type": "no_solution", "message": "No solution (a=0, b=0)"}
        return {"roots": [-c/b], "type": "linear", "message": f"Linear equation: x = {-c/b}"}
    
    discriminant = b**2 - 4*a*c
    
    if discriminant > 0:
        x1 = (-b + math.sqrt(discriminant)) / (2*a)
        x2 = (-b - math.sqrt(discriminant)) / (2*a)
        return {"roots": [x1, x2], "type": "two_real", "message": "Two real roots"}
    elif discriminant == 0:
        x = -b / (2*a)
        return {"roots": [x], "type": "one_real", "message": "One real root (repeated)"}
    else:
        real_part = -b / (2*a)
        imag_part = math.sqrt(abs(discriminant)) / (2*a)
        return {"roots": [f"{real_part}+{imag_part}i", f"{real_part}-{imag_part}i"], "type": "complex", "message": "Two complex roots"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve')
def solve():
    try:
        a = float(request.args.get('a', 0))
        b = float(request.args.get('b', 0))
        c = float(request.args.get('c', 0))
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid input. Please enter numeric values."}), 400
    
    if a == 0 and b == 0 and c == 0:
        return jsonify({"error": "All values cannot be zero"}), 400
    
    result = solve_quadratic(a, b, c)
    
    hostname = socket.gethostname()
    server_ip = socket.gethostbyname(hostname)
    
    return jsonify({
        "equation": f"{a}x² + {b}x + {c} = 0",
        "discriminant": b**2 - 4*a*c,
        "solution": result["roots"],
        "solution_type": result["type"],
        "message": result["message"],
        "server_ip": server_ip,
        "hostname": hostname
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)