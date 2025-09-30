/**
 * Demo page showcasing the Job-CV matching functionality
 */
import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import api from '../lib/api';
import JobMatchingCard from '../components/JobMatchingCard';

// Sample job data
const sampleJobs = [
  {
    id: 1,
    company: "TechCorp",
    title: "Senior Python Developer",
    description: "We are looking for a Senior Python Developer with 5+ years experience in Django, Flask, REST API development, PostgreSQL, Redis, AWS, Docker, and Machine Learning. Strong problem-solving skills and team collaboration experience required."
  },
  {
    id: 2,
    company: "DataSoft",
    title: "Data Scientist",
    description: "Seeking a Data Scientist with expertise in Python, pandas, scikit-learn, TensorFlow, PyTorch, SQL, and statistical analysis. Experience with machine learning pipelines, data visualization, and cloud platforms (AWS/GCP) preferred."
  },
  {
    id: 3,
    company: "WebAgency",
    title: "Full Stack Developer",
    description: "Looking for a Full Stack Developer proficient in React, Node.js, TypeScript, MongoDB, Express.js, and modern web technologies. Experience with responsive design, API integration, and deployment on cloud platforms."
  }
];

// Sample CV text
const sampleCV = `I am a Python Developer with 6 years of experience in web development and data science. 

Technical Skills:
- Python, Django, Flask, FastAPI
- REST API and GraphQL development
- PostgreSQL, MongoDB, Redis
- AWS, Docker, Jenkins, CI/CD
- Machine Learning: TensorFlow, PyTorch, scikit-learn
- Data Science: pandas, numpy, matplotlib
- Frontend: React, JavaScript, TypeScript
- Version Control: Git, GitHub

Experience:
- 6 years as Python Developer at various companies
- Built scalable web applications using Django and Flask
- Developed REST APIs and microservices
- Implemented machine learning models for business insights
- Worked with cloud platforms and containerization
- Led technical teams and mentored junior developers

Education:
- Bachelor's in Computer Science
- Multiple certifications in AWS and Python

I am passionate about clean code, continuous learning, and building innovative solutions.`;

