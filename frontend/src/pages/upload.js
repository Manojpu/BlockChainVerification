import React from 'react';
import ResumeUploadForm from '../components/forms/ResumeUploadForm';

const UploadPage = () => {
    return (
        <div className="container mx-auto p-4">
            <h1 className="text-2xl font-bold mb-4">Upload Your Resume</h1>
            <ResumeUploadForm />
        </div>
    );
};

export default UploadPage;