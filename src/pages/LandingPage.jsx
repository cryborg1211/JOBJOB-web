import { Link } from "react-router-dom";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-[#071a1d] text-white">
      {/* Header */}
      <header className="fixed top-0 inset-x-0 z-50 bg-transparent">
        <div className="mx-auto max-w-7xl px-6 py-6 flex items-center justify-between">
          <div className="text-white font-extrabold text-xl">JobJob</div>
          <nav className="hidden md:flex items-center gap-10 text-sm text-white/80">
            <a href="#" className="hover:text-white">Giới thiệu</a>
            <a href="#" className="hover:text-white">Liên Hệ</a>
            <a href="#" className="hover:text-white">Gói Cước</a>
            <a href="#" className="hover:text-white">Đăng Ký</a>
          </nav>
        </div>
      </header>

      {/* Hero */}
      <section className="relative pt-32">
        <div className="absolute inset-0 -z-10 bg-[radial-gradient(1200px_600px_at_20%_0%,#1bd2c5_0%,#0d3237_40%,#071a1d_60%)]" />
        <div className="mx-auto max-w-7xl px-6 pb-24">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div>
              <h1 className="text-5xl md:text-6xl leading-tight font-extrabold tracking-tight">
                Lướt Để Tìm<br/>Việc, Match<br/>Để Thành<br/>Công
              </h1>
              <p className="mt-6 text-white/70 max-w-xl">Lướt trái bỏ qua, quẹt phải là có việc – JobJob, nơi cơ hội tìm đến bạn chỉ sau một cú click</p>
              <div className="mt-8 flex gap-4">
                <button className="px-6 py-3 rounded-full bg-emerald-400 text-slate-900 font-semibold">SUBSCRIBE</button>
                <Link to="/trial" className="rounded-full border border-white/25 px-6 py-3 font-medium hover:border-white/60 hover:bg-white/5 transition">FREE TRIAL</Link>
              </div>
            </div>
            <div className="flex justify-center lg:justify-end">
              <div className="w-[420px] h-[380px] bg-gradient-to-br from-indigo-400/20 to-cyan-300/20 rounded-3xl border border-white/10 backdrop-blur-sm shadow-[0_0_120px_rgba(27,210,197,0.25)]" />
            </div>
          </div>
          <div className="mt-14 text-white/60 text-sm">Featured on</div>
          <div className="mt-6 grid grid-cols-2 sm:grid-cols-4 md:grid-cols-6 gap-6 opacity-80">
            {['TechCrunch','FastCompany','MIT','Forbes','WIRED','TheVerge'].map((x)=> (
              <div key={x} className="h-8 rounded bg-white/5 border border-white/10 flex items-center justify-center text-xs text-white/60">{x}</div>
            ))}
          </div>
        </div>
      </section>

      {/* Matching section */}
      <section className="py-24 bg-[#051416]">
        <div className="mx-auto max-w-7xl px-6 grid lg:grid-cols-2 gap-16 items-center">
          <div className="flex justify-center">
            <div className="w-[360px] h-[280px] rounded-3xl bg-gradient-to-b from-violet-400/20 to-blue-300/10 border border-white/10" />
          </div>
          <div>
            <p className="text-emerald-300/80 mb-3">Thuật toán thông minh</p>
            <h2 className="text-4xl md:text-5xl font-extrabold leading-tight">Kết Nối Các<br/>Hồ Sơ Làm<br/>Việc Phù Hợp<br/>Với Mô Tả</h2>
            <p className="mt-6 text-white/70 max-w-xl">Áp dụng thuật toán matching vào quá trình recommend việc làm phù hợp với hồ sơ người dùng</p>
            <button className="mt-8 px-6 py-3 rounded-full bg-emerald-400 text-slate-900 font-semibold">SUBSCRIBE</button>
          </div>
        </div>
      </section>

      {/* Remove manual screening section */}
      <section className="py-24 bg-[#061a1d]">
        <div className="mx-auto max-w-7xl px-6 grid lg:grid-cols-2 gap-16 items-center">
          <div>
            <p className="text-white/60">Tối ưu hoá quá trình tuyển dụng</p>
            <h2 className="mt-4 text-4xl md:text-5xl font-extrabold leading-tight">Loại Bỏ Quá<br/>Trình Sàn<br/>Lọc Bằng<br/>Tay Cho Nhà<br/>Tuyển Dụng</h2>
            <p className="mt-6 text-white/70 max-w-xl">Tiết kiệm thời gian trong quy trình sàn lọc CV của ứng viên</p>
            <button className="mt-8 px-6 py-3 rounded-full bg-emerald-400 text-slate-900 font-semibold">SUBSCRIBE</button>
          </div>
          <div className="grid gap-4">
            <div className="h-16 rounded-2xl bg-gradient-to-r from-sky-400/20 to-violet-400/20 border border-white/10" />
            <div className="h-16 rounded-2xl bg-gradient-to-r from-sky-400/20 to-violet-400/20 border border-white/10" />
            <div className="h-16 rounded-2xl bg-white/10 border border-white/10" />
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-24">
        <div className="mx-auto max-w-7xl px-6">
          <div className="rounded-[32px] p-12 md:p-16 bg-gradient-to-r from-cyan-400/30 to-blue-500/30 border border-white/10">
            <p className="text-center text-emerald-200/90">BẠN ĐÃ SẴN SÀNG CHƯA?</p>
            <h3 className="mt-3 text-center text-4xl md:text-5xl font-extrabold">Tuyển Dụng Thời Đại<br/>Mới, Bắt Đầu Từ Bạn</h3>
            <div className="mt-8 flex justify-center">
              <button className="px-6 py-3 rounded-full bg-black/70 text-white border border-white/10">Xem Các Gói Thành Viên</button>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-16 border-t border-white/10 bg-[#071a1d]">
        <div className="mx-auto max-w-7xl px-6 grid md:grid-cols-3 gap-10 text-sm text-white/70">
          <div>
            <div className="text-white font-extrabold text-lg">JobJob</div>
          </div>
          <div>
            <div className="font-semibold text-white mb-3">Liên Hệ</div>
            <ul className="space-y-2">
              <li>Email</li>
              <li>LinkedIn</li>
              <li>Instagram</li>
            </ul>
          </div>
          <div>
            <div className="font-semibold text-white mb-3">Không bỏ lỡ bất kỳ cập nhật nào</div>
            <div className="flex items-center gap-2">
              <input className="flex-1 px-4 py-2 rounded-full bg-white/5 border border-white/10 outline-none" placeholder="Nhập email của bạn ở đây" />
              <button className="px-5 py-2 rounded-full bg-white text-slate-900 font-semibold">Gửi</button>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}


