import React, { Component } from "react";
import "./Matrix.css";

class Matrix extends Component {
  constructor(props) {
    super(props);
    const initialMatrix = Array.from({ length: 8 }, () => Array(8).fill(0));

    for (let i = 3; i < 4; i++) {
      for (let j = 3; j < 5; j++) {
        initialMatrix[i][j] = -1;
      }
    }
    for (let i = 4; i < 5; i++) {
      for (let j = 3; j < 5; j++) {
        initialMatrix[i][j] = 1;
      }
    }

    this.state = {
      matrix: initialMatrix,
    };
  }
  sendMatrixToAPI = async (matrix) => {
    try {
       const response = await fetch('YOUR_API_ENDPOINT', {
         method: 'POST',
         headers: {
           'Content-Type': 'application/json',
         },
         body: JSON.stringify({ matrix }),
       });
   
       if (!response.ok) {
         throw new Error('Network response was not ok');
       }
   
       const data = await response.json();
       return data;
    } catch (error) {
       console.error('There was a problem with the fetch operation:', error);
    }
   };
   
   updateCell = async (row, col) => {
    const newMatrix = this.state.matrix.map((row) => [...row]);
    const currentValue = newMatrix[row][col];
    const newValue = currentValue === -1 ? 1 : -1;
    newMatrix[row][col] = newValue;
    this.setState({ matrix: newMatrix });
    const apiResponse = await this.sendMatrixToAPI(newMatrix);    
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
                cellClass += "one";
              } else if (cell === -1) {
                cellClass += "-one";
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
