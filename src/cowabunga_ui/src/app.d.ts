// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
import type { LFAssistant } from '$lib/types/assistants';
import type { Profile } from '$lib/types/profile';
import type { LFThread } from '$lib/types/threads';
import type { FileObject } from 'openai/resources/files';
import type { APIKeyRow } from '$lib/types/apiKeys';

interface User {
  id: string;
  email?: string;
  app_metadata?: { provider?: string; providers?: string[] };
  user_metadata?: {
    email?: string;
    email_verified?: boolean;
    full_name?: string;
    iss?: string;
    name?: string;
    phone_verified?: boolean;
    provider_id?: string;
    sub?: string;
  };
  aud?: string;
  created_at?: string;
}

interface Session {
  access_token: string;
  refresh_token?: string;
  expires_in?: number;
  expires_at?: number;
  token_type?: string;
  provider_token?: string | null;
  provider_refresh_token?: string | null;
  user: User;
}

declare global {
  namespace App {
    // interface Error {}
    interface Locals {
      safeGetSession: () => Promise<{ session: Session | null; user: User | null }>;
      session: Session | null;
      user: User | null;
      isUsingOpenAI: boolean;
    }
    interface PageData {
      session: Session | null;
      user: User | null;
      title?: string | null;
      profile?: Profile;
      threads?: LFThread[];
      assistants?: LFAssistant[];
      files?: FileObject[];
      keys?: APIKeyRow[];
      isUsingOpenAI?: boolean;
    }

    // interface PageState {}
    // interface Platform {}
  }
}

export {};
