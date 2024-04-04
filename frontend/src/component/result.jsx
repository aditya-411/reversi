import { useLocation } from "react-router-dom";
import "./Result.css";
function ResultsPage() {
  const location = useLocation();
  const { winner } = location.state || {};

  return (
    <div className="res">
      <h1>Results</h1>
      <p>The winner is: {winner}</p>
      <button className="leader" id="home" onClick={()=>window.location.href="/"}>Back To Home!</button>
    </div>
  );
}

export default ResultsPage;
