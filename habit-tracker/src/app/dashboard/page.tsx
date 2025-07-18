'use client'

import { useState, useEffect } from 'react'
import { createClient } from '@/lib/supabase-client'
import { useRouter } from 'next/navigation'
import { HabitList } from '@/components/habit-list'
import { CreateHabitDialog } from '@/components/create-habit-dialog'
import { StatsCards } from '@/components/stats-cards'
import { Navigation } from '@/components/navigation'
import { Button } from '@/components/ui/button'
import { Loader2, Plus } from 'lucide-react'
import { toast } from 'sonner'

export default function DashboardPage() {
  const [habits, setHabits] = useState([])
  const [loading, setLoading] = useState(true)
  const [showCreateDialog, setShowCreateDialog] = useState(false)
  const supabase = createClient()
  const router = useRouter()

  useEffect(() => {
    fetchHabits()
  }, [])

  const fetchHabits = async () => {
    try {
      const { data: { user } } = await supabase.auth.getUser()
      if (!user) {
        router.push('/login')
        return
      }

      const { data, error } = await supabase
        .from('habits')
        .select(`*, habit_logs(*)`)
        .eq('user_id', user.id)
        .eq('is_archived', false)
        .order('created_at', { ascending: false })

      if (error) throw error
      setHabits(data || [])
    } catch (error: any) {
      toast.error('Failed to load habits')
      console.error('Error fetching habits:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSignOut = async () => {
    try {
      await supabase.auth.signOut()
      router.push('/login')
    } catch (error: any) {
      toast.error('Failed to sign out')
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation onSignOut={handleSignOut} />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Today's Habits</h1>
            <p className="text-gray-600 mt-1">Keep your streak going! 💪</p>
          </div>
          <Button onClick={() => setShowCreateDialog(true)} >
            <Plus className="w-4 h-4 mr-2" />
            New Habit
          </Button>
        </div>

        <StatsCards habits={habits} />

        <HabitList habits={habits} onUpdate={fetchHabits} />

        <CreateHabitDialog 
          open={showCreateDialog} 
          onOpenChange={setShowCreateDialog}
          onSuccess={fetchHabits}
        />
      </main>
    </div>
  )
}