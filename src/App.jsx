import { Routes, Route } from "react-router-dom";
import LandingPage from "./pages/LandingPage.jsx";
import RoleSelect from "./pages/RoleSelect.jsx";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/trial" element={<RoleSelect />} />
    </Routes>
  );
}
