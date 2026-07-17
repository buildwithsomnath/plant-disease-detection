import { BrowserRouter, Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar";

import Home from "./pages/Home";
import History from "./pages/History";
import DiseaseInfo from "./pages/DiseaseInfo";

function App() {
  return (
    <BrowserRouter>
      <Navbar />

      <div className="container">
        <Routes>
          <Route path="/" element={<Home />} />

          <Route path="/history" element={<History />} />

          <Route path="/diseases" element={<DiseaseInfo />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;