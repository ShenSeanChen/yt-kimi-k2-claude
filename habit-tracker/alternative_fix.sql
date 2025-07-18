-- Alternative Fix: Remove Trigger Completely
-- This will help us test if the trigger is causing the issue

-- 1. Remove the trigger and function completely
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
DROP FUNCTION IF EXISTS handle_new_user() CASCADE;

-- 2. Make profiles table completely open for testing
ALTER TABLE profiles DISABLE ROW LEVEL SECURITY;

-- 3. Grant all permissions to authenticated users
GRANT ALL ON profiles TO authenticated;
GRANT ALL ON profiles TO anon;

-- 4. Test user creation without automatic profile creation
-- Users will need to create their profiles manually after signup 