export default function MatchingDemo() {
  const [currentJobIndex, setCurrentJobIndex] = useState(0);
  const [cvText, setCvText] = useState(sampleCV);
  const [apiStatus, setApiStatus] = useState('checking');
  const [matchingResults, setMatchingResults] = useState({});

  // Check API health on component mount
  useEffect(() => {
    const checkAPI = async () => {
      try {
        await api.healthCheck();
        setApiStatus('connected');
      } catch (error) {
        console.error('API connection failed:', error);
        setApiStatus('disconnected');
      }
    };
    checkAPI();
  }, []);

  // Calculate matching for all jobs when CV text changes
  useEffect(() => {
    if (apiStatus !== 'connected') return;

    const calculateAllMatches = async () => {
      const results = {};
      
      for (const job of sampleJobs) {
        try {
          const result = await api.predict({
            jd_text: job.description,
            cv_text: cvText,
            topk: 6
          });
          results[job.id] = result;
        } catch (error) {
          console.error(`Matching failed for job ${job.id}:`, error);
          results[job.id] = { score: 0, percent: '0%', features: [], latency_ms: 0 };
        }
      }
      
      setMatchingResults(results);
    };

    calculateAllMatches();
  }, [cvText, apiStatus]);

  const currentJob = sampleJobs[currentJobIndex];
  const currentMatch = matchingResults[currentJob?.id];

  const nextJob = () => {
    setCurrentJobIndex((prev) => (prev + 1) % sampleJobs.length);
  };

  const prevJob = () => {
    setCurrentJobIndex((prev) => (prev - 1 + sampleJobs.length) % sampleJobs.length);
  };

  return (
    <div className="min-h-screen bg-[#081A17] text-white p-6">
      {/* Header */}
      <div className="max-w-4xl mx-auto mb-8">
        <h1 className="text-3xl font-bold text-center mb-2">
          Job-CV Matching Demo
        </h1>
        <p className="text-center text-white/70">
          AI-powered job matching using TF-IDF and cosine similarity
        </p>
        
        {/* API Status */}
        <div className="mt-4 flex justify-center">
          <div className={`px-4 py-2 rounded-full text-sm font-medium ${
            apiStatus === 'connected' 
              ? 'bg-green-500/20 text-green-400 border border-green-500/30' 
              : apiStatus === 'disconnected'
              ? 'bg-red-500/20 text-red-400 border border-red-500/30'
              : 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30'
          }`}>
            {apiStatus === 'connected' && '✅ API Connected'}
            {apiStatus === 'disconnected' && '❌ API Disconnected'}
            {apiStatus === 'checking' && '🔄 Checking API...'}
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto grid lg:grid-cols-2 gap-8">
        {/* CV Input */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold">Your CV Text</h2>
          <textarea
            value={cvText}
            onChange={(e) => setCvText(e.target.value)}
            className="w-full h-64 p-4 bg-white/5 border border-white/10 rounded-lg text-white placeholder-white/50 resize-none"
            placeholder="Paste your CV text here..."
          />
          <div className="text-sm text-white/60">
            {cvText.length} characters
          </div>
        </div>

        {/* Job Display */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold">Job Opportunities</h2>
            <div className="flex gap-2">
              <button
                onClick={prevJob}
                className="px-3 py-1 bg-white/10 rounded text-sm hover:bg-white/20 transition-colors"
              >
                ← Previous
              </button>
              <button
                onClick={nextJob}
                className="px-3 py-1 bg-white/10 rounded text-sm hover:bg-white/20 transition-colors"
              >
                Next →
              </button>
            </div>
          </div>

          {/* Job Card */}
          <motion.div
            key={currentJob.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white/5 border border-white/10 rounded-lg p-6"
          >
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-lg font-semibold">{currentJob.title}</h3>
                <p className="text-white/70">{currentJob.company}</p>
              </div>
              {currentMatch && (
                <div className="text-right">
                  <div className="text-2xl font-bold text-green-400">
                    {currentMatch.percent}
                  </div>
                  <div className="text-sm text-white/60">
                    Match Score
                  </div>
                </div>
              )}
            </div>

            <p className="text-white/80 text-sm leading-relaxed mb-4">
              {currentJob.description}
            </p>

            {/* Matching Features */}
            {currentMatch && currentMatch.features.length > 0 && (
              <div>
                <h4 className="text-sm font-medium text-white/70 mb-2">
                  Matching Skills:
                </h4>
                <div className="flex flex-wrap gap-2">
                  {currentMatch.features.map((feature, index) => (
                    <span
                      key={index}
                      className="px-3 py-1 bg-green-500/20 text-green-300 rounded-full text-xs"
                    >
                      {feature}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Debug Info */}
            {process.env.NODE_ENV === 'development' && currentMatch && (
              <div className="mt-4 pt-4 border-t border-white/10 text-xs text-white/50">
                <div>Score: {currentMatch.score.toFixed(3)}</div>
                <div>Latency: {currentMatch.latency_ms}ms</div>
              </div>
            )}
          </motion.div>

          {/* Job Navigation */}
          <div className="flex justify-center gap-2">
            {sampleJobs.map((_, index) => (
              <button
                key={index}
                onClick={() => setCurrentJobIndex(index)}
                className={`w-3 h-3 rounded-full transition-colors ${
                  index === currentJobIndex 
                    ? 'bg-white' 
                    : 'bg-white/30 hover:bg-white/50'
                }`}
              />
            ))}
          </div>
        </div>
      </div>

      {/* Instructions */}
      <div className="max-w-4xl mx-auto mt-8 p-6 bg-white/5 border border-white/10 rounded-lg">
        <h3 className="text-lg font-semibold mb-3">How to Use</h3>
        <ol className="space-y-2 text-sm text-white/80">
          <li>1. Make sure the backend API is running on <code className="bg-white/10 px-2 py-1 rounded">http://localhost:8000</code></li>
          <li>2. Modify the CV text in the left panel to see how it affects matching scores</li>
          <li>3. Navigate through different job postings using the Previous/Next buttons</li>
          <li>4. Observe how the AI identifies matching skills and calculates compatibility scores</li>
        </ol>
      </div>
    </div>
  );
}
