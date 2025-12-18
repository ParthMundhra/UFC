import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./Home";
import DivisionRankings from "./DivisionRankings";
import Fights from "./Fights";
import Navbar from "./Navbar";

function App() {
  return (
    <BrowserRouter>
      <Navbar />

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/rankings" element={<DivisionRankings />} />
        <Route path="/fights" element={<Fights />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
