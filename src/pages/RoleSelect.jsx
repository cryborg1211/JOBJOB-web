import { Link } from "react-router-dom";
import Navbar from "../components/Navbar.jsx";

function ButtonPill({ to, label }) {
  return (
    <Link
      to={to}
      className="inline-flex items-center justify-center rounded-full bg-gradient-to-r from-teal-400 to-emerald-400 px-10 py-5 text-base sm:text-lg font-semibold text-black tracking-wide shadow-[0_10px_40px_rgba(0,0,0,0.3)] hover:brightness-105 active:translate-y-px focus:outline-none focus-visible:ring-2 focus-visible:ring-white/60 transition"
    >
      {label}
    </Link>
  );
}

export default function RoleSelect() {
  return (
    <div className="min-h-dvh bg-[#081A17] text-white">
      {/* radial glows */}
      <div aria-hidden className="pointer-events-none fixed inset-0 -z-10">
        <div className="absolute right-[-15%] top-[-10%] h-[520px] w-[520px] rounded-full bg-cyan-400/25 blur-3xl" />
        <div className="absolute left-[-15%] bottom-[-10%] h-[520px] w-[520px] rounded-full bg-emerald-400/25 blur-3xl" />
        <div className="absolute inset-0 [mask-image:radial-gradient(900px_500px_at_50%_20%,black,transparent)] bg-black/20" />
      </div>
      <Navbar />

      <section className="mx-auto w-full max-w-7xl px-4 pt-8 pb-20 flex flex-col items-center justify-center min-h-[calc(100svh-4rem)] text-center">
        <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-extralight tracking-wide">
          Chào Mừng Bạn Đến Với JobJob
        </h1>
        <h2 className="mt-6 text-4xl sm:text-5xl md:text-6xl font-extrabold">
          Bạn Là Ai ?
        </h2>

        <div className="mt-12 flex flex-col gap-6 sm:flex-row sm:justify-center">
          <ButtonPill to="/signup?role=recruiter" label="NHÀ TUYỂN DỤNG" />
          <ButtonPill to="/candidate/upload" label="ỨNG VIÊN" />
        </div>
      </section>
    </div>
  );
}


