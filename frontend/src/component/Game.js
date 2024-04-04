import React, { useState } from 'react';
import './game.css';

const BoardGame = () => {
 const rows = 8;
 const cols = 8;

 const initialBoard = Array(rows).fill().map((_, rowIndex) =>
    Array(cols).fill().map((_, colIndex) => {
      if (rowIndex === 3 && (colIndex === 3 || colIndex === 4)) {
        return 1; 
      } else if (rowIndex === 4 && (colIndex === 3 || colIndex === 4)) {
        return -1; 
      } else {
        return 0; 
      }
    })
 );

 const [board, setBoard] = useState(initialBoard);

 const renderCell = (row, col) => {
    const cellClass = board[row][col] === 0 ? 'empty' : board[row][col] === 1 ? 'black' : 'white';

    return (
      <div
        key={`${row}-${col}`}
        className={`cell ${cellClass}`}
        onClick={() => handleCellClick(row, col)}
      >
        {/* You can render additional content here if needed */}
      </div>
    );
 };

 const renderBoard = () => {
    return (
      <div className="board">
        {board.map((row, rowIndex) => (
          <div key={rowIndex} className="row">
            {row.map((cell, colIndex) => renderCell(rowIndex, colIndex))}
          </div>
        ))}
      </div>
    );
 };

 const handleCellClick = (row, col) => {
    // Logic to handle cell clicks and add more pieces
    // This is a placeholder. You'll need to implement the game logic here.
    console.log(`Cell clicked: row ${row}, col ${col}`);
 };

 return <div>{renderBoard()}</div>;
};

export default BoardGame;
