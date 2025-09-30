/**
 * Enhanced Job Card component with AI matching integration
 */
import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import api from '../lib/api';

export default function JobMatchingCard({ 
  job, 
  draggingX, 
  onDragEnd, 
  cvText = null, // CV text for matching
  showMatching = true 
}) {
  const [matchingData, setMatchingData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Avatar = ký tự đầu công ty
  const avatar = (job.company || "?").slice(0, 1).toUpperCase();

  // Calculate matching score when job or CV text changes
  useEffect(() => {
    if (!showMatching || !cvText || !job.description) return;

    const calculateMatching = async () => {
      setLoading(true);
      setError(null);
      
      try {
        const result = await api.predict({
          jd_text: job.description,
          cv_text: cvText,
          topk: 6
        });
        
        setMatchingData(result);
      } catch (err) {
        console.error('Matching calculation failed:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    calculateMatching();
  }, [job.description, cvText, showMatching]);

  // Get display data
  const score = matchingData?.score || 0;
  const percent = matchingData?.percent || '—%';
  const features = matchingData?.features || [];
  const latency = matchingData?.latency_ms || 0;

  return (
    <motion.div
      className="relative mx-auto w-full max-w-[720px] rounded-[28px] bg-[#1CDAC4] px-6 pb-8 pt-4 shadow-[0_30px_120px_rgba(0,0,0,0.35)]"
      style={{ x: draggingX }}
      drag="x"
      dragConstraints={{ left: 0, right: 0 }}
      onDragEnd={onDragEnd}
    >
      {/* Matching Badge */}
      {showMatching && (
        <div className="absolute right-6 top-4 rounded-full bg-white/70 text-black/80 px-4 py-1 text-[13px] font-semibold">
          {loading ? (
            <span className="flex items-center gap-2">
              <div className="w-3 h-3 border-2 border-black/30 border-t-black/80 rounded-full animate-spin" />
              Đang tính...
            </span>
          ) : error ? (
            <span className="text-red-600">Lỗi</span>
          ) : (
            `Độ tương thích: ${percent}`
          )}
        </div>
      )}

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
        {job.description || "Mô tả công việc"}
      </div>

      {/* Matching Features */}
      {showMatching && features.length > 0 && (
        <div className="mt-4 space-y-2">
          <div className="text-white/80 text-sm font-medium">
            Kỹ năng phù hợp:
          </div>
          <div className="flex flex-wrap gap-2">
            {features.slice(0, 4).map((feature, index) => (
              <span
                key={index}
                className="px-3 py-1 bg-white/20 rounded-full text-xs text-white/90 font-medium"
              >
                {feature}
              </span>
            ))}
            {features.length > 4 && (
              <span className="px-3 py-1 bg-white/10 rounded-full text-xs text-white/70">
                +{features.length - 4} khác
              </span>
            )}
          </div>
        </div>
      )}

      {/* Debug info (only in development) */}
      {process.env.NODE_ENV === 'development' && matchingData && (
        <div className="mt-2 text-xs text-white/60">
          Score: {score.toFixed(3)} | Latency: {latency}ms
        </div>
      )}
    </motion.div>
  );
}
