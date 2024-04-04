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
      'current_move': move 
    };

    console.log("step 1");

    const request_options = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(input_data)
    }
    console.log("step 2");


    fetch('/move/', request_options)
      .then(response => response.json())
      .then(data => console.log(data))
      .catch(error => console.error(error))

      console.log("step 3")
   };

   
   updateCell = async (row, col) => {
    const newMatrix = this.state.matrix.map((row) => [...row]);
    const currentValue = newMatrix[row][col];
    const newValue = currentValue === -1 ? 1 : -1;
    newMatrix[row][col] = newValue;
    this.setState({ matrix: newMatrix });
    console.log(".")
    const apiResponse = await this.sendMatrixToAPI(newMatrix, [row, col]);    
    console.log(".")
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
