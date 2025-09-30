import { useEffect, useRef, useState, useMemo } from "react";
import { useLocation } from "react-router-dom";
import { motion, useMotionValue, useTransform, AnimatePresence, useAnimation } from "framer-motion";
import { API_BASE } from "../lib/config";

// ========= Chat Sidebar (placeholder) =========
function ChatSidebar() {
  return (
    <aside className="hidden lg:block w-[280px] shrink-0 h-dvh sticky top-0 bg-gradient-to-b from-[#0D2D2A] to-[#0E3631] border-r border-white/5">
      <div className="px-5 pt-4 pb-3 flex items-center justify-between">
        <div className="h-9 w-9 rounded-full border-2 border-teal-400/70" />
        <div className="h-6 w-8 rounded bg-teal-400/30" />
      </div>
      <div className="px-5 text-sm text-white/60">Chat (sắp ra mắt)</div>
      <div className="px-5 mt-3 space-y-3">
        {Array.from({ length: 6 }).map((_, i) => (
          <div key={i} className="rounded-xl bg-white/5 h-14 border border-white/5" />
        ))}
      </div>
    </aside>
  );
}

// ========= Card riêng lẻ =========
function JobCard({ job, draggingX, onDragEnd, overrideScore, overrideFeatures }) {
  // Avatar = ký tự đầu công ty
  const avatar = (job.company || "?").slice(0, 1).toUpperCase();
  return (
    <motion.div
      className="relative mx-auto w-full max-w-[720px] rounded-[28px] bg-[#1CDAC4] px-6 pb-8 pt-4 shadow-[0_30px_120px_rgba(0,0,0,0.35)]"
      style={{ x: draggingX }}
      drag="x"
      dragConstraints={{ left: 0, right: 0 }}
      onDragEnd={onDragEnd}
    >
      {/* Badge độ tương thích (placeholder) */}
      <div className="absolute right-6 top-4 rounded-full bg-white/70 text-black/80 px-4 py-1 text-[13px] font-semibold">
        Độ tương thích: {overrideScore?.percent || '—%'}
      </div>

      {/* Avatar */}
      <div className="mx-auto mt-4 mb-4 h-20 w-20 rounded-full bg-white/90 text-black grid place-items-center text-2xl font-bold ring-4 ring-white/30">
        {avatar}
      </div>

      {/* Company */}
      <div className="rounded-full bg-white/90 text-black px-6 py-3 border border-black/10 shadow-inner text-center font-semibold">
        {job.company || "Tên công ty"}
      </div>

      {/* Title */}
      <div className="mt-3 rounded-full bg-white/90 text-black px-6 py-3 border border-black/10 shadow-inner text-center">
        {job.title || "Vị trí"}
      </div>

             {/* Description */}
       <div className="mt-4 rounded-[18px] bg-[#0EA89A] text-white/95 px-5 py-4 min-h-32 max-h-32 whitespace-pre-wrap break-words overflow-hidden">
         {overrideFeatures && overrideFeatures.length ? overrideFeatures.join(' • ') : (job.description || "Mô tả công việc")}
       </div>
    </motion.div>
  );
}

// ========= Stack 3 thẻ =========
function Deck({ queue, peekBlurPx, onSwipe, overrideScore, overrideFeatures }) {
  // Top 3 items hiển thị
  const cards = useMemo(() => queue.slice(0, 3), [queue]);

  // motion cho card trên cùng
  const x = useMotionValue(0);
  const rotate = useTransform(x, [-220, 0, 220], [-11, 0, 11]);

  // Khi kết thúc kéo
  function handleDragEnd(_, info) {
    if (info.offset.x > 120) onSwipe("apply");  // phải
    else if (info.offset.x < -120) onSwipe("skip");  // trái
    else x.set(0);
  }

  return (
    <div className="relative w-full max-w-[760px] mx-auto">
      {/* Card thứ 3 (xa nhất) */}
      {cards[2] && (
        <motion.div
          className="absolute inset-0 flex items-start justify-center pointer-events-none"
          style={{ filter: `blur(${peekBlurPx}px)` }}
          initial={{ y: 60, scale: 0.94, opacity: 0.85 }}
          animate={{ y: 60, scale: 0.94, opacity: 0.85 }}
        >
          <div className="w-full">
                         <div className="mx-auto w-full max-w-[720px] rounded-[28px] bg-[#0FBCA9] h-[320px]" />
          </div>
        </motion.div>
      )}

      {/* Card thứ 2 */}
      {cards[1] && (
        <motion.div
          className="absolute inset-0 flex items-start justify-center pointer-events-none"
          style={{ filter: `blur(${Math.max(peekBlurPx - 2, 3)}px)` }}
          initial={{ y: 34, scale: 0.97, opacity: 0.92 }}
          animate={{ y: 34, scale: 0.97, opacity: 0.92 }}
        >
          <div className="w-full">
                         <div className="mx-auto w-full max-w-[720px] rounded-[28px] bg-[#11CDB4] h-[340px]" />
          </div>
        </motion.div>
      )}

      {/* Card trên cùng (draggable) */}
      {cards[0] && (
        <motion.div style={{ rotate }} className="relative">
          <JobCard job={cards[0]} draggingX={x} onDragEnd={handleDragEnd} overrideScore={overrideScore} overrideFeatures={overrideFeatures} />
        </motion.div>
      )}
    </div>
  );
}

