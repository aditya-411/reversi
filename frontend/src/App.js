import React, { Component } from "react";
import {
    BrowserRouter as Router,
    Routes,
    Route,
} from "react-router-dom";
import Home from "./component/home.jsx";
import About from "./component/about.jsx";
import Game from "./component/Matrix.jsx";
import Result from "./component/result.jsx";
class App extends Component {
    render() {
        return (
            <Router>
                <div className="App">
                    <Routes>
                        <Route
                            path="/"
                            element={<Home />}
                        ></Route>
                        <Route
                            path="/game"
                            element={<Game />}
                        ></Route>
                        <Route
                            path="/about"
                            element={<About />}
                        ></Route>
                        <Route
                            path="/result"
                            element={<Result />}
                        ></Route>
                    </Routes>
                </div>
            </Router>
        );
    }
}

export default App;
