-- Habit Tracker Database Schema
-- Ultra-simple schema for demo purposes

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- User profiles table
CREATE TABLE profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  full_name TEXT,
  avatar_url TEXT,
  timezone TEXT DEFAULT 'UTC',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Habit categories
CREATE TABLE habit_categories (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT UNIQUE NOT NULL,
  icon TEXT NOT NULL,
  color TEXT NOT NULL
);

-- Insert default categories
INSERT INTO habit_categories (name, icon, color) VALUES
('Health', '💪', '#ef4444'),
('Productivity', '⚡', '#3b82f6'),
('Learning', '📚', '#8b5cf6'),
('Mindfulness', '🧘', '#10b981'),
('Creativity', '🎨', '#f59e0b'),
('Social', '👥', '#ec4899'),
('Fitness', '🏃', '#f97316'),
('Sleep', '😴', '#6366f1'),
('Nutrition', '🥗', '#84cc16'),
('Finance', '💰', '#eab308');

-- Habits table
CREATE TABLE habits (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  description TEXT,
  category TEXT NOT NULL,
  color TEXT DEFAULT '#3b82f6',
  icon TEXT DEFAULT '🎯',
  frequency TEXT DEFAULT 'daily' CHECK (frequency IN ('daily', 'weekly', 'custom')),
  target_count INTEGER DEFAULT 1,
  is_archived BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Habit completion logs
CREATE TABLE habit_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  habit_id UUID REFERENCES habits(id) ON DELETE CASCADE,
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
  date DATE NOT NULL DEFAULT CURRENT_DATE,
  completed BOOLEAN DEFAULT TRUE,
  notes TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(habit_id, user_id, date)
);

-- Indexes for performance
CREATE INDEX idx_habits_user_id ON habits(user_id);
CREATE INDEX idx_habits_created_at ON habits(created_at);
CREATE INDEX idx_habit_logs_user_id ON habit_logs(user_id);
CREATE INDEX idx_habit_logs_habit_id ON habit_logs(habit_id);
CREATE INDEX idx_habit_logs_date ON habit_logs(date);

-- Row Level Security (RLS)
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE habits ENABLE ROW LEVEL SECURITY;
ALTER TABLE habit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE habit_categories ENABLE ROW LEVEL SECURITY;

-- RLS Policies
-- Profiles policies
CREATE POLICY "Users can view their own profile" ON profiles
  FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update their own profile" ON profiles
  FOR UPDATE USING (auth.uid() = id);

-- Habits policies
CREATE POLICY "Users can view their own habits" ON habits
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create their own habits" ON habits
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own habits" ON habits
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own habits" ON habits
  FOR DELETE USING (auth.uid() = user_id);

-- Habit logs policies
CREATE POLICY "Users can view their own habit logs" ON habit_logs
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create their own habit logs" ON habit_logs
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own habit logs" ON habit_logs
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own habit logs" ON habit_logs
  FOR DELETE USING (auth.uid() = user_id);

-- Function to handle user creation
CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO profiles (id, full_name, avatar_url)
  VALUES (new.id, new.raw_user_meta_data->>'full_name', new.raw_user_meta_data->>'avatar_url');
  RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger for new user creation
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION handle_new_user();

-- Categories policies
CREATE POLICY "Allow read access to categories" ON habit_categories
  FOR SELECT USING (true);