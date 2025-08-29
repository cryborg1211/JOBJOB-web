import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { ROUTE_TRIAL } from "../routes";

const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:5000";

export default function SignUp() {
  const nav = useNavigate();
  const [form, setForm] = useState({ email: "", username: "", password: "", confirm: "" });
  const [err, setErr] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  function onChange(e: React.ChangeEvent<HTMLInputElement>) {
    setForm((f) => ({ ...f, [e.target.name]: e.target.value }));
  }

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setErr(null);
    if (!form.email || !form.username || !form.password || !form.confirm) {
      setErr("Vui lòng điền đầy đủ thông tin.");
      return;
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
      setErr("Email không hợp lệ.");
      return;
    }
    if (form.password !== form.confirm) {
      setErr("Mật khẩu nhập lại chưa khớp.");
      return;
    }

    setLoading(true);
    try {
      // Nếu backend đã có API đăng ký, dùng; nếu không, vẫn điều hướng sang trial.
      await fetch(`${API_BASE}/api/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: form.email,
          username: form.username,
          password: form.password,
        }),
      }).catch(() => {}); // không chặn flow nếu backend chưa sẵn

      nav(ROUTE_TRIAL); // flow: đăng ký → trial
    } catch (e: any) {
      setErr(e?.message || "Có lỗi xảy ra, vui lòng thử lại.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-dvh bg-[#081A17] text-white">
      {/* BG glow */}
      <div aria-hidden className="pointer-events-none fixed inset-0 -z-10 [mask-image:radial-gradient(700px_520px_at_55%_10%,black,transparent)]">
        <div className="absolute right-[-15%] top-[-20%] h-[720px] w-[720px] rounded-full bg-cyan-400/20 blur-3xl" />
        <div className="absolute left-[-10%] bottom-[-20%] h-[620px] w-[620px] rounded-full bg-emerald-500/20 blur-3xl" />
      </div>

      {/* Top bar gọn */}
      <header className="h-16 flex items-center justify-between px-6">
        <Link to="/" className="font-semibold tracking-tight hover:text-teal-300 transition-colors">JobJob</Link>
        <nav className="hidden gap-8 text-sm md:flex">
          <Link to="/" className="hover:text-teal-300 transition-colors">Giới thiệu</Link>
          <Link to="/" className="hover:text-teal-300 transition-colors">Liên Hệ</Link>
          <Link to="/pricing" className="hover:text-teal-300 transition-colors">Gói Cước</Link>
          <Link to="/signup" className="hover:text-teal-300 transition-colors">Đăng Ký</Link>
        </nav>
      </header>

      {/* Grid layout */}
      <main className="mx-auto max-w-6xl px-6 py-6 md:py-10 grid grid-cols-1 md:grid-cols-2 gap-10 items-center">
        {/* Ảnh bên trái */}
        <div className="order-2 md:order-1">
          <img
            src="/src/assets/Other 08.png"
            alt=""
            className="w-full h-auto max-w-[680px] object-contain select-none pointer-events-none"
          />
        </div>

        {/* Card form bên phải */}
        <div className="order-1 md:order-2">
          <div className="rounded-[22px] bg-gradient-to-b from-teal-600/70 to-cyan-700/70 p-6 md:p-8 border border-white/10 shadow-[0_30px_120px_rgba(0,0,0,0.35)]">
            <form onSubmit={onSubmit} className="space-y-5">
              <PillInput
                name="email"
                placeholder="Nhập Mail Đăng Ký"
                type="email"
                value={form.email}
                onChange={onChange}
              />
              <PillInput
                name="username"
                placeholder="Tên Đăng Nhập"
                value={form.username}
                onChange={onChange}
              />
              <PillInput
                name="password"
                placeholder="Nhập Mật Khẩu"
                type="password"
                value={form.password}
                onChange={onChange}
              />
              <PillInput
                name="confirm"
                placeholder="Nhập Lại Mật Khẩu"
                type="password"
                value={form.confirm}
                onChange={onChange}
              />

              {err && <p className="text-red-300 text-sm">{err}</p>}

              <div className="mt-3 flex items-center gap-4">
                {/* ĐĂNG KÝ (submit) */}
                <button
                  type="submit"
                  disabled={loading}
                  className="rounded-full border border-white/60 bg-transparent px-8 py-3 font-semibold hover:bg-white/10 disabled:opacity-50"
                >
                  {loading ? "Đang đăng ký..." : "ĐĂNG KÝ"}
                </button>

                {/* ĐĂNG NHẬP (đi sang /login nếu có) */}
                <button
                  type="button"
                  onClick={() => window.location.assign("/login")}
                  className="rounded-full bg-emerald-400 px-8 py-3 font-semibold text-black hover:bg-emerald-300"
                >
                  ĐĂNG NHẬP
                </button>
              </div>
            </form>
          </div>
        </div>
      </main>
    </div>
  );
}

type PillProps = React.InputHTMLAttributes<HTMLInputElement>;
function PillInput(props: PillProps) {
  const { className = "", ...rest } = props;
  return (
    <input
      {...rest}
      className={
        "w-full rounded-full bg-black px-6 py-4 text-white placeholder:text-white/60 " +
        "border border-white/20 focus:outline-none focus:ring-2 focus:ring-teal-300/60 " +
        className
      }
    />
  );
}
