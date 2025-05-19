import React, { useState } from 'react';

const ResumeUploadForm = () => {
    const [file, setFile] = useState(null);
    const [error, setError] = useState(null);

    const handleFileChange = (event) => {
        const selectedFile = event.target.files[0];
        if (selectedFile && selectedFile.type === 'application/pdf') {
            setFile(selectedFile);
            setError(null);
        } else {
            setError('Please upload a valid PDF file.');
        }
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!file) {
            setError('Please select a file to upload.');
            return;
        }

        const formData = new FormData();
        formData.append('resume', file);

        try {
            const response = await fetch('/api/resumes/upload', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error('Failed to upload resume.');
            }

            // Handle successful upload (e.g., show a success message or redirect)
        } catch (error) {
            setError(error.message);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <div>
                <label htmlFor="resume">Upload Resume (PDF only):</label>
                <input type="file" id="resume" onChange={handleFileChange} />
                {error && <p style={{ color: 'red' }}>{error}</p>}
            </div>
            <button type="submit">Upload</button>
        </form>
    );
};

export default ResumeUploadForm;