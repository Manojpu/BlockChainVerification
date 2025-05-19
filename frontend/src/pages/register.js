import React from 'react';
import RegisterForm from '../components/auth/RegisterForm';

const RegisterPage = () => {
    return (
        <div className="flex justify-center items-center h-screen">
            <div className="w-full max-w-md">
                <h2 className="text-2xl font-bold mb-6">Register</h2>
                <RegisterForm />
            </div>
        </div>
    );
};

export default RegisterPage;