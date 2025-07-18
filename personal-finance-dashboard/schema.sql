-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create profiles table
CREATE TABLE IF NOT EXISTS profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id),
  full_name TEXT,
  monthly_budget DECIMAL(10,2) DEFAULT 3000,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Create transactions table
CREATE TABLE IF NOT EXISTS transactions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES profiles(id),
  amount DECIMAL(10,2) NOT NULL,
  description TEXT NOT NULL,
  category TEXT NOT NULL,
  type TEXT CHECK (type IN ('income', 'expense')),
  date DATE NOT NULL DEFAULT CURRENT_DATE,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Users can view own profile" ON profiles
  FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON profiles
  FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Users can view own transactions" ON transactions
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create own transactions" ON transactions
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own transactions" ON transactions
  FOR DELETE USING (auth.uid() = user_id);

-- Create function to handle new user signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (id, full_name)
  VALUES (new.id, new.raw_user_meta_data->>'full_name');
  RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create trigger for new user signup
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- Insert sample data for demo user
-- Note: Run this after creating a user with email: demo@example.com, password: demo123

-- Sample transactions for demo
INSERT INTO transactions (user_id, amount, description, category, type, date) VALUES 
('demo-user-id', 3500.00, 'Monthly Salary', 'Bills', 'income', '2024-07-01'),
('demo-user-id', 120.50, 'Grocery Shopping', 'Food', 'expense', '2024-07-03'),
('demo-user-id', 45.00, 'Netflix Subscription', 'Entertainment', 'expense', '2024-07-05'),
('demo-user-id', 60.00, 'Gas', 'Transportation', 'expense', '2024-07-07'),
('demo-user-id', 85.00, 'Dinner with friends', 'Food', 'expense', '2024-07-10'),
('demo-user-id', 200.00, 'Electric Bill', 'Bills', 'expense', '2024-07-15'),
('demo-user-id', 35.00, 'Movie tickets', 'Entertainment', 'expense', '2024-07-18'),
('demo-user-id', 150.00, 'New shoes', 'Shopping', 'expense', '2024-07-20');