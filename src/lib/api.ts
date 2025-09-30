/**
 * API client for Job-CV matching service
 */

export interface PredictionRequest {
  jd_text: string;
  cv_text: string;
  topk?: number;
}

export interface PredictionResponse {
  score: number;
  percent: string;
  features: string[];
  latency_ms: number;
}

export interface BatchPredictionRequest {
  pairs: Array<{
    jd_text: string;
    cv_text: string;
  }>;
  topk?: number;
}

export interface BatchPredictionResponse {
  results: PredictionResponse[];
}

export interface HealthResponse {
  status: string;
  timestamp: number;
  version: string;
}

class JobMatchingAPI {
  private baseURL: string;
  private timeout: number;

  constructor(baseURL: string = 'http://localhost:8000', timeout: number = 15000) {
    this.baseURL = baseURL;
    this.timeout = timeout;
  }

  /**
   * Make a request with timeout and error handling
   */
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      const response = await fetch(`${this.baseURL}${endpoint}`, {
        ...options,
        signal: controller.signal,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          errorData.detail || `HTTP ${response.status}: ${response.statusText}`
        );
      }

      return await response.json();
    } catch (error) {
      clearTimeout(timeoutId);
      
      if (error instanceof Error) {
        if (error.name === 'AbortError') {
          throw new Error('Request timeout - please try again');
        }
        throw error;
      }
      
      throw new Error('Unknown error occurred');
    }
  }

  /**
   * Check API health
   */
  async healthCheck(): Promise<HealthResponse> {
    return this.request<HealthResponse>('/health');
  }

  /**
   * Predict matching score between job description and CV
   */
  async predict(request: PredictionRequest): Promise<PredictionResponse> {
    return this.request<PredictionResponse>('/predict', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  /**
   * Predict matching scores for multiple JD-CV pairs
   */
  async predictBatch(request: BatchPredictionRequest): Promise<BatchPredictionResponse> {
    return this.request<BatchPredictionResponse>('/predict/batch_json', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  /**
   * Multipart batch: one JD PDF, many CV PDFs
   */
  async predictBatchFiles(
    jdFile: File,
    cvFiles: File[],
    topk: number = 6
  ): Promise<{ jd_name: string; results: Array<{ cv_name: string; score: number; percent: string; features: string[]; latency_ms: number; }> }>{
    const form = new FormData();
    form.append('jd_file', jdFile);
    cvFiles.forEach((f) => form.append('cv_files', f));
    form.append('topk', String(topk));

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      const response = await fetch(`${this.baseURL}/predict/batch`, {
        method: 'POST',
        body: form,
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const text = await response.text();
        throw new Error(text || `HTTP ${response.status}: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      clearTimeout(timeoutId);
      if (error instanceof Error) {
        if (error.name === 'AbortError') throw new Error('Request timeout - please try again');
        throw error;
      }
      throw new Error('Unknown error occurred');
    }
  }

  /**
   * Predict matching score from uploaded files
   */
  async predictFromFiles(
    jdFile: File,
    cvFile: File,
    topk: number = 6
  ): Promise<PredictionResponse> {
    const formData = new FormData();
    formData.append('jd_file', jdFile);
    formData.append('cv_file', cvFile);
    formData.append('topk', topk.toString());

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      const response = await fetch(`${this.baseURL}/predict/files`, {
        method: 'POST',
        body: formData,
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          errorData.detail || `HTTP ${response.status}: ${response.statusText}`
        );
      }

      return await response.json();
    } catch (error) {
      clearTimeout(timeoutId);
      
      if (error instanceof Error) {
        if (error.name === 'AbortError') {
          throw new Error('Request timeout - please try again');
        }
        throw error;
      }
      
      throw new Error('Unknown error occurred');
    }
  }

  /**
   * Quick prediction with default parameters
   */
  async quickPredict(jdText: string, cvText: string): Promise<PredictionResponse> {
    return this.predict({
      jd_text: jdText,
      cv_text: cvText,
      topk: 6,
    });
  }

  /**
   * Get matching score as percentage number
   */
  async getMatchPercentage(jdText: string, cvText: string): Promise<number> {
    const result = await this.quickPredict(jdText, cvText);
    return Math.round(result.score * 100);
  }

  /**
   * Get top matching features
   */
  async getTopFeatures(jdText: string, cvText: string, count: number = 6): Promise<string[]> {
    const result = await this.predict({
      jd_text: jdText,
      cv_text: cvText,
      topk: count,
    });
    return result.features;
  }
}

// Create and export default API instance
const api = new JobMatchingAPI();

export default api;

// Export wrapper functions to preserve `this` context
export const healthCheck = () => api.healthCheck();
export const predict = (request: PredictionRequest) => api.predict(request);
export const predictBatch = (request: BatchPredictionRequest) => api.predictBatch(request);
export const predictFromFiles = (jdFile: File, cvFile: File, topk: number = 6) =>
  api.predictFromFiles(jdFile, cvFile, topk);
export const quickPredict = (jdText: string, cvText: string) => api.quickPredict(jdText, cvText);
export const getMatchPercentage = (jdText: string, cvText: string) =>
  api.getMatchPercentage(jdText, cvText);
export const getTopFeatures = (jdText: string, cvText: string, count: number = 6) =>
  api.getTopFeatures(jdText, cvText, count);

// Export the class for custom instances
export { JobMatchingAPI };