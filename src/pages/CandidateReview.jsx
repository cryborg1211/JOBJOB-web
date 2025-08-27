import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useProfile } from '../store/profile'
import Navbar from '../components/Navbar.jsx'

export default function CandidateReview() {
  const { data, updateField } = useProfile()
  const nav = useNavigate()
  const [editing, setEditing] = useState(false)

  useEffect(() => {
    if (!data) nav('/candidate/upload')
  }, [data, nav])

  if (!data) return null

  const Tag = ({ label, field }) => (
    <div className="rounded-full bg-white/10 px-6 py-3 text-white/90 border border-white/15 shadow-inner">
      {editing ? (
        <input
          className="bg-transparent outline-none text-center w-full"
          value={data[field] || ''}
          onChange={(e) => updateField(field, e.target.value)}
          placeholder={label}
        />
      ) : (
        <span className="font-semibold">{data[field] || label}</span>
      )}
    </div>
  )

  return (
    <div className="min-h-dvh bg-[#081A17] text-white">
      {/* glows */}
      <div aria-hidden className="pointer-events-none fixed inset-0 -z-10">
        <div className="absolute right-[-15%] top-[-10%] h-[520px] w-[520px] rounded-full bg-cyan-400/25 blur-3xl" />
        <div className="absolute left-[-15%] bottom-[-10%] h-[520px] w-[520px] rounded-full bg-emerald-400/25 blur-3xl" />
        <div className="absolute inset-0 [mask-image:radial-gradient(900px_500px_at_50%_15%,black,transparent)] bg-black/30" />
      </div>

      <Navbar />

      <section className="mx-auto w-full max-w-5xl px-4 sm:px-6 py-12 md:py-16 text-center">
        <h1 className="text-4xl sm:text-5xl md:text-6xl font-extralight tracking-wide">Hồ Sơ Của Bạn Đã Hoàn Tất</h1>

        <div className="mx-auto mt-10 rounded-[28px] bg-[#1CDAC4] px-6 py-10 sm:px-10 sm:py-12 max-w-lg shadow-[0_30px_120px_rgba(0,0,0,0.35)]">
          {/* avatar */}
          <div className="mx-auto mb-6 h-24 w-24 overflow-hidden rounded-full ring-4 ring-teal-300/60 shadow">
            <img
              src={data.avatar_data_url}
              alt="avatar"
              className="h-full w-full object-cover"
              draggable="false"
            />
          </div>

          <div className="grid grid-cols-1 gap-3">
            <Tag label="HỌ VÀ TÊN" field="name" />
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <Tag label="BẰNG CẤP" field="degree" />
              <Tag label="NGOẠI NGỮ" field="languagesText" />
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <Tag label="KINH NGHIỆM 1" field="exp1" />
              <Tag label="KINH NGHIỆM 2" field="exp2" />
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <Tag label="NĂNG LỰC 1" field="skill1" />
              <Tag label="NĂNG LỰC 2" field="skill2" />
            </div>
          </div>
        </div>

        <div className="mx-auto mt-10 flex max-w-lg items-center justify-between gap-4">
          <button
            onClick={() => setEditing((v) => !v)}
            className="rounded-full border border-white/30 px-8 py-3 font-semibold tracking-wide hover:bg-white/10 transition"
          >
            {editing ? 'LƯU LẠI' : 'CHỈNH SỬA'}
          </button>
          <button
            onClick={() => { console.log('CONFIRM PROFILE', data) }}
            className="rounded-full bg-emerald-400 px-8 py-3 font-semibold text-black tracking-wide hover:bg-emerald-300 transition"
          >
            XÁC NHẬN
          </button>
        </div>
      </section>
    </div>
  )
}


