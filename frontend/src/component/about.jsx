import React from 'react';
import './Leaderboard.css'; 
import data from '../final_leaderboard.json'


const Leaderboard = () => {
const players = data["data"];
console.log(players);

 return (
    <div className="leaderboard">
      <h2>Leaderboard</h2>
      <table>
        <thead>
          <tr>
            <th>Rank</th>
            <th>Name</th>
            <th>Score</th>
          </tr>
        </thead>
        <tbody>
          {players.map((player, index) => (
            <tr key={index}>
              <td>{index + 1}</td>
              <td>{player.name}</td>
              <td>{player.score}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
 );
};

export default Leaderboard;
