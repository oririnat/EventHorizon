// models.ts

export interface ActorSchema {
  id: number;             // Actor ID
  login: string;          // Actor login
  avatar_url?: string;    // Actor avatar URL, optional
}

export interface RepositorySchema {
  id: number;             // Repository ID
  name: string;           // Repository name
  stars?: number;         // Star count, optional
}

export interface ValidationError {
  loc: (string | number)[];  // Location in the schema where the error occurred
  msg: string;               // Error message
  type: string;              // Error type
}

export interface EventSchema {
  id: string;                     // Event ID
  type: string;                   // Event type
  actor: ActorSchema;             // Actor object
  repository: RepositorySchema;   // Repository object
  created_at: string;             // Creation timestamp, in ISO 8601 format
}
