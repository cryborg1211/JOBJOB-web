import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useProfile } from '../store/profile'

function Pill({ children }) {
  return (
    <div className="rounded-full bg-white/90 text-black px-6 py-3 border border-black/10 shadow-inner text-center font-semibold truncate">
      {children}
    </div>
  );
}

function InfoBox({ children }) {
  // ô nội dung dài nhưng KHÔNG scroll, chỉ ẩn tràn để card không quá cao
  return (
    <div className="rounded-[18px] bg-[#0EA89A] text-white/95 px-5 py-4 
                    max-h-[140px] overflow-hidden whitespace-pre-wrap break-words">
      {children}
    </div>
  );
}

export default function CandidateReview() {
  const { data, updateField } = useProfile()
  const nav = useNavigate()
  const [editing, setEditing] = useState(false)

  useEffect(() => {
    if (!data) nav('/candidate/upload')
  }, [data, nav])

  if (!data) return null

  return (
    <div className="min-h-dvh bg-[#081A17] text-white">
      {/* radial bg */}
      <div aria-hidden className="pointer-events-none fixed inset-0 -z-10 
          [mask-image:radial-gradient(700px_520px_at_55%_10%,black,transparent)]">
        <div className="absolute right-[-15%] top-[-20%] h-[720px] w-[720px] rounded-full bg-cyan-400/20 blur-3xl" />
        <div className="absolute left-[-10%] bottom-[-20%] h-[620px] w-[620px] rounded-full bg-emerald-500/20 blur-3xl" />
      </div>

      <div className="mx-auto max-w-6xl px-6">
        {/* Header */}
        <header className="h-16 flex items-center justify-between">
          <div className="font-semibold tracking-tight">JobJob</div>
          <nav className="hidden gap-8 text-sm md:flex">
            <a className="hover:text-teal-300 transition-colors" href="#gioi-thieu">Giới thiệu</a>
            <a className="hover:text-teal-300 transition-colors" href="#lien-he">Liên Hệ</a>
            <a className="hover:text-teal-300 transition-colors" href="#goi-cuoc">Gói Cước</a>
            <a className="hover:text-teal-300 transition-colors" href="#dang-ky">Đăng Ký</a>
          </nav>
        </header>

        <h1 className="text-center text-4xl sm:text-5xl font-extrabold leading-tight mt-2 mb-8">
          Hồ Sơ Của Bạn Đã Hoàn Tất
        </h1>

        {/* CARD rộng hơn + thấp hơn */}
        <div className="mx-auto w-full max-w-[1000px] rounded-[28px] bg-[#1CDAC4] 
                        px-6 pt-6 pb-0 shadow-[0_30px_120px_rgba(0,0,0,0.35)]">
          {/* Avatar */}
          <div className="mx-auto mb-4 h-20 w-20 rounded-full bg-white/90 text-black 
                          grid place-items-center text-2xl font-bold ring-4 ring-white/30">
            {data.avatar_data_url ? (
              <img src={data.avatar_data_url} className="h-20 w-20 rounded-full object-cover" alt="avatar" />
            ) : (
              (data.name?.slice(0,1) ?? 'U').toUpperCase()
            )}
          </div>

          {/* Name full width (pill) */}
          <Pill>{data.name || "Họ và tên"}</Pill>

          {/* GRID 2 cột: kéo ngang, không cao */}
          <div className="mt-5 grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Các ô ngắn dạng pill */}
            <Pill>{data.degree || "Bằng cấp"}</Pill>
            <Pill>{data.languagesText || "Ngoại ngữ"}</Pill>

            {/* Các ô dài: dùng InfoBox, KHÔNG có thanh scroll */}
            <InfoBox>
              {data.exp1 || "Kinh nghiệm 1"}
            </InfoBox>
            <InfoBox>
              {data.exp2 || "Kinh nghiệm 2"}
            </InfoBox>

            {/* tuỳ bạn thêm các mục khác: kỹ năng, thành tựu, v.v. */}
            <Pill>{data.skill1 || "Năng lực 1"}</Pill>
            <Pill>{data.skill2 || "Năng lực 2"}</Pill>
          </div>

          {/* Action bar STICKY bên trong card để NÚT LUÔN HIỆN */}
          <div className="sticky bottom-0 -mx-6 mt-6 rounded-b-[28px] 
                          bg-gradient-to-t from-[#1CDAC4] to-[#1CDAC4]/80 
                          backdrop-blur px-6 py-4">
            <div className="flex items-center justify-between">
              <button
                type="button"
                className="rounded-full border border-black/20 bg-white/80 text-black 
                           px-6 py-2.5 font-medium hover:bg-white"
                onClick={() => setEditing((v) => !v)}
              >
                {editing ? 'LƯU LẠI' : 'CHỈNH SỬA'}
              </button>
              <button
                type="button"
                className="rounded-full bg-black text-white px-8 py-2.5 font-semibold 
                           hover:bg-black/90"
                onClick={() => nav("/jobs/browse")}
              >
                XÁC NHẬN
              </button>
            </div>
          </div>
        </div>

        <div className="h-10" />
      </div>
    </div>
  );
}


