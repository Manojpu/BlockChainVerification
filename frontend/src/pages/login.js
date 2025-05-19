import React from 'react';
import LoginForm from '../components/auth/LoginForm';

const LoginPage = () => {
    return (
        <div className="flex items-center justify-center h-screen">
            <div className="w-full max-w-md">
                <h1 className="text-2xl font-bold mb-6">Login</h1>
                <LoginForm />
            </div>
        </div>
    );
};

export default LoginPage;