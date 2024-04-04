import React from 'react';
import { useNavigate } from 'react-router-dom'; 
import './Home.css';

const Home = () => {
 const navigate = useNavigate(); 

 const goToAbout = () => {
    navigate('/about'); 
 };
 const goToStart = () => {
    navigate('/game'); 
 };

 return (
    <div className="home-container">
      <h1>Welcome to Othello!</h1>
      <p>
        Othello is a classic board game. The goal is to have the majority of
        disks turned to display your color when the last playable empty square
        is filled.
      </p>
      <p>To start playing, click the Start button below.</p>
      <button onClick={goToStart} className='start'>Start</button>
      <button onClick={goToAbout} className='leaderboard'>Leaderboard</button>
    </div>
 );
};

export default Home;
