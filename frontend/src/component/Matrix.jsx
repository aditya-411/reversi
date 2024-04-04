import React, { Component } from "react";
import "./Matrix.css";

class Matrix extends Component {
  constructor(props) {
    super(props);
    const initialMatrix = Array.from({ length: 8 }, () => Array(8).fill(0));
    
    initialMatrix[3][3]= initialMatrix[4][4] = -1
    initialMatrix[3][4] = initialMatrix[4][3] = 1

    this.state = {
      matrix: initialMatrix,
    };
  }
  sendMatrixToAPI = async (matrix, move) => {
    const input_data = {
      'grid' : matrix,
      'current_move': move,
      'depth' : 6,
    };


    const request_options = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(input_data)
    }

    var output;


    fetch('http://127.0.0.1:5000/move/', request_options)
      .then(response => response.json())
      .then(data => {
        output = data;
       })
      .then(() => {
        console.log(output);
       });

   };

   
   updateCell = async (row, col) => {
    const newMatrix = this.state.matrix.map((row) => [...row]);
    const currentValue = newMatrix[row][col];
    const newValue = currentValue === -1 ? 1 : -1;
    newMatrix[row][col] = newValue;
    this.setState({ matrix: newMatrix });
    const apiResponse = await this.sendMatrixToAPI(newMatrix, [row, col]);    
    this.setState({ matrix: apiResponse });
   };

  render() {
    return (
      <div>
        {this.state.matrix.map((row, rowIndex) => (
          <div key={rowIndex}>
            {row.map((cell, colIndex) => {
              let cellClass = "cell ";
              if (cell === 0) {
                cellClass += "empty";
              } else if (cell === 1) {
                cellClass += "-one";
              } else if (cell === -1) {
                cellClass += "one";
              }
              return (
                <button
                  key={colIndex}
                  className={cellClass}
                  onClick={() => this.updateCell(rowIndex, colIndex)}
                >
                </button>
              );
            })}
          </div>
        ))}
      </div>
    );
  }
}

export default Matrix;
