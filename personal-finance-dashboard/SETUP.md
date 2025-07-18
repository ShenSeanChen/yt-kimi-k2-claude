# Personal Finance Dashboard - Quick Setup

## 1. Supabase Setup

1. Go to https://supabase.com and create a new project
2. Once created, go to Project Settings > API
3. Copy your URL and Anon Key into `.env.local`:
   ```
   NEXT_PUBLIC_SUPABASE_URL=your_url_here
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key_here
   ```

## 2. Database Setup

In your Supabase dashboard, go to SQL Editor and run:

```sql
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
```

## 3. Start the App

```bash
npm run dev
```

The app will run on http://localhost:3001 (or available port)

## Demo Instructions

1. **Sign Up**: Create a new account with email/password
2. **Add Transactions**: Click "+ Add Transaction" to add income/expenses
3. **View Dashboard**: See your total income, expenses, and balance in real-time

## Sample Data (Optional)

After creating a user, you can add sample data by running this SQL in Supabase:

```sql
-- Add sample transactions for demo
-- Replace 'your-user-id-here' with actual user ID from auth.users
INSERT INTO transactions (user_id, amount, description, category, type, date) VALUES 
('your-user-id-here', 3500.00, 'Monthly Salary', 'Bills', 'income', '2024-07-01'),
('your-user-id-here', 120.50, 'Grocery Shopping', 'Food', 'expense', '2024-07-03'),
('your-user-id-here', 45.00, 'Netflix Subscription', 'Entertainment', 'expense', '2024-07-05'),
('your-user-id-here', 60.00, 'Gas', 'Transportation', 'expense', '2024-07-07');
```