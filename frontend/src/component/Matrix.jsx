import React, { Component } from "react";
import { Navigate } from 'react-router-dom';

import "./Matrix.css";

class Matrix extends Component {
  constructor(props) {
    super(props);
    const initialMatrix = Array.from({ length: 8 }, () => Array(8).fill(0));
    initialMatrix[3][3] = initialMatrix[4][4] = -1;
    initialMatrix[3][4] = initialMatrix[4][3] = 1;
    this.state = {
      matrix: initialMatrix,
    };
  }
  sendMatrixToAPI = async (matrix, move) => {
    const input_data = {
      grid: matrix,
      current_move: move,
      depth: 6,
    };

    const request_options = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(input_data),
    };

    try {
      const response = await fetch(
        "http://127.0.0.1:5000/move/",
        request_options
      );
      const data = await response.json();
      const output = data.grid;
      console.log(data);
      return output;
    } catch (error) {
      console.error("Error fetching grid:", error);
      return null;
    }
  };

  updateCell = async (row, col) => {
    const newMatrix = this.state.matrix.map((row) => [...row]);
    const currentValue = newMatrix[row][col];
    const newValue = currentValue === -1 ? 1 : -1;
    newMatrix[row][col] = newValue;
    this.setState({ matrix: newMatrix });
    const apiResponse = await this.sendMatrixToAPI(newMatrix, [row, col]);
    console.log(apiResponse);
    if (
      apiResponse.can_move === "bad input" ||
      apiResponse.can_move === "invalid user move"
    ) {
      console.log("Invalid move:", apiResponse.can_move);
      return;
    }
    if (apiResponse.can_move === "can't_move") {
      console.log("Game Over", apiResponse.winner, "won");
      this.setState({matrix: apiResponse.grid});
      return;
    }
    this.setState({ matrix: apiResponse.grid });
  };

  render() {
    return (
      <div className="matrix">
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
                ></button>
              );
            })}
          </div>
        ))}
      </div>
    );
  }
}

export default Matrix;
