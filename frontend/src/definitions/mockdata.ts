import { Resume } from "@/types";

// Mock data for resumes
export const mockResumes: Resume[] = [
  {
    _id: "1",
    resume_id: "res_001",
    job_id: "job_001",
    username: "johndoe",
    name: "John Doe",
    email: "john.doe@example.com",
    phone: "+1 (123) 456-7890",
    status: "APPLICATION_SUBMITTED",
    is_verified: "PENDING",
    ranking_score: 85.4,
    education: [
      {
        send: {
          degree: "Bachelor of Computer Science",
          institution: "MIT",
        },
        actual: {
          degree: null,
          institution: null,
        },
        verified: false,
      },
      {
        send: {
          degree: "Master of Business Administration",
          institution: "Harvard Business School",
        },
        actual: {
          degree: "Master of Business Administration",
          institution: "Harvard Extension School",
        },
        verified: false,
      },
    ],
    work_experience: [
      {
        send: {
          position: "Software Engineer",
          company: "Google",
        },
        actual: {
          position: "Software Engineer Intern",
          company: "Google",
        },
        verified: false,
      },
      {
        send: {
          position: "Senior Developer",
          company: "Microsoft",
        },
        actual: {
          position: null,
          company: null,
        },
        verified: false,
      },
    ],
  },
  {
    _id: "2",
    resume_id: "res_002",
    job_id: "job_002",
    username: "janesmith",
    name: "Jane Smith",
    email: "jane.smith@example.com",
    phone: "+1 (234) 567-8901",
    status: "INTERVIEW_SCHEDULED",
    is_verified: "VERIFIED",
    ranking_score: 92.7,
    education: [
      {
        send: {
          degree: "Bachelor of Arts in Psychology",
          institution: "Stanford University",
        },
        actual: {
          degree: "Bachelor of Arts in Psychology",
          institution: "Stanford University",
        },
        verified: true,
      },
    ],
    work_experience: [
      {
        send: {
          position: "Product Manager",
          company: "Apple",
        },
        actual: {
          position: "Product Manager",
          company: "Apple",
        },
        verified: true,
      },
      {
        send: {
          position: "UX Designer",
          company: "Facebook",
        },
        actual: {
          position: "UX Designer",
          company: "Facebook",
        },
        verified: true,
      },
    ],
  },
  {
    _id: "3",
    resume_id: "res_003",
    job_id: "job_003",
    username: "robertjohnson",
    name: "Robert Johnson",
    email: "robert.johnson@example.com",
    phone: "+1 (345) 678-9012",
    status: "APPLICATION_REJECTED",
    is_verified: "REJECTED",
    ranking_score: 45.3,
    education: [
      {
        send: {
          degree: "Ph.D in Computer Science",
          institution: "Carnegie Mellon University",
        },
        actual: {
          degree: "Master's in Computer Science",
          institution: "Local Community College",
        },
        verified: false,
      },
    ],
    work_experience: [
      {
        send: {
          position: "CTO",
          company: "Amazon",
        },
        actual: {
          position: "IT Support Specialist",
          company: "Small Local Shop",
        },
        verified: false,
      },
    ],
  },
];
