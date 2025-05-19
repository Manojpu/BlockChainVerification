import React from 'react';
import Link from 'next/link';

const HomePage = () => {
    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
            <h1 className="text-4xl font-bold mb-4">Welcome to the Resume Verification App</h1>
            <p className="text-lg mb-8">Verify your resumes securely and efficiently.</p>
            <div className="flex space-x-4">
                <Link href="/login">
                    <a className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">Login</a>
                </Link>
                <Link href="/register">
                    <a className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600">Register</a>
                </Link>
                <Link href="/upload">
                    <a className="px-4 py-2 bg-yellow-500 text-white rounded hover:bg-yellow-600">Upload Resume</a>
                </Link>
            </div>
        </div>
    );
};

export default HomePage;