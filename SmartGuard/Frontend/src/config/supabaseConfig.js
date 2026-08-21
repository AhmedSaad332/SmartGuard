/**
 * Supabase Configuration
 * Initialize Supabase client with credentials
 */

import { createClient } from '@supabase/supabase-js';

// Load Supabase credentials from environment for security.
// Vite exposes env vars as `import.meta.env.VITE_*`.
const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL || 'https://chjonhyjqztktxspwlkd.supabase.co';
const SUPABASE_ANON_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY;

// NOTE: Never include the service-role key in frontend code. Service-role keys
// should be stored only on trusted backends and rotated if exposed.

// Real-time client for Supabase (uses the anon/public key)
if (!SUPABASE_ANON_KEY) {
  // In development you can set VITE_SUPABASE_ANON_KEY in a .env file.
  console.warn('VITE_SUPABASE_ANON_KEY is not set. Supabase requests may fail.');
}
export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// Utility function to make requests to Supabase
export const supabaseClient = {
  // Get auth token from localStorage
  getToken: () => localStorage.getItem('supabase_token'),
  
  // Set auth token to localStorage
  setToken: (token) => localStorage.setItem('supabase_token', token),
  
  // Set user to localStorage as a fallback
  setLocalUser: (user) => {
    if (!user) {
      localStorage.removeItem('supabase_user');
      return;
    }
    localStorage.setItem('supabase_user', JSON.stringify(user));
  },
  
  // Get user from localStorage
  getLocalUser: () => {
    const user = localStorage.getItem('supabase_user');
    return user ? JSON.parse(user) : null;
  },
  
  // Remove auth token from localStorage
  removeToken: () => {
    localStorage.removeItem('supabase_token');
    localStorage.removeItem('supabase_user');
  },
  
  // Get user from localStorage (alias for backward compatibility)
  getUser: () => {
    return supabaseClient.getLocalUser();
  },

  // Get user from Supabase (Asynchronous version)
  getUserAsync: async () => {
    const token = supabaseClient.getToken();
    if (!token) return null;

    // Try to decode JWT token to get email
    let userEmail = null;
    try {
      const parts = token.split('.');
      if (parts.length === 3) {
        const payload = parts[1];
        const decoded = atob(payload);
        const tokenData = JSON.parse(decoded);
        userEmail = tokenData?.email;
      }
    } catch (e) {
      console.warn('JWT Decode Error:', e);
    }

    // Try fetching fresh data from Supabase if we have an email
    if (userEmail) {
      try {
        console.log(`🔄 Fetching fresh user data for: ${userEmail}`);
        const data = await supabaseClient.request(`/users?email=eq.${encodeURIComponent(userEmail)}`, 'GET');
        if (data && data.length > 0) {
          const freshUser = data[0];
          console.log(`✅ Received fresh data. Role: ${freshUser.role}`);
          supabaseClient.setLocalUser(freshUser);
          return freshUser;
        }
      } catch (error) {
        console.warn('⚠️ Failed to fetch fresh user data, falling back to cache:', error);
      }
    }

    // Fallback to local cache if Supabase request fails or no email found
    return supabaseClient.getLocalUser();
  },
  
  // Set user to Supabase instead of localStorage
  setUser: async (user) => {
    if (!user || !user.email) return;

    const userData = {
      email: user.email,
      full_name: user.full_name,
      organization: user.organization,
      role: user.role,
      status: user.status || 'pending',
      created_at: user.created_at || new Date().toISOString()
    };

    try {
      // First, try to see if user exists by email
      let existing;
      try {
        existing = await supabaseClient.request(`/users?email=eq.${user.email}`, 'GET');
      } catch (err) {
        if (err.message.includes('404')) {
          existing = await supabaseClient.request(`/profiles?email=eq.${user.email}`, 'GET');
        } else {
          throw err;
        }
      }

      let result = null;
      if (existing && existing.length > 0) {
        // Update existing record using email as key
        result = await supabaseClient.request(`/users?email=eq.${user.email}`, 'PATCH', userData);
      } else {
        // DO NOT AUTO-INSERT. Users must be created via Signup or by Admin.
        console.warn('User not found in Supabase. Cannot update.');
      }
      
      // Update local storage too
      supabaseClient.setLocalUser(userData);
      return result;
    } catch (error) {
      console.error('Error saving user to Supabase:', error);
      // If table is missing, store in localStorage as temporary fallback
      supabaseClient.setLocalUser(userData);
    }
  },
  
  // Remove user from localStorage
  removeUser: () => localStorage.removeItem('supabase_user'),
  
  // Remove user from Supabase
  removeUserFromSupabase: async (email) => {
    try {
      await supabaseClient.request(`/users?email=eq.${encodeURIComponent(email)}`, 'DELETE');
      localStorage.removeItem('supabase_user');
    } catch (error) {
      console.error('Error removing user from Supabase:', error);
    }
  },
  
  // Make authenticated request
  request: async (path, method = 'GET', body = null) => {
    const options = {
      method,
      headers: {
        'Content-Type': 'application/json',
        'apikey': SUPABASE_ANON_KEY,
        'Prefer': 'return=representation',
        'Authorization': `Bearer ${SUPABASE_ANON_KEY}`
      }
    };
    
    // Only add body for methods that support it (POST, PATCH, PUT)
    // DELETE requests should not have a body
    if (body && method !== 'DELETE') {
      options.body = JSON.stringify(body);
    }
    
    const response = await fetch(`${SUPABASE_URL}/rest/v1${path}`, options);
    
    // If 401 occurs, it's often because of the Authorization header issues
    if (response.status === 401) {
      console.warn('Supabase 401: Retrying...');
      const retryResponse = await fetch(`${SUPABASE_URL}/rest/v1${path}`, options);
      if (retryResponse.ok) return await retryResponse.json();
    }

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || `Request failed with status ${response.status}`);
    }
    
    return await response.json();
  }
};

export default {
  SUPABASE_URL,
  SUPABASE_ANON_KEY
};
