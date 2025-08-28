import { useState, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import Navbar from '../components/Navbar.jsx'
import { API_BASE } from '../lib/config'

export default function EmployerUpload() {
  return (
    <div className="min-h-dvh bg-[#081A17] text-white">
      <div aria-hidden className="pointer-events-none fixed inset-0 -z-10">
        <div className="absolute right-[-15%] top-[-10%] h-[520px] w-[520px] rounded-full bg-cyan-400/25 blur-3xl" />
        <div className="absolute left-[-15%] bottom-[-10%] h-[520px] w-[520px] rounded-full bg-emerald-400/25 blur-3xl" />
        <div className="absolute inset-0 [mask-image:radial-gradient(900px_500px_at_50%_15%,black,transparent)] bg-black/30" />
      </div>
      <Navbar />
      <section className="mx-auto w-full max-w-7xl px-4 sm:px-6 py-12 md:py-16 text-center">
        <h1 className="text-4xl sm:text-5xl md:text-6xl font-extralight tracking-wide">Chào Mừng Bạn Đến Với JobJob</h1>
        <h2 className="mt-4 text-3xl sm:text-4xl md:text-5xl font-extrabold">Hãy Tải Mô Tả Công Việc Bạn Lên Đây Nhé</h2>
        <div className="mt-12 flex justify-center"><Dropzone /></div>
      </section>
    </div>
  )
}

function Dropzone() {
  const [isOver, setIsOver] = useState(false)
  const [file, setFile] = useState(null)
  const [error, setError] = useState('')
  const inputRef = useRef(null)
  const navigate = useNavigate()

  const onFiles = async (files) => {
    setError('')
    const f = files?.[0]
    if (!f) return
    const okExt = /\.(pdf|doc|docx|txt)$/i.test(f.name)
    if (!okExt) { setError('Chỉ nhận PDF, DOC, DOCX, TXT'); return }
    if (f.size > 10*1024*1024) { setError('Tối đa 10MB'); return }
    setFile(f)
  }

  const parse = async () => {
    try {
      const form = new FormData()
      form.append('file', file)
      const res = await fetch(`${API_BASE}/api/parse-jd`, { method: 'POST', body: form })
      const json = await res.json()
      if (!res.ok || json.error) { setError(json.error || 'Không parse được JD'); return }
      
      // Map sang state tạm để fill vào review
      const norm = {
        company: json.company || '',
        title: json.title || '',
        description: json.description || '', // gộp summary + responsibilities + requirements
      };
      sessionStorage.setItem('jd_draft', JSON.stringify(norm));
      navigate('/employer/review')
    } catch (e) {
      setError('Không thể kết nối API')
    }
  }

  return (
    <div className="w-full max-w-3xl">
      <div
        role="button"
        tabIndex={0}
        onClick={()=>inputRef.current?.click()}
        onKeyDown={(e)=>((e.key==='Enter'||e.key===' ') && inputRef.current?.click())}
        onDragEnter={(e)=>{e.preventDefault(); setIsOver(true)}}
        onDragOver={(e)=>{e.preventDefault(); setIsOver(true)}}
        onDragLeave={()=>setIsOver(false)}
        onDrop={(e)=>{e.preventDefault(); setIsOver(false); onFiles(e.dataTransfer.files)}}
        className={["rounded-[32px] p-10 sm:p-14 transition","border-2 border-dashed", isOver?"border-emerald-300 bg-white/5":"border-teal-300/70 bg-white/0"].join(' ')}
      >
        {!file ? (
          <div className="flex flex-col items-center gap-4">
            <svg width="64" height="64" viewBox="0 0 24 24" className="opacity-90"><path fill="currentColor" d="M12 3l4 4h-3v6h-2V7H8l4-4zm-6 12h12v2H6v-2z"/></svg>
            <p className="text-white/80">Kéo thả PDF/DOC/DOCX/TXT vào đây hoặc bấm để chọn</p>
            <input ref={inputRef} type="file" accept=".pdf,.doc,.docx,.txt" className="hidden" onChange={(e)=>onFiles(e.target.files)} />
          </div>
        ) : (
          <div className="flex flex-col items-center gap-4">
            <p className="text-lg font-semibold">{file.name} <span className="text-white/60">({(file.size/1024/1024).toFixed(2)} MB)</span></p>
            <div className="flex gap-3">
              <button onClick={()=>setFile(null)} className="rounded-full border border-white/20 px-5 py-2 hover:bg-white/10 transition">Chọn lại</button>
              <button onClick={parse} className="rounded-full bg-emerald-400 px-5 py-2 font-medium text-black hover:bg-emerald-300 transition">Tiếp tục</button>
            </div>
          </div>
        )}
      </div>
      {error && <p className="mt-3 text-red-400">{error}</p>}
    </div>
  )
}
