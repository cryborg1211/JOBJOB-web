import { useState, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import Navbar from '../components/Navbar.jsx'
import { API_BASE } from '../lib/config'

export default function CandidateNew() {
  const [name, setName] = useState('')
  const [degree, setDegree] = useState('')
  const [languagesText, setLanguagesText] = useState('')
  const [exp1, setExp1] = useState('')
  const [exp2, setExp2] = useState('')
  const [skill1, setSkill1] = useState('')
  const [skill2, setSkill2] = useState('')
  const [avatarFile, setAvatarFile] = useState(null)
  const [avatarPreview, setAvatarPreview] = useState('')
  const [error, setError] = useState('')
  const inputRef = useRef(null)
  const navigate = useNavigate()

  const onPick = (file) => {
    if (!file) return
    const extOk = /\.(png|jpg|jpeg)$/i.test(file.name)
    if (!extOk) { setError('Chỉ nhận PNG/JPG'); return }
    if (file.size > 5 * 1024 * 1024) { setError('Ảnh tối đa 5MB'); return }
    setError('')
    setAvatarFile(file)
    const url = URL.createObjectURL(file)
    setAvatarPreview(url)
  }

  const onDrop = (e) => {
    e.preventDefault()
    onPick(e.dataTransfer.files?.[0])
  }

  const submit = async () => {
    try {
      setError('')
      const form = new FormData()
      form.append('name', name)
      form.append('degree', degree)
      form.append('languages', languagesText)
      form.append('exp1', exp1)
      form.append('exp2', exp2)
      form.append('skill1', skill1)
      form.append('skill2', skill2)
      if (avatarFile) form.append('avatar', avatarFile)
      const res = await fetch(`${API_BASE}/api/candidates`, { method: 'POST', body: form })
      const json = await res.json()
      if (!res.ok) { setError(json.error || 'Tạo hồ sơ thất bại'); return }
      navigate(`/candidate/review/${json.id}`)
    } catch (e) {
      setError('Lỗi mạng. Thử lại sau.')
    }
  }

  return (
    <div className="min-h-dvh bg-[#081A17] text-white">
      <div aria-hidden className="pointer-events-none fixed inset-0 -z-10">
        <div className="absolute right-[-15%] top-[-10%] h-[520px] w-[520px] rounded-full bg-cyan-400/25 blur-3xl" />
        <div className="absolute left-[-15%] bottom-[-10%] h-[520px] w-[520px] rounded-full bg-emerald-400/25 blur-3xl" />
        <div className="absolute inset-0 [mask-image:radial-gradient(900px_500px_at_50%_15%,black,transparent)] bg-black/30" />
      </div>

      <Navbar />

      <section className="mx-auto w-full max-w-5xl px-4 sm:px-6 py-12 md:py-16 text-center">
        <h1 className="text-4xl sm:text-5xl md:text-6xl font-extralight tracking-wide">Tạo Mới Hồ Sơ Xin Việc</h1>

        <div className="mx-auto mt-10 rounded-[28px] bg-[#1CDAC4] px-6 py-10 sm:px-10 sm:py-12 max-w-lg shadow-[0_30px_120px_rgba(0,0,0,0.35)]">
          <div
            onClick={() => inputRef.current?.click()}
            onDragOver={(e)=>e.preventDefault()}
            onDrop={onDrop}
            className="mx-auto mb-6 h-24 w-24 overflow-hidden rounded-full ring-4 ring-teal-300/60 shadow cursor-pointer bg-white/10 flex items-center justify-center"
          >
            {avatarPreview ? (
              <img src={avatarPreview} alt="avatar" className="h-full w-full object-cover" />
            ) : (
              <span className="text-black/70">Ảnh</span>
            )}
            <input ref={inputRef} type="file" accept=".png,.jpg,.jpeg" className="hidden" onChange={(e)=>onPick(e.target.files?.[0])} />
          </div>

          <div className="grid grid-cols-1 gap-3 text-black">
            <PillInput placeholder="HỌ VÀ TÊN" value={name} onChange={setName} />
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <PillInput placeholder="BẰNG CẤP" value={degree} onChange={setDegree} />
              <PillInput placeholder="NGOẠI NGỮ" value={languagesText} onChange={setLanguagesText} />
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <PillInput placeholder="KINH NGHIỆM 1" value={exp1} onChange={setExp1} />
              <PillInput placeholder="KINH NGHIỆM 2" value={exp2} onChange={setExp2} />
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <PillInput placeholder="NĂNG LỰC 1" value={skill1} onChange={setSkill1} />
              <PillInput placeholder="NĂNG LỰC 2" value={skill2} onChange={setSkill2} />
            </div>
          </div>
        </div>

        {error && <p className="mt-4 text-red-300">{error}</p>}

        <div className="mx-auto mt-10 flex max-w-lg items-center justify-center gap-4">
          <button onClick={submit} className="rounded-full bg-emerald-400 px-8 py-3 font-semibold text-black tracking-wide hover:bg-emerald-300 transition">XÁC NHẬN</button>
        </div>
      </section>
    </div>
  )
}

function PillInput({ placeholder, value, onChange }) {
  return (
    <input
      className="rounded-full bg-white/10 px-6 py-3 text-center border border-white/15 focus:border-white/40 outline-none placeholder:text-white/60"
      placeholder={placeholder}
      value={value}
      onChange={(e)=>onChange(e.target.value)}
    />
  )
}


