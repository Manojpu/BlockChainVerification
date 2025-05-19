import React from 'react';
import ResumeCard from './ResumeCard';

const ResumeList = ({ resumes }) => {
    return (
        <div className="resume-list">
            {resumes.length > 0 ? (
                resumes.map(resume => (
                    <ResumeCard key={resume.id} resume={resume} />
                ))
            ) : (
                <p>No resumes available.</p>
            )}
        </div>
    );
};

export default ResumeList;