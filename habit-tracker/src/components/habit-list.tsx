'use client'

import { useState, useEffect } from 'react'
import { createClient } from '@/lib/supabase-client'
import { Card, CardContent } from '@/components/ui/card'
import { Checkbox } from '@/components/ui/checkbox'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { toast } from 'sonner'
import { Flame, Edit, Trash2 } from 'lucide-react'
import { format } from 'date-fns'
import { EditHabitDialog } from './edit-habit-dialog'
import { DeleteHabitDialog } from './delete-habit-dialog'

interface Habit {
  id: string
  name: string
  description: string | null
  category: string
  color: string
  icon: string
  frequency: string
  target_count: number
  habit_logs: Array<{
    id: string
    date: string
    completed: boolean
  }>
}

interface HabitListProps {
  habits: Habit[]
  onUpdate: () => void
}

export function HabitList({ habits, onUpdate }: HabitListProps) {
  const [todayLogs, setTodayLogs] = useState<Record<string, boolean>>({})
  const [streaks, setStreaks] = useState<Record<string, number>>({})
  const [editingHabit, setEditingHabit] = useState<string | null>(null)
  const [deletingHabit, setDeletingHabit] = useState<string | null>(null)
  const supabase = createClient()

  const today = format(new Date(), 'yyyy-MM-dd')

  useEffect(() => {
    if (habits.length > 0) {
      fetchTodayLogs()
      calculateStreaks()
    }
  }, [habits])

  const fetchTodayLogs = async () => {
    try {
      const { data: { user } } = await supabase.auth.getUser()
      if (!user) return

      const { data } = await supabase
        .from('habit_logs')
        .select('*')
        .eq('user_id', user.id)
        .eq('date', today)

      const logsMap: Record<string, boolean> = {}
      data?.forEach(log => {
        logsMap[log.habit_id] = log.completed
      })
      setTodayLogs(logsMap)
    } catch (error) {
      console.error('Error fetching today logs:', error)
    }
  }

  const calculateStreaks = async () => {
    try {
      const { data: { user } } = await supabase.auth.getUser()
      if (!user) return

      const streaksMap: Record<string, number> = {}

      for (const habit of habits) {
        const { data: logs } = await supabase
          .from('habit_logs')
          .select('date, completed')
          .eq('habit_id', habit.id)
          .eq('completed', true)
          .order('date', { ascending: false })

        let streak = 0
        let currentDate = new Date()
        
        if (logs) {
          for (const log of logs) {
            const logDate = new Date(log.date)
            const diffDays = Math.floor((currentDate.getTime() - logDate.getTime()) / (1000 * 60 * 60 * 24))
            
            if (diffDays === streak) {
              streak++
            } else {
              break
            }
          }
        }
        
        streaksMap[habit.id] = streak
      }
      
      setStreaks(streaksMap)
    } catch (error) {
      console.error('Error calculating streaks:', error)
    }
  }

  const toggleHabit = async (habitId: string) => {
    try {
      const { data: { user } } = await supabase.auth.getUser()
      if (!user) return

      const isCompleted = todayLogs[habitId]

      if (isCompleted) {
        const { error } = await supabase
          .from('habit_logs')
          .delete()
          .eq('habit_id', habitId)
          .eq('user_id', user.id)
          .eq('date', today)

        if (error) throw error
        
        setTodayLogs(prev => ({ ...prev, [habitId]: false }))
        toast.success('Habit unchecked for today')
      } else {
        const { error } = await supabase
          .from('habit_logs')
          .insert([
            {
              habit_id: habitId,
              user_id: user.id,
              date: today,
              completed: true,
            },
          ])

        if (error) throw error
        
        setTodayLogs(prev => ({ ...prev, [habitId]: true }))
        toast.success('Great job! Habit completed!')
      }

      calculateStreaks()
      onUpdate()
    } catch (error: any) {
      toast.error(error.message)
    }
  }

  if (habits.length === 0) {
    return (
      <Card className="text-center py-12">
        <CardContent>
          <p className="text-gray-500 mb-4">No habits yet. Start building better habits today!</p>
          <Button onClick={onUpdate}>
            Refresh
          </Button>
        </CardContent>
      </Card>
    )
  }

  return (
    <div className="space-y-4">
      {habits.map((habit) => (
        <Card key={habit.id} className="group">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <Checkbox
                  checked={todayLogs[habit.id] || false}
                  onCheckedChange={() => toggleHabit(habit.id)}
                  className="h-6 w-6"
                />
                <div className="flex items-center space-x-2">
                  <span className="text-2xl">{habit.icon}</span>
                  <div>
                    <h3 className="font-semibold text-gray-900">{habit.name}</h3>
                    <p className="text-sm text-gray-600">{habit.description}</p>
                  </div>
                </div>
              </div>

              <div className="flex items-center space-x-2">
                <Badge variant="outline" style={{ color: habit.color }}>
                  {habit.category}
                </Badge>
                
                {streaks[habit.id] > 0 && (
                  <Badge variant="secondary" className="flex items-center space-x-1">
                    <Flame className="w-3 h-3" />
                    <span>{streaks[habit.id]} day streak</span>
                  </Badge>
                )}

                <div className="opacity-0 group-hover:opacity-100 transition-opacity flex space-x-1">
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={() => setEditingHabit(habit.id)}
                  >
                    <Edit className="w-4 h-4" />
                  </Button>
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={() => setDeletingHabit(habit.id)}
                  >
                    <Trash2 className="w-4 h-4" />
                  </Button>
                </div>
              </div>
            </div>
          </CardContent>

          {editingHabit === habit.id && (
            <EditHabitDialog
              habit={habit}
              open={true}
              onOpenChange={(open) => !open && setEditingHabit(null)}
              onSuccess={() => {
                setEditingHabit(null)
                onUpdate()
              }}
            />
          )}

          {deletingHabit === habit.id && (
            <DeleteHabitDialog
              habit={habit}
              open={true}
              onOpenChange={(open) => !open && setDeletingHabit(null)}
              onSuccess={() => {
                setDeletingHabit(null)
                onUpdate()
              }}
            />
          )}
        </Card>
      ))}
    </div>
  )
}