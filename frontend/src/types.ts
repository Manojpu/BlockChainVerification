export interface Education {
  send: {
    degree: string;
    institution: string;
  };
  actual: {
    degree: string | null;
    institution: string | null;
  };
  verified: boolean;
}

export interface WorkExperience {
  send: {
    position: string;
    company: string;
  };
  actual: {
    position: string | null;
    company: string | null;
  };
  verified: boolean;
}

// Add or update in your types.ts file
export interface Resume {
  _id: string;
  job_id: string;
  username: string;
  is_verified: string; // "PENDING", "VERIFIED", or "REJECTED"
  status: string;
  ranking_score: number;
  name: string;
  email: string;
  phone: string;
  education: Array<{
    send: {
      degree: string;
      institution: string;
      gpa?: number;
    };
    actual?: {
      degree: string;
      institution: string;
      gpa?: number;
    };
    verified: string; // "PENDING", "BLOCKCHAIN_VERIFIED", "SUBMITTED", "VERIFIED", or "REJECTED"
  }>;
  work_experience: Array<{
    send: {
      position: string;
      company: string;
    };
    actual?: {
      position: string;
      company: string;
    };
    verified: string; // "PENDING", "BLOCKCHAIN_VERIFIED", "SUBMITTED", "VERIFIED", or "REJECTED"
  }>;
}
