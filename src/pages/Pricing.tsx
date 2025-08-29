import { useNavigate, Link } from "react-router-dom";
import { ROUTE_CV_SCAN } from "../routes";

export default function Pricing() {
  const nav = useNavigate();

  return (
    <div className="min-h-dvh bg-[#081A17] text-white">
      {/* radial bg */}
      <div aria-hidden className="pointer-events-none fixed inset-0 -z-10 [mask-image:radial-gradient(700px_520px_at_55%_10%,black,transparent)]">
        <div className="absolute right-[-15%] top-[-20%] h-[720px] w-[720px] rounded-full bg-cyan-400/20 blur-3xl" />
        <div className="absolute left-[-10%] bottom-[-20%] h-[620px] w-[620px] rounded-full bg-emerald-500/20 blur-3xl" />
      </div>

      {/* Top bar gọn */}
      <header className="h-16 flex items-center justify-between px-6">
        <Link to="/" className="font-semibold tracking-tight hover:text-teal-300 transition-colors cursor-pointer">JobJob</Link>
        <nav className="hidden gap-8 text-sm md:flex">
          <Link to="/" className="hover:text-teal-300 transition-colors">Giới thiệu</Link>
          <Link to="/" className="hover:text-teal-300 transition-colors">Liên Hệ</Link>
          <Link to="/pricing" className="hover:text-teal-300 transition-colors">Gói Cước</Link>
          <Link to="/" className="hover:text-teal-300 transition-colors">Đăng Ký</Link>
        </nav>
      </header>

      <main className="mx-auto max-w-6xl px-6">
        <h1 className="text-center text-4xl sm:text-5xl font-extrabold leading-tight mt-2 mb-10">
          Các Hạn Mức Đăng Ký
        </h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
          {/* FREE */}
          <div className="rounded-[22px] bg-white/95 text-black p-8 shadow-[0_30px_120px_rgba(0,0,0,0.35)] flex flex-col">
            <div className="flex-1">
              <h3 className="text-lg font-extrabold tracking-[0.06em]">JOBJOB FREE</h3>
              <div className="mt-2 text-4xl font-extrabold">0 VND</div>
              <div className="mt-1 text-black/70">trong 1 tháng</div>

              <div className="mt-6">
                <p className="text-lg font-bold">Features</p>
                <ul className="mt-3 space-y-3">
                  <li className="flex items-center gap-3">
                    <span className="h-3 w-3 rounded-full bg-[#0C2F2B]" />
                    <span>12 lượt lướt phải mỗi ngày</span>
                  </li>
                </ul>
              </div>
            </div>

            <button
              onClick={() => nav("/signup")}
              className="mt-8 w-full rounded-full bg-black text-white py-3 font-semibold hover:bg-black/90"
            >
              SUBSCRIBE
            </button>
          </div>

          {/* GOLD */}
          <div className="rounded-[22px] bg-gradient-to-br from-teal-400 to-cyan-500 text-black p-8 shadow-[0_30px_120px_rgba(0,0,0,0.35)] flex flex-col">
            <div className="flex-1">
              <h3 className="text-lg font-extrabold tracking-[0.06em]">JOBJOB GOLD</h3>
              <div className="mt-2 text-4xl font-extrabold">120.000 VND</div>
              <div className="mt-1 text-black/70">trong 1 tháng</div>

              <div className="mt-6">
                <p className="text-lg font-bold">Features</p>
                <ul className="mt-3 space-y-3">
                  <li className="flex items-center gap-3">
                    <span className="h-3 w-3 rounded-full bg-[#0C2F2B]" />
                    <span>Không giới hạn lượt lướt phải</span>
                  </li>
                  <li className="flex items-center gap-3">
                    <span className="h-3 w-3 rounded-full bg-[#0C2F2B]" />
                    <span>Ưu tiên hiển thị mọi lúc</span>
                  </li>
                </ul>
              </div>
            </div>

            <button
              onClick={() => nav("/signup")}
              className="mt-8 w-full rounded-full bg-black text-white py-3 font-semibold hover:bg-black/90"
            >
              SUBSCRIBE
            </button>
          </div>
        </div>

        <div className="h-12" />
      </main>
    </div>
  );
}
