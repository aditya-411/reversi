import React, { Component, us } from "react";
import { Navigate } from "react-router-dom";
import "./Matrix.css";
import "./Popup.css";
import data from '../leaderboard.json'

var players = data["data"];
players.sort();

class Matrix extends Component {
  constructor(props) {
    super(props);
    const initialMatrix = Array.from({ length: 8 }, () => Array(8).fill(0));
    initialMatrix[3][3] = initialMatrix[4][4] = -1;
    initialMatrix[3][4] = initialMatrix[4][3] = 1;
    this.state = {
      matrix: initialMatrix,
      redirectToResult: false,
      showPopup: false,
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
      return data;
    } catch (error) {
      console.error("Error fetching grid:", error);
      return null;
    }
  };

  updateCell = async (row, col) => {
    const newMatrix = this.state.matrix.map((row) => [...row]);
    const currentValue = newMatrix[row][col];
    if (currentValue !== 0) {
      return;
    }
    // const newValue = currentValue === -1 ? 1 : -1;
    // newMatrix[row][col] = newValue;

    function countOccurrences(arr, target) {
      let count = 0;
      
      for (let i = 0; i < arr.length; i++) {
        for (let j = 0; j < arr[i].length; j++) {
          if (arr[i][j] === target) {
            count++;
          }
        }
      }
      
      return count;
    }


    this.setState({ matrix: newMatrix });
    const apiResponse = await this.sendMatrixToAPI(newMatrix, [row, col]);
    console.log(apiResponse);
    if (
      apiResponse.can_move === "bad input" ||
      apiResponse.can_move === "invalid user move"
    ) {
      console.log("Invalid move:", apiResponse.can_move);
      this.setState({ showPopup: true });
      return;
    }
    if (apiResponse.can_move === "can't move") {
      console.log("Game Over", apiResponse.winner, "won");
      if (apiResponse.winner === "user") {
        players.concat({"name": "You", "score": (countOccurrences(apiResponse.grid, -1)-countOccurrences(apiResponse.grid, 1))*100});
        const input_data = {
          array: players
        };
    
        const request_options = {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(input_data),
        };

        try {
          await fetch(
            "http://127.0.0.1:5000/updatelb/",
            request_options
          );
        } catch (error) {
          console.error("Error fetching grid:", error);
          return null;
        }

    }
      this.setState({
        matrix: apiResponse.grid,
        redirectToResult: true,
        winner: apiResponse.winner,
      });
      return;
    }

    this.setState({ matrix: apiResponse.grid });
  };
  closePopup=()=>{
    console.log('close')
    this.setState({ showPopup: false });
    
  };
  render() {
    const { redirectToResult, winner } = this.state;

    if (redirectToResult) {
      return <Navigate to="/result" state={{ winner }} replace />;
    }

    return (
      <div className="gamepage">
        {this.state.showPopup && (
          <div className="popup-container">
          <div className="popup-body">
            <h1>Invalid Move</h1>
            <button onClick={this.closePopup}>Close X</button>
          </div>
        </div>
         
        )}
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
      </div>
    );
  }
}

export default Matrix;