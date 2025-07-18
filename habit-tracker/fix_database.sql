-- Fix Database Setup for Habit Tracker
-- Run this script in your Supabase SQL Editor to fix authentication issues

-- 1. Enable Row Level Security (RLS) on all tables
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE habits ENABLE ROW LEVEL SECURITY;
ALTER TABLE habit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE habit_categories ENABLE ROW LEVEL SECURITY;

-- 2. Drop existing policies if they exist (to avoid conflicts)
DROP POLICY IF EXISTS "Users can view their own profile" ON profiles;
DROP POLICY IF EXISTS "Users can update their own profile" ON profiles;
DROP POLICY IF EXISTS "Users can insert their own profile" ON profiles;

DROP POLICY IF EXISTS "Users can view their own habits" ON habits;
DROP POLICY IF EXISTS "Users can create their own habits" ON habits;
DROP POLICY IF EXISTS "Users can update their own habits" ON habits;
DROP POLICY IF EXISTS "Users can delete their own habits" ON habits;

DROP POLICY IF EXISTS "Users can view their own habit logs" ON habit_logs;
DROP POLICY IF EXISTS "Users can create their own habit logs" ON habit_logs;
DROP POLICY IF EXISTS "Users can update their own habit logs" ON habit_logs;
DROP POLICY IF EXISTS "Users can delete their own habit logs" ON habit_logs;

DROP POLICY IF EXISTS "Allow read access to categories" ON habit_categories;

-- 3. Create RLS Policies
-- Profiles policies
CREATE POLICY "Users can view their own profile" ON profiles
  FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update their own profile" ON profiles
  FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Users can insert their own profile" ON profiles
  FOR INSERT WITH CHECK (auth.uid() = id);

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

-- Categories policies (read-only for all authenticated users)
CREATE POLICY "Allow read access to categories" ON habit_categories
  FOR SELECT USING (true);

-- 4. Add missing UNIQUE constraint on habit_logs
ALTER TABLE habit_logs ADD CONSTRAINT habit_logs_habit_user_date_unique 
  UNIQUE(habit_id, user_id, date);

-- 5. Drop existing trigger and function if they exist
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
DROP FUNCTION IF EXISTS handle_new_user();

-- 6. Create the trigger function to handle new user creation
CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO profiles (id, full_name, avatar_url)
  VALUES (
    new.id, 
    COALESCE(new.raw_user_meta_data->>'full_name', split_part(new.email, '@', 1)), 
    new.raw_user_meta_data->>'avatar_url'
  );
  RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- 7. Create the trigger
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION handle_new_user();

-- 8. Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_habits_user_id ON habits(user_id);
CREATE INDEX IF NOT EXISTS idx_habits_created_at ON habits(created_at);
CREATE INDEX IF NOT EXISTS idx_habit_logs_user_id ON habit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_habit_logs_habit_id ON habit_logs(habit_id);
CREATE INDEX IF NOT EXISTS idx_habit_logs_date ON habit_logs(date);

-- 9. Insert default categories if they don't exist
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
('Finance', '💰', '#eab308')
ON CONFLICT (name) DO NOTHING;

-- 10. Grant necessary permissions
GRANT USAGE ON SCHEMA public TO anon, authenticated;
GRANT ALL ON ALL TABLES IN SCHEMA public TO anon, authenticated;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO anon, authenticated; 