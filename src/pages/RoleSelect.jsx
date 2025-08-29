import { Link } from "react-router-dom";
import Navbar from "../components/Navbar.jsx";

function ButtonPill({ to, label }) {
  return (
    <Link
      to={to}
      className="w-full min-h-[84px] rounded-full bg-teal-400 text-black 
                 font-semibold text-xl tracking-wide 
                 px-8 py-5 shadow-[0_18px_60px_rgba(0,0,0,0.35)]
                 hover:bg-teal-300 active:translate-y-[1px] 
                 transition flex items-center justify-center"
    >
      {label}
    </Link>
  );
}

export default function RoleSelect() {
  return (
    <div className="h-screen bg-[#081A17] text-white overflow-hidden">
      {/* radial glows */}
      <div aria-hidden className="pointer-events-none fixed inset-0 -z-10">
        <div className="absolute right-[-15%] top-[-10%] h-[520px] w-[520px] rounded-full bg-cyan-400/25 blur-3xl" />
        <div className="absolute left-[-15%] bottom-[-10%] h-[520px] w-[520px] rounded-full bg-emerald-400/25 blur-3xl" />
        <div className="absolute inset-0 [mask-image:radial-gradient(900px_500px_at_50%_20%,black,transparent)] bg-black/20" />
      </div>
      <Navbar />

      <section className="relative">
        <div className="mx-auto max-w-6xl px-6 py-16">
          <h1 className="text-center text-4xl sm:text-5xl font-extrabold leading-tight">
            Chào Mừng Bạn Đến Với JobJob
          </h1>
          <p className="mt-4 text-center text-3xl sm:text-4xl font-extrabold">
            Bạn Là Ai ?
          </p>

          {/* Hàng chứa 2 nút: grid 2 cột md+, 1 cột mobile */}
          <div className="mt-10 grid grid-cols-1 md:grid-cols-2 gap-8 items-stretch max-w-4xl mx-auto">
            {/* Cột 1 */}
            <div className="flex">
              <ButtonPill to="/employer/upload" label="NHÀ TUYỂN DỤNG" />
            </div>

            {/* Cột 2 */}
            <div className="flex">
              <ButtonPill to="/candidate/upload" label="ỨNG VIÊN" />
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}


