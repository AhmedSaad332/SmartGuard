-- Multi-tenancy Row Level Security Policy for Events Table
-- This policy ensures users can only access events from their own organization
-- Only Smart Guard (super admin) can access all organizations

-- Enable RLS on events table
ALTER TABLE events ENABLE ROW LEVEL SECURITY;

-- Policy to allow users to read events only from their organization
CREATE POLICY "Users can view own organization events" ON events
    FOR SELECT USING (
        auth.role() = 'authenticated' 
        AND org_id = (
            SELECT org_id 
            FROM users 
            WHERE users.id = auth.uid()
        )
    );

-- Policy to allow users to insert events only for their organization
CREATE POLICY "Users can insert own organization events" ON events
    FOR INSERT WITH CHECK (
        auth.role() = 'authenticated' 
        AND org_id = (
            SELECT org_id 
            FROM users 
            WHERE users.id = auth.uid()
        )
    );

-- Policy to allow users to update events only from their organization
CREATE POLICY "Users can update own organization events" ON events
    FOR UPDATE USING (
        auth.role() = 'authenticated' 
        AND org_id = (
            SELECT org_id 
            FROM users 
            WHERE users.id = auth.uid()
        )
    );

-- Policy to allow users to delete events only from their organization
CREATE POLICY "Users can delete own organization events" ON events
    FOR DELETE USING (
        auth.role() = 'authenticated' 
        AND org_id = (
            SELECT org_id 
            FROM users 
            WHERE users.id = auth.uid()
        )
    );

-- Smart Guard (super admin) bypass policy - ONLY Smart Guard can manage all events
CREATE POLICY "Smart Guard can manage all events" ON events
    FOR ALL USING (
        auth.role() = 'authenticated' 
        AND auth.email() = 'admin@smartguard.com'
    );
