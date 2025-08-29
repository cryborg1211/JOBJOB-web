import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <header className="sticky top-0 z-20 bg-[#081A17]/70 backdrop-blur-md">
      <div className="mx-auto w-full max-w-7xl px-4 sm:px-6 flex h-16 items-center justify-between">
        <Link to="/" className="text-lg md:text-xl font-semibold tracking-tight hover:text-teal-300 transition-colors">
          JobJob
          <span className="sr-only">Trang chủ JobJob</span>
        </Link>

        <nav className="hidden md:flex items-center gap-10 text-sm text-white/80">
          <Link to="/" className="hover:text-white transition-colors">Giới thiệu</Link>
          <Link to="/" className="hover:text-white transition-colors">Liên Hệ</Link>
          <Link to="/pricing" className="hover:text-white transition-colors">Gói Cước</Link>
          <Link to="/signup" className="hover:text-white transition-colors">Đăng Ký</Link>
        </nav>
      </div>
    </header>
  );
}


