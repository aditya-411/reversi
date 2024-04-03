from algo import Node
from flask import Flask, jsonify, request, render_template, send_from_directory
import numpy as np




app = Flask(__name__)

@app.route('/move/', methods=['GET', 'POST'])
def return_move():
    data = request.get_json()
    grid = None
    n = None
    chance = None
    depth = None

    try:
        grid = np.array(data['grid'])
        n = np.array(grid[0].size)
        chance = data['chance']
        depth = data['depth']
    except:
        return "invalid array"
    response = {}
    tree = Node(n, chance, grid, depth)
    response['can_move'] = tree.can_move
    response['grid'], response['next_possibilities'] = tree.find_next_move()
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')