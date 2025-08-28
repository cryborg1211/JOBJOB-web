import { Routes, Route } from "react-router-dom";
import LandingPage from "./pages/LandingPage.jsx";
import RoleSelect from "./pages/RoleSelect.jsx";
import CandidateReview from "./pages/CandidateReview.jsx";
import CandidateNew from "./pages/CandidateNew.jsx";
import CandidateReviewFromServer from "./pages/CandidateReviewFromServer.jsx";
import CandidateUpload from "./pages/CandidateUpload.jsx";
import EmployerUpload from "./pages/EmployerUpload.jsx";
import EmployerReview from "./pages/EmployerReview.jsx";
import EmployerReviewFromServer from "./pages/EmployerReviewFromServer.jsx";
import JobSwipe from "./pages/JobSwipe.jsx";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/trial" element={<RoleSelect />} />
      <Route path="/candidate/upload" element={<CandidateUpload />} />
      <Route path="/candidate/new" element={<CandidateNew />} />
      <Route path="/candidate/review" element={<CandidateReview />} />
      <Route path="/candidate/review/:id" element={<CandidateReviewFromServer />} />
      <Route path="/employer/upload" element={<EmployerUpload />} />
      <Route path="/employer/review" element={<EmployerReview />} />
      <Route path="/employer/review/:id" element={<EmployerReviewFromServer />} />
      <Route path="/jobs/browse" element={<JobSwipe />} />
    </Routes>
  );
}
