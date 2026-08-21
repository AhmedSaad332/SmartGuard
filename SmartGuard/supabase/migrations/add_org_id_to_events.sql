-- Migration: Add org_id column to events table for multi-tenancy support
-- This migration adds organization-based data isolation for Smart Guard

-- Add org_id column as UUID type with foreign key constraint
ALTER TABLE events 
ADD COLUMN org_id UUID REFERENCES organizations(id);

-- Add index for better query performance on organization filtering
CREATE INDEX idx_events_org_id ON events(org_id);

-- Add comment to document the purpose of this column
COMMENT ON COLUMN events.org_id IS 'Organization identifier for multi-tenancy support - links to organizations table';

-- Update existing events with default organization (migration cleanup)
-- This is a one-time operation to set existing events to a default organization
-- In production, you might want to handle this differently based on your business logic
UPDATE events 
SET org_id = (
    SELECT org_id 
    FROM users 
    WHERE users.id = events.created_by 
    LIMIT 1
) 
WHERE org_id IS NULL;

-- Add created_by column if it doesn't exist for tracking who created the event
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'events' 
        AND column_name = 'created_by'
    ) THEN
        ALTER TABLE events ADD COLUMN created_by UUID REFERENCES users(id);
        COMMENT ON COLUMN events.created_by IS 'User who created this event';
    END IF;
END $$;
