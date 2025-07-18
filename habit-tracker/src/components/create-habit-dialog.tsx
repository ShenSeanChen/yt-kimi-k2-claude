'use client'

import { useState, useEffect } from 'react'
import { createClient } from '@/lib/supabase-client'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { toast } from 'sonner'
import { Loader2 } from 'lucide-react'

interface Category {
  id: string
  name: string
  icon: string
  color: string
}

interface CreateHabitDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSuccess: () => void
}

export function CreateHabitDialog({ open, onOpenChange, onSuccess }: CreateHabitDialogProps) {
  const [categories, setCategories] = useState<Category[]>([])
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    category: '',
    frequency: 'daily',
    target_count: 1,
  })
  const supabase = createClient()

  useEffect(() => {
    if (open) {
      fetchCategories()
    }
  }, [open])

  const fetchCategories = async () => {
    try {
      const { data, error } = await supabase
        .from('habit_categories')
        .select('*')
        .order('name')

      if (error) throw error
      setCategories(data || [])
    } catch (error: any) {
      toast.error('Failed to load categories')
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      const { data: { user } } = await supabase.auth.getUser()
      if (!user) {
        toast.error('You must be logged in')
        return
      }

      const selectedCategory = categories.find(c => c.name === formData.category)
      if (!selectedCategory) {
        toast.error('Please select a category')
        return
      }

      const { error } = await supabase
        .from('habits')
        .insert([
          {
            user_id: user.id,
            name: formData.name,
            description: formData.description,
            category: formData.category,
            color: selectedCategory.color,
            icon: selectedCategory.icon,
            frequency: formData.frequency,
            target_count: formData.target_count,
          },
        ])

      if (error) throw error

      toast.success('Habit created successfully!')
      onSuccess()
      onOpenChange(false)
      setFormData({
        name: '',
        description: '',
        category: '',
        frequency: 'daily',
        target_count: 1,
      })
    } catch (error: any) {
      toast.error(error.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Create New Habit</DialogTitle>
          <DialogDescription>
            Start building a new habit today. Choose a category and set your goal.
          </DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <label className="text-sm font-medium">Habit Name</label>
            <Input
              placeholder="e.g., Drink 8 glasses of water"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              required
            />
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium">Description (optional)</label>
            <Textarea
              placeholder="Brief description of your habit"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              rows={3}
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">Category</label>
              <Select
                value={formData.category}
                onValueChange={(value) => setFormData({ ...formData, category: value })}
                required
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select category" />
                </SelectTrigger>
                <SelectContent>
                  {categories.map((category) => (
                    <SelectItem key={category.id} value={category.name}>
                      <span className="flex items-center space-x-2">
                        <span>{category.icon}</span>
                        <span>{category.name}</span>
                      </span>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium">Frequency</label>
              <Select
                value={formData.frequency}
                onValueChange={(value: any) => setFormData({ ...formData, frequency: value })}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="daily">Daily</SelectItem>
                  <SelectItem value="weekly">Weekly</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="flex justify-end space-x-2">
            <Button
              type="button"
              variant="outline"
              onClick={() => onOpenChange(false)}
              disabled={loading}
            >
              Cancel
            </Button>
            <Button type="submit" disabled={loading}>
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Creating...
                </>
              ) : (
                'Create Habit'
              )}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  )
}