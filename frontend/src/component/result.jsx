import { useLocation } from "react-router-dom";
import "./Result.css";
function ResultsPage() {
  const location = useLocation();
  const { winner } = location.state || {};

  return (
    <div>
      <h1>Results</h1>
      <p>The winner is: {winner}</p>
    </div>
  );
}

export default ResultsPage;
