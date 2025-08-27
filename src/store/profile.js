import { create } from 'zustand'

export const useProfile = create((set) => ({
  data: null,
  setData: (data) => set({ data }),
  updateField: (key, val) => set((s) => ({ data: { ...(s.data || {}), [key]: val } })),
  reset: () => set({ data: null })
}))


