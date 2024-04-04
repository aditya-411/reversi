from algo import Node
from flask import Flask, jsonify, request, render_template, send_from_directory
import numpy as np




app = Flask(__name__)

@app.route('/move/', methods=['GET', 'POST'])
def return_move():
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
        return jsonify({"can_move":"bad input"})
    response = {}
    tree = Node(n, -1, grid, 1)
    x, user_possible_moves = tree.find_next_move()
    valid_move = False
    for i in user_possible_moves:
        if i[current_move[0], current_move[1]] == -1:
            valid_move = True
            grid = np.array(i)
            node = Node(n, 1, grid, depth)
    if not valid_move:
        return jsonify({"can_move":"invalid user move"})
    response['can_move'] = tree.can_move
    response['grid'], next_possibilities = tree.find_next_move()
    if response['grid'] == "game over":
        response['grid'] = "user won"
    elif next_possibilities == 0:
        response['grid'] = "bot won"
    return jsonify(response)

    #possible responses:
    #1) can_move: bad input (gave bad input to request)
    #2) can_move: invalid user move (the move that user tried is illegal, try again)
    #3) can_move: can't move  grid: user won   (user won the game)
    #4) can_move: can move grid: bot won       (bot won the game)
    #5 can_move: can't move grid: opponent chance (another chance for opponent)
    #6) can_move: can move  grid: a matrix  
if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')