export default function JobSwipe() {
  const [queue, setQueue] = useState([]);
  const [offset, setOffset] = useState(0);
  const [loading, setLoading] = useState(false);
  const location = useLocation();
  const stateData = location && location.state;
  const persisted = (() => { 
    try { 
      return JSON.parse(localStorage.getItem('lastMatch')||'null') || JSON.parse(localStorage.getItem('lastResult')||'null'); 
    } catch { return null } 
  })();
  const scoreData = stateData || persisted || null;

  async function fetchMore() {
    if (loading) return;
    setLoading(true);
    try {
      const r = await fetch(`${API_BASE}/api/jobs?offset=${offset}&limit=12`);
      const j = await r.json();
      setQueue((q) => [...q, ...(j.items || [])]);
      setOffset(j.nextOffset ?? offset);
    } catch (error) {
      console.error('❌ Fetch error:', error);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchMore();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function sendDecision(job, action) {
    try {
      await fetch(`${API_BASE}/api/decisions`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ job_id: job.id, action }),
      });
    } catch {}
  }

  function handleSwipe(action) {
    const job = queue[0];
    if (!job) return;
    // loại bỏ thẻ đầu
    setQueue((q) => q.slice(1));
    sendDecision(job, action);
    if (queue.length < 5) fetchMore();
  }

  const top = queue[0];

  return (
         <div className="h-screen bg-[#081A17] text-white relative overflow-hidden">
      {/* radial gradient bg */}
      <div
        aria-hidden
        className="pointer-events-none fixed inset-0 -z-10 [mask-image:radial-gradient(700px_520px_at_55%_10%,black,transparent)]"
      >
        <div className="absolute right-[-15%] top-[-20%] h-[720px] w-[720px] rounded-full bg-cyan-400/20 blur-3xl" />
        <div className="absolute left-[-10%] bottom-[-20%] h-[620px] w-[620px] rounded-full bg-emerald-500/20 blur-3xl" />
      </div>

      <div className="flex">
        <ChatSidebar />

        <main className="flex-1">
          {/* Top bar giả lập */}
          <div className="h-16 flex items-center justify-between px-6">
            <div className="font-semibold tracking-tight">JobJob</div>
            <nav className="hidden gap-8 text-sm md:flex">
              <a className="hover:text-teal-300 transition-colors" href="#gioi-thieu">Giới thiệu</a>
              <a className="hover:text-teal-300 transition-colors" href="#lien-he">Liên Hệ</a>
              <a className="hover:text-teal-300 transition-colors" href="#goi-cuoc">Gói Cước</a>
              <a className="hover:text-teal-300 transition-colors" href="#dang-ky">Đăng Ký</a>
            </nav>
          </div>

                     <h1 className="text-center text-3xl sm:text-4xl font-extrabold leading-tight mt-2 mb-4">
             Tìm Việc Làm Phù Hợp
           </h1>

          {/* Deck */}
          <div className="px-4">
            <AnimatePresence initial={false} mode="popLayout">
              {top ? (
                <Deck key={top.id} queue={queue} onSwipe={handleSwipe} peekBlurPx={10} overrideScore={scoreData} overrideFeatures={scoreData?.features} />
              ) : (
                <div className="grid place-items-center h-[60vh] opacity-80">
                  Hết job để quẹt — quay lại sau nha!
                </div>
              )}
            </AnimatePresence>
          </div>

                     {/* Nút hành động */}
           <div className="mt-4 mb-6 flex items-center justify-between max-w-[720px] mx-auto px-4">
            <button
              onClick={() => handleSwipe("skip")}
              className="rounded-full bg-black/70 px-10 py-4 text-lg font-semibold hover:bg-black/60 shadow-[0_10px_40px_rgba(0,0,0,0.35)]"
            >
              BỎ QUA
            </button>
            <button
              onClick={() => handleSwipe("apply")}
              className="rounded-full border border-white/50 px-10 py-4 text-lg font-semibold hover:bg-white/10 shadow-[0_10px_40px_rgba(0,0,0,0.35)]"
            >
              ỨNG TUYỂN
            </button>
          </div>
        </main>
      </div>
    </div>
  );
}
