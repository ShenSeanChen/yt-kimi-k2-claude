-- Simple Fix for Authentication Issues
-- Run this in your Supabase SQL Editor

-- 1. First, let's drop the problematic trigger and function
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
DROP FUNCTION IF EXISTS handle_new_user() CASCADE;

-- 2. Make sure the profiles table allows INSERT operations
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- 3. Drop and recreate the profile policies to ensure they work
DROP POLICY IF EXISTS "Users can insert their own profile" ON profiles;
DROP POLICY IF EXISTS "Users can view their own profile" ON profiles;
DROP POLICY IF EXISTS "Users can update their own profile" ON profiles;

-- 4. Create the correct policies for profiles
CREATE POLICY "Enable insert for authentication" ON profiles
  FOR INSERT WITH CHECK (true);

CREATE POLICY "Users can view their own profile" ON profiles
  FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update their own profile" ON profiles
  FOR UPDATE USING (auth.uid() = id);

-- 5. Create a simpler trigger function that's more robust
CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
  -- Insert a new profile for the user
  INSERT INTO profiles (id, full_name)
  VALUES (
    NEW.id,
    COALESCE(NEW.raw_user_meta_data->>'full_name', split_part(NEW.email, '@', 1))
  );
  
  RETURN NEW;
EXCEPTION 
  WHEN OTHERS THEN
    -- Log the error but don't fail the user creation
    RAISE WARNING 'Failed to create profile for user %: %', NEW.id, SQLERRM;
    RETURN NEW;
END;
$$;

-- 6. Create the trigger
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW
  EXECUTE FUNCTION handle_new_user();

-- 7. Test if the function works by checking if it exists
SELECT routine_name 
FROM information_schema.routines 
WHERE routine_name = 'handle_new_user';

-- 8. Check if RLS is enabled on profiles
SELECT tablename, rowsecurity 
FROM pg_tables 
WHERE tablename = 'profiles'; 