import { Routes, Route } from "react-router-dom";
import LandingPage from "./pages/LandingPage.jsx";
import RoleSelect from "./pages/RoleSelect.jsx";
import CandidateReview from "./pages/CandidateReview.jsx";
import CandidateNew from "./pages/CandidateNew.jsx";
import CandidateReviewFromServer from "./pages/CandidateReviewFromServer.jsx";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/trial" element={<RoleSelect />} />
      <Route path="/candidate/new" element={<CandidateNew />} />
      <Route path="/candidate/review" element={<CandidateReview />} />
      <Route path="/candidate/review/:id" element={<CandidateReviewFromServer />} />
    </Routes>
  );
}
