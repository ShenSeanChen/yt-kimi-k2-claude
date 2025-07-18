'use client'

import { useEffect, useState } from 'react'
import { createClient } from '@/lib/supabase-client'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Flame, Target, Calendar, TrendingUp } from 'lucide-react'
import { format, subDays } from 'date-fns'

interface Habit {
  id: string
  habit_logs: Array<{
    date: string
    completed: boolean
  }>
}

interface StatsCardsProps {
  habits: Habit[]
}

export function StatsCards({ habits }: StatsCardsProps) {
  const [stats, setStats] = useState({
    totalHabits: 0,
    completedToday: 0,
    currentStreak: 0,
    weeklyCompletion: 0,
  })

  useEffect(() => {
    calculateStats()
  }, [habits])

  const calculateStats = async () => {
    const today = format(new Date(), 'yyyy-MM-dd')
    const weekAgo = format(subDays(new Date(), 7), 'yyyy-MM-dd')

    const totalHabits = habits.length
    const completedToday = habits.filter(habit => 
      habit.habit_logs.some(log => log.date === today && log.completed)
    ).length

    // Calculate current streak (simplified)
    let currentStreak = 0
    const streakDays = []
    for (let i = 0; i < 30; i++) {
      const date = format(subDays(new Date(), i), 'yyyy-MM-dd')
      const completed = habits.some(habit => 
        habit.habit_logs.some(log => log.date === date && log.completed)
      )
      if (completed) {
        streakDays.unshift(date)
      } else {
        break
      }
    }
    currentStreak = streakDays.length

    // Calculate weekly completion rate
    let totalPossible = 0
    let totalCompleted = 0
    
    for (let i = 0; i < 7; i++) {
      const date = format(subDays(new Date(), i), 'yyyy-MM-dd')
      const dayHabits = habits.filter(habit => 
        habit.habit_logs.some(log => log.date === date && log.completed)
      ).length
      totalCompleted += dayHabits
      totalPossible += totalHabits
    }

    const weeklyCompletion = totalPossible > 0 
      ? Math.round((totalCompleted / totalPossible) * 100) 
      : 0

    setStats({
      totalHabits,
      completedToday,
      currentStreak,
      weeklyCompletion,
    })
  }

  return (
    <div className="grid gap-4 md:grid-cols-4 mb-8">
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Total Habits</CardTitle>
          <Target className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{stats.totalHabits}</div>
          <p className="text-xs text-muted-foreground">Active habits</p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Completed Today</CardTitle>
          <Calendar className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{stats.completedToday}</div>
          <p className="text-xs text-muted-foreground">Out of {stats.totalHabits} total</p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Current Streak</CardTitle>
          <Flame className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{stats.currentStreak}</div>
          <p className="text-xs text-muted-foreground">Days in a row</p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Weekly Completion</CardTitle>
          <TrendingUp className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{stats.weeklyCompletion}%</div>
          <p className="text-xs text-muted-foreground">This week</p>
        </CardContent>
      </Card>
    </div>
  )
}