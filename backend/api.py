from algo import Node
from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS, cross_origin
import numpy as np
import json


def write_lb(data):
    with open('frontend/src/final_leaderboard.json', 'w') as file:
        json.dump(data, file)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/move/', methods=['GET', 'POST'])
def move():
    data = request.get_json()
    grid = None
    n = None
    depth = None
    current_move = None

    try:
        current_move = data['current_move']
        grid = np.array(data['grid'])
        n = np.array(grid[0].size)
        depth = data['depth']
    except:
        return jsonify({"can_move":"bad input"}), 200, {'Content-Type': 'application/json'}
    response = {}
    tree = Node(n, -1, grid, 1)
    valid_move = False
    for i in [j.grid for j in tree.children]:

        if i[current_move[0], current_move[1]] == -1:
            valid_move = True
            grid = np.array(i)
            tree = Node(n, 1, grid, depth)
            break
    if not valid_move:
        return jsonify({"can_move":"invalid user move"}), 200, {'Content-Type': 'application/json'}
    
    #If bot finds no valid move for it
    if len(tree.children) == 0:
        if len(Node(tree.n, -1, tree.grid, tree.depth).children) == 0:
                if np.count_nonzero(tree.grid == 1)>np.count_nonzero(tree.grid == -1):
                    return jsonify({"can_move":"can't move", "grid":tree.grid.tolist(), "winner":"bot"}), 200, {'Content-Type': 'application/json'}
                else:
                    return jsonify({"can_move":"can't move", "grid":tree.grid.tolist(), "winner":"user"}), 200, {'Content-Type': 'application/json'}
        else:
                return jsonify({"can_move":"can move", "grid":tree.grid.tolist()}), 200, {'Content-Type': 'application/json'}

    #If bot finds a valid move for it
    next_move = tree.find_next_move()
    if len(next_move.children) >0:
        return jsonify({"can_move":"can move", "grid":next_move.grid.tolist()}), 200, {'Content-Type': 'application/json'}
    elif -1 not in next_move.grid:
        return jsonify({"can_move":"can't move", "grid":next_move.grid.tolist(), "winner":"bot"}), 200, {'Content-Type': 'application/json'}
    elif 0 not in next_move.grid:
        if np.count_nonzero(next_move.grid == 1)>np.count_nonzero(next_move.grid == -1):
            return jsonify({"can_move":"can't move", "grid":next_move.grid.tolist(), "winner":"bot"}), 200, {'Content-Type': 'application/json'}
        else:
            return jsonify({"can_move":"can't move", "grid":next_move.grid.tolist(), "winner":"user"}), 200, {'Content-Type': 'application/json'}
    else:
        while len(next_move.children) == 0:
            next_move = Node(n, 1, next_move.grid, depth).find_next_move()
            if -1 not in next_move:
                break
            if 0 not in next_move:
                if np.count_nonzero(next_move.grid == 1)>np.count_nonzero(next_move.grid == -1):
                    return jsonify({"can_move":"can't move", "grid":next_move.grid.tolist(), "winner":"bot"}), 200, {'Content-Type': 'application/json'}
                else:
                    return jsonify({"can_move":"can't move", "grid":next_move.grid.tolist(), "winner":"user"}), 200, {'Content-Type': 'application/json'}
                
        if -1 not in next_move.grid:
            return jsonify({"can_move":"can't move", "grid":next_move.grid.tolist(), "winner":"bot"}), 200, {'Content-Type': 'application/json'}
        else:
            return jsonify({"can_move":"can move", "grid":next_move.grid.tolist()}), 200, {'Content-Type': 'application/json'}


    #possible responses:
    #1) can_move: bad input (gave bad input to request)
    #2) can_move: invalid user move (the move that user tried is illegal, try again)
    #3) can_move: can't move  grid: user won   (user won the game)
    #4) can_move: can't move grid: bot won       (bot won the game)
    #5 can_move: can't move grid: opponent chance (another chance for opponent)
    #6) can_move: can move  grid: a matrix  



@app.route('/updatelb/', methods=['GET', 'POST'])
def update_leaderboard():
    data = request.get_json()
    print(data)
    data['data'].sort(key=lambda x:x['score'], reverse=True)
    write_lb(data)
    print("done")
    return "updated"


if __name__ == "__main__":
    app.run()