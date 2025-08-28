import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import Navbar from '../components/Navbar.jsx'
import { API_BASE } from '../lib/config'

export default function EmployerReviewFromServer() {
  const { id } = useParams()
  const [data, setData] = useState(null)
  const [editing, setEditing] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    fetch(`${API_BASE}/api/jobs/${id}`).then(r=>r.json()).then(setData)
  }, [id])

  if (!data) return null

  const save = async () => {
    const res = await fetch(`${API_BASE}/api/jobs/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        company: data.company,
        title: data.title,
        description: data.description,
      })
    })
    const json = await res.json()
    if (!res.ok) { setError(json.error || 'Cập nhật thất bại'); return }
    setEditing(false)
    setData(json)
  }

  const Tag = ({ label, field, variant = "short" }) => {
    const base = "border border-black/10 shadow-inner text-black";
    const common = variant === "short"
      ? "rounded-full min-h-14 px-6 py-3"
      : "rounded-2xl px-5 py-4 whitespace-pre-wrap break-words max-h-36 overflow-auto";
    
    return (
      <div className={`bg-white/90 ${base} ${common}`}>
        {editing ? (
          <textarea
            rows={variant === "short" ? 1 : 3}
            className="w-full resize-none bg-transparent outline-none text-center caret-black placeholder:text-black/50"
            value={data[field] || ""}
            onChange={e => setData(prev => ({...prev, [field]: e.target.value}))}
            placeholder={label}
          />
        ) : (
          <span className="font-semibold block text-center">{data[field] || label}</span>
        )}
      </div>
    );
  };

  const LongDescription = ({ label, field }) => (
    <div className="rounded-2xl bg-white/90 text-black px-5 py-4 border border-black/10 shadow-inner whitespace-pre-wrap break-words min-h-40">
      {editing ? (
        <textarea
          rows={8}
          className="w-full resize-none bg-transparent outline-none text-center caret-black placeholder:text-black/50 min-h-40"
          value={data[field] || ""}
          onChange={e => setData(prev => ({...prev, [field]: e.target.value}))}
          placeholder={label}
        />
      ) : (
        <span className="font-semibold block text-center">{data[field] || label}</span>
      )}
    </div>
  );

  return (
    <div className="min-h-dvh bg-[#081A17] text-white">
      <div aria-hidden className="pointer-events-none fixed inset-0 -z-10">
        <div className="absolute right-[-15%] top-[-10%] h-[520px] w-[520px] rounded-full bg-cyan-400/25 blur-3xl" />
        <div className="absolute left-[-15%] bottom-[-10%] h-[520px] w-[520px] rounded-full bg-emerald-400/25 blur-3xl" />
        <div className="absolute inset-0 [mask-image:radial-gradient(900px_500px_at_50%_15%,black,transparent)] bg-black/30" />
      </div>
      <Navbar />
      <section className="mx-auto w-full max-w-5xl px-4 sm:px-6 py-12 md:py-16 text-center">
        <h1 className="text-4xl sm:text-5xl md:text-6xl font-extralight tracking-wide">Mô Tả Công Việc</h1>
        <div className="mx-auto mt-10 rounded-[28px] bg-[#1CDAC4] px-6 py-10 sm:px-10 sm:py-12 max-w-2xl shadow-[0_30px_120px_rgba(0,0,0,0.35)]">
          <div className="mx-auto mb-6 h-24 w-24 overflow-hidden rounded-full ring-4 ring-teal-300/60 shadow bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
            {data.company ? <span className="text-3xl font-bold text-white">{data.company.charAt(0).toUpperCase()}</span> : <div />}
          </div>
          <div className="grid grid-cols-1 gap-3">
            <Tag label="TÊN CÔNG TY" field="company" />
            <Tag label="VỊ TRÍ" field="title" />
            <LongDescription label="MÔ TẢ CÔNG VIỆC" field="description" />
          </div>
        </div>
        {error && <p className="mt-4 text-red-300">{error}</p>}
        <div className="mx-auto mt-10 flex max-w-lg items-center justify-between gap-4">
          <button onClick={()=>setEditing(v=>!v)} className="rounded-full border border-white/30 px-8 py-3 font-semibold tracking-wide hover:bg-white/10 transition">{editing?'LƯU LẠI':'CHỈNH SỬA'}</button>
          {editing && <button onClick={save} className="rounded-full bg-emerald-400 px-8 py-3 font-semibold text-black tracking-wide hover:bg-emerald-300 transition">LƯU</button>}
        </div>
      </section>
    </div>
  )
}
