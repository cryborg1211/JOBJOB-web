import { useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar.jsx";
import api from "../lib/api";

type Candidate = { name?: string; avatarUrl?: string };

function Box({ label, accept, multiple, onFiles }: { label: string; accept: string; multiple?: boolean; onFiles: (files: File[])=>void }) {
  const [isOver, setIsOver] = useState(false);
  const inputRef = useRef<HTMLInputElement | null>(null);
  return (
    <div
      role="button"
      tabIndex={0}
      onClick={() => inputRef.current?.click()}
      onKeyDown={(e)=>((e.key==='Enter'||e.key===' ') && inputRef.current?.click())}
      onDragEnter={(e)=>{e.preventDefault(); setIsOver(true)}}
      onDragOver={(e)=>{e.preventDefault(); setIsOver(true)}}
      onDragLeave={()=>setIsOver(false)}
      onDrop={(e)=>{e.preventDefault(); setIsOver(false); const files = Array.from(e.dataTransfer.files||[]); if(files.length) onFiles(files)}}
      className={["h-64 sm:h-72 md:h-80 w-full rounded-3xl flex items-center justify-center transition","border-2 border-dashed", isOver?"border-emerald-300 bg-white/5":"border-cyan-300/70 bg-transparent"].join(' ')}
    >
      <div className="flex flex-col items-center gap-3">
        <svg width="36" height="36" viewBox="0 0 24 24" className="opacity-90"><path fill="currentColor" d="M12 3l4 4h-3v6h-2V7H8l4-4zm-6 12h12v2H6v-2z"/></svg>
        <p className="text-sm tracking-wide opacity-80">{label}</p>
        <input ref={inputRef} type="file" accept={accept} multiple={multiple} className="hidden" onChange={(e)=>{const files = Array.from(e.target.files||[]); if(files.length) onFiles(files)}} />
      </div>
    </div>
  );
}

export default function UploadForHR() {
  const [jdFile, setJdFile] = useState<File | null>(null);
  const [cvFiles, setCvFiles] = useState<File[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>("");
  const navigate = useNavigate();

  const canStart = Boolean(jdFile && cvFiles.length > 0);

  function handlePickJD(files: File[]) {
    const f = files[0];
    if (!f) return;
    if (f.type !== "application/pdf") {
      setError("Chỉ nhận JD dạng PDF");
      return;
    }
    setJdFile(f);
  }

  function handlePickCV(files: File[]) {
    const pdfs = files.filter(f => f.type === "application/pdf");
    if (pdfs.length !== files.length) {
      setError("Một số file không phải PDF đã bị bỏ qua");
    }
    // dedupe by name
    const merged = [...cvFiles, ...pdfs].filter((f, i, self) => self.findIndex(x => x.name === f.name) === i);
    setCvFiles(merged);
  }

  async function onStart() {
    if (!canStart || loading) return;
    setError("");
    setLoading(true);
    try {
      const batch = await api.predictBatchFiles(jdFile as File, cvFiles, 6);
      localStorage.setItem("lastBatch", JSON.stringify(batch));
      navigate("/browse", { state: { batch } });
    } catch (e: any) {
      setError(e?.message || "Không thể gọi API");
    } finally {
      setLoading(false);
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

      <section className="mx-auto w-full max-w-6xl px-4 sm:px-6 py-12 md:py-16">
        <h2 className="text-center text-3xl sm:text-4xl md:text-5xl font-extrabold">Hãy tải JD và CV để tính Độ Tương Thích</h2>
        <p className="mt-2 text-center text-white/60 text-sm">Kết quả chỉ phục vụ sàng lọc nội bộ HR</p>

        <div className="mt-10 grid grid-cols-1 sm:grid-cols-2 gap-6 md:gap-10">
          <div className="flex flex-col items-center gap-3">
            <span className="text-sm tracking-[0.18em] text-white/80">JOB DESCRIPTION</span>
            <Box label="Chỉ nhận .pdf (1 file)" accept="application/pdf" multiple={false} onFiles={handlePickJD} />
            {jdFile && <span className="text-white/70 text-xs break-all">{jdFile.name}</span>}
          </div>
          <div className="flex flex-col items-center gap-3">
            <span className="text-sm tracking-[0.18em] text-white/80">CV</span>
            <Box label="Chỉ nhận .pdf (chọn nhiều)" accept="application/pdf" multiple onFiles={handlePickCV} />
            {cvFiles.length > 0 && (
              <div className="mt-2 max-h-28 w-full overflow-auto text-xs text-white/70">
                {cvFiles.map((f) => (
                  <div key={f.name} className="truncate">• {f.name}</div>
                ))}
                <div className="mt-1 opacity-80">Tổng: {cvFiles.length} CV</div>
              </div>
            )}
          </div>
        </div>

        <div className="mt-10 flex justify-center">
          <button
            onClick={onStart}
            disabled={!canStart || loading}
            className="rounded-full bg-white text-black px-8 py-3 font-semibold tracking-wide hover:bg-white/90 active:translate-y-[1px] transition disabled:opacity-60"
          >
            {loading ? 'Đang tính...' : 'BẮT ĐẦU'}
          </button>
        </div>

        {error && (
          <div className="fixed right-4 bottom-4 rounded-xl bg-black/80 text-white px-4 py-3 border border-white/10 max-w-sm text-sm">{error}</div>
        )}
      </section>
    </div>
  );
}


