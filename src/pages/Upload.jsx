import { useRef, useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { predictFiles } from '../lib/api'
import Navbar from '../components/Navbar.jsx'

function UploadBox({ label, accept, onFile }) {
  const [isOver, setIsOver] = useState(false)
  const inputRef = useRef(null)

  const handleFiles = (files) => {
    const f = files?.[0]
    if (!f) return
    onFile(f)
  }

  return (
    <div
      role="button"
      tabIndex={0}
      onClick={()=>inputRef.current?.click()}
      onKeyDown={(e)=>((e.key==='Enter'||e.key===' ') && inputRef.current?.click())}
      onDragEnter={(e)=>{e.preventDefault(); setIsOver(true)}}
      onDragOver={(e)=>{e.preventDefault(); setIsOver(true)}}
      onDragLeave={()=>setIsOver(false)}
      onDrop={(e)=>{e.preventDefault(); setIsOver(false); handleFiles(e.dataTransfer.files)}}
      className={["h-64 sm:h-72 md:h-80 w-full rounded-3xl flex items-center justify-center transition",
                  "border-2 border-dashed",
                  isOver?"border-emerald-300 bg-white/5":"border-cyan-300/70 bg-transparent"].join(' ')}
    >
      <div className="flex flex-col items-center gap-3">
        <svg width="36" height="36" viewBox="0 0 24 24" className="opacity-90">
          <path fill="currentColor" d="M12 3l4 4h-3v6h-2V7H8l4-4zm-6 12h12v2H6v-2z"/>
        </svg>
        <p className="text-sm tracking-wide opacity-80">{label}</p>
        <input ref={inputRef} type="file" accept={accept} className="hidden" onChange={(e)=>handleFiles(e.target.files)} />
      </div>
    </div>
  )
}

export default function Upload() {
  const [jdFile, setJdFile] = useState(null)
  const [cvFile, setCvFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const canStart = Boolean(jdFile && cvFile)

  const onStart = async () => {
    if (!canStart || loading) return
    setError('')
    setLoading(true)
    try {
      const data = await predictFiles({ jdFile, cvFile })
      navigate('/trial', { state: data })
    } catch (e) {
      setError(typeof e?.message === 'string' ? e.message : 'Không thể gọi API')
    } finally {
      setLoading(false)
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
      <section className="mx-auto w-full max-w-6xl px-4 sm:px-6 py-12 md:py-16 text-center">
        <h2 className="text-3xl sm:text-4xl md:text-5xl font-extrabold">Hãy Tải Tài Liệu Của Bạn Lên Đây Nhé</h2>

        <div className="mt-10 grid grid-cols-1 sm:grid-cols-2 gap-6 md:gap-10">
          <div className="flex flex-col items-center gap-3">
            <span className="text-sm tracking-[0.18em] text-white/80">JOB DESCRIPTION</span>
            <UploadBox label="Tải lên JD" accept=".pdf,.doc,.docx,.txt" onFile={setJdFile} />
            {jdFile && <span className="text-white/70 text-xs break-all">{jdFile.name}</span>}
          </div>
          <div className="flex flex-col items-center gap-3">
            <span className="text-sm tracking-[0.18em] text-white/80">CV</span>
            <UploadBox label="Tải lên CV" accept=".pdf,.doc,.docx" onFile={setCvFile} />
            {cvFile && <span className="text-white/70 text-xs break-all">{cvFile.name}</span>}
          </div>
        </div>

        <div className="mt-10 flex justify-center">
          {canStart ? (
            <button
              onClick={onStart}
              disabled={loading}
              className="rounded-full bg-white text-black px-8 py-3 font-semibold tracking-wide hover:bg-white/90 active:translate-y-[1px] transition disabled:opacity-60"
            >
              {loading ? 'Đang tính...' : 'BẮT ĐẦU'}
            </button>
          ) : (
            <button
              disabled
              className="rounded-full bg-white/70 text-black/70 px-8 py-3 font-semibold tracking-wide cursor-not-allowed"
            >
              BẮT ĐẦU
            </button>
          )}
        </div>

        <div className="mt-4 text-xs text-white/50">Hoặc <Link to="/trial" className="underline">chọn lại vai trò</Link></div>

        {error && (
          <div className="fixed right-4 bottom-4 rounded-xl bg-black/80 text-white px-4 py-3 border border-white/10 max-w-sm text-sm">
            {error}
          </div>
        )}
      </section>
    </div>
  )
}


