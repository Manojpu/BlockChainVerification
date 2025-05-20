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

export interface Resume {
  _id: string;
  resume_id: string;
  job_id: string;
  username: string;
  is_verified: "VERIFIED" | "PENDING" | "REJECTED";
  status: string;
  ranking_score: number;
  name: string;
  email: string;
  phone: string;
  education: Education[];
  work_experience: WorkExperience[];
}
