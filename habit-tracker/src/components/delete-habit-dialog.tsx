'use client'

import { createClient } from '@/lib/supabase-client'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { toast } from 'sonner'
import { Loader2 } from 'lucide-react'
import { useState } from 'react'

interface Habit {
  id: string
  name: string
}

interface DeleteHabitDialogProps {
  habit: Habit
  open: boolean
  onOpenChange: (open: boolean) => void
  onSuccess: () => void
}

export function DeleteHabitDialog({ habit, open, onOpenChange, onSuccess }: DeleteHabitDialogProps) {
  const [loading, setLoading] = useState(false)
  const supabase = createClient()

  const handleDelete = async () => {
    setLoading(true)
    try {
      const { error } = await supabase
        .from('habits')
        .update({ is_archived: true })
        .eq('id', habit.id)

      if (error) throw error

      toast.success('Habit archived successfully')
      onSuccess()
      onOpenChange(false)
    } catch (error: any) {
      toast.error(error.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Archive Habit</DialogTitle>
          <DialogDescription>
            Are you sure you want to archive "{habit.name}"? This will hide it from your daily view but keep your progress history.
          </DialogDescription>
        </DialogHeader>
        <DialogFooter>
          <Button
            variant="outline"
            onClick={() => onOpenChange(false)}
            disabled={loading}
          >
            Cancel
          </Button>
          <Button
            variant="destructive"
            onClick={handleDelete}
            disabled={loading}
          >
            {loading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Archiving...
              </>
            ) : (
              'Archive'
            )}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}