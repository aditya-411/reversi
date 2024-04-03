import React from "react";

const GameBoard = ({ board, onMove }) => {
  const handleClick = (row, col) => {
    onMove(row, col);
  };

  return (
    <div>
      {board.map((row, rowIndex) => (
        <div key={rowIndex}>
          {row.map((cell, colIndex) => (
            <div
              key={colIndex}
              onClick={() => handleClick(rowIndex, colIndex)}
              style={{
                width: "50px",
                height: "50px",
                border: "1px solid black",
              }}
            >
              {cell}
            </div>
          ))}
        </div>
      ))}
    </div>
  );
};

export default GameBoard;
