export interface TranscriptionEntry {
  id: string;
  role: 'user' | 'model';
  text: string;
  timestamp: number;
}

export const SessionStatus = {
  IDLE: 'IDLE',
  CONNECTING: 'CONNECTING',
  ACTIVE: 'ACTIVE',
  ERROR: 'ERROR'
} as const;

export type SessionStatus = (typeof SessionStatus)[keyof typeof SessionStatus];
