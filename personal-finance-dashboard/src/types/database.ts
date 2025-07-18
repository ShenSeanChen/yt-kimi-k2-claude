export interface Profile {
  id: string
  full_name: string | null
  monthly_budget: number
  created_at: string
}

export interface Transaction {
  id: string
  user_id: string
  amount: number
  description: string
  category: string
  type: 'income' | 'expense'
  date: string
  created_at: string
}

export interface Budget {
  id: string
  user_id: string
  category: string
  monthly_limit: number
}

export const CATEGORIES = [
  'Food',
  'Transportation',
  'Entertainment',
  'Shopping',
  'Bills',
  'Healthcare',
  'Education',
  'Other'
] as const

export type Category = typeof CATEGORIES[number]

export const CATEGORY_COLORS: Record<Category, string> = {
  Food: '#ef4444',
  Transportation: '#3b82f6',
  Entertainment: '#8b5cf6',
  Shopping: '#ec4899',
  Bills: '#f59e0b',
  Healthcare: '#10b981',
  Education: '#06b6d4',
  Other: '#6b7280'
}

export const CATEGORY_ICONS: Record<Category, string> = {
  Food: '🍔',
  Transportation: '🚗',
  Entertainment: '🎬',
  Shopping: '🛍️',
  Bills: '📄',
  Healthcare: '🏥',
  Education: '📚',
  Other: '📦'
}