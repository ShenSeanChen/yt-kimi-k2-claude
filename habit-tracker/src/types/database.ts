export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export type Database = {
  public: {
    Tables: {
      profiles: {
        Row: {
          id: string
          full_name: string | null
          avatar_url: string | null
          timezone: string
          created_at: string
          updated_at: string
        }
        Insert: {
          id: string
          full_name?: string | null
          avatar_url?: string | null
          timezone?: string
          created_at?: string
          updated_at?: string
        }
        Update: {
          id?: string
          full_name?: string | null
          avatar_url?: string | null
          timezone?: string
          created_at?: string
          updated_at?: string
        }
        Relationships: [
          {
            foreignKeyName: "profiles_id_fkey"
            columns: ["id"]
            isOneToOne: true
            referencedRelation: "users"
            referencedColumns: ["id"]
          }
        ]
      }
      habits: {
        Row: {
          id: string
          user_id: string
          name: string
          description: string | null
          category: string
          color: string
          icon: string
          frequency: string
          target_count: number
          is_archived: boolean
          created_at: string
          updated_at: string
        }
        Insert: {
          id?: string
          user_id: string
          name: string
          description?: string | null
          category: string
          color?: string
          icon?: string
          frequency?: string
          target_count?: number
          is_archived?: boolean
          created_at?: string
          updated_at?: string
        }
        Update: {
          id?: string
          user_id?: string
          name?: string
          description?: string | null
          category?: string
          color?: string
          icon?: string
          frequency?: string
          target_count?: number
          is_archived?: boolean
          created_at?: string
          updated_at?: string
        }
        Relationships: [
          {
            foreignKeyName: "habits_user_id_fkey"
            columns: ["user_id"]
            isOneToOne: false
            referencedRelation: "profiles"
            referencedColumns: ["id"]
          }
        ]
      }
      habit_logs: {
        Row: {
          id: string
          habit_id: string
          user_id: string
          date: string
          completed: boolean
          notes: string | null
          created_at: string
        }
        Insert: {
          id?: string
          habit_id: string
          user_id: string
          date?: string
          completed?: boolean
          notes?: string | null
          created_at?: string
        }
        Update: {
          id?: string
          habit_id?: string
          user_id?: string
          date?: string
          completed?: boolean
          notes?: string | null
          created_at?: string
        }
        Relationships: [
          {
            foreignKeyName: "habit_logs_habit_id_fkey"
            columns: ["habit_id"]
            isOneToOne: false
            referencedRelation: "habits"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "habit_logs_user_id_fkey"
            columns: ["user_id"]
            isOneToOne: false
            referencedRelation: "profiles"
            referencedColumns: ["id"]
          }
        ]
      }
      habit_categories: {
        Row: {
          id: string
          name: string
          icon: string
          color: string
        }
        Insert: {
          id?: string
          name: string
          icon: string
          color: string
        }
        Update: {
          id?: string
          name?: string
          icon?: string
          color?: string
        }
        Relationships: []
      }
    }
    Views: {
      [_ in never]: never
    }
    Functions: {
      [_ in never]: never
    }
    Enums: {
      [_ in never]: never
    }
    CompositeTypes: {
      [_ in never]: never
    }
  }
}

export type Tables<T extends keyof Database["public"]["Tables"]> = Database["public"]["Tables"][T]["Row"]

export type TablesInsert<T extends keyof Database["public"]["Tables"]> = Database["public"]["Tables"][T]["Insert"]

export type TablesUpdate<T extends keyof Database["public"]["Tables"]> = Database["public"]["Tables"][T]["Update"]

export type Enums<T extends keyof Database["public"]["Enums"]> = Database["public"]["Enums"][T]
  