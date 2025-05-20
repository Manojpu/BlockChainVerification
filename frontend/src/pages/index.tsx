import React from "react";
import Link from "next/link";
import { Shield, File, Database, Award } from "lucide-react";
import Head from "next/head";

const HomePage = () => {
  return (
    <>
      <Head>
        <title>ResVerify | Blockchain Resume Verification</title>
        <meta
          name="description"
          content="Secure and transparent resume verification using blockchain technology"
        />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
        {/* Navigation - Modernized with better spacing and hover effects */}
        <nav className="bg-white shadow-sm sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex items-center">
                <Link href="/" className="flex items-center">
                  <Shield className="h-8 w-8 text-blue-600 mr-2" />
                  <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600">
                    ResVerify
                  </span>
                </Link>
              </div>
              <div className="flex items-center space-x-6">
                <Link
                  href="/login"
                  className="text-gray-600 hover:text-blue-600 transition duration-150 text-sm font-medium"
                >
                  Login
                </Link>
                <Link
                  href="/register"
                  className="bg-blue-700 !text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700 transition duration-150"
                >
                  Register
                </Link>
              </div>
            </div>
          </div>
        </nav>

        {/* Hero Section - Improved with modern design and better visual hierarchy */}
        <div className="relative overflow-hidden">
          <div className="max-w-7xl mx-auto">
            <div className="relative z-10 py-12 sm:py-16 md:py-20 lg:py-28 lg:max-w-2xl lg:w-full">
              <main className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                <div className="sm:text-center lg:text-left">
                  <h1 className="text-4xl tracking-tight font-extrabold text-gray-900 sm:text-5xl md:text-6xl">
                    <span className="block">Verify credentials with</span>{" "}
                    <span className="block text-blue-600">
                      blockchain security
                    </span>
                  </h1>
                  <p className="mt-4 text-xl text-gray-500 sm:mt-6 sm:max-w-xl sm:mx-auto lg:mx-0">
                    Our immutable blockchain platform ensures credentials remain
                    tamper-proof, providing transparency and trust in the
                    verification process.
                  </p>
                  <div className="mt-8 sm:mt-10 sm:flex sm:justify-center lg:justify-start gap-4">
                    <Link
                      href="/register"
                      className="w-full sm:w-auto flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md !text-white bg-blue-600 hover:bg-blue-700 transition duration-150 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 md:py-4 md:text-lg md:px-10"
                    >
                      Get started
                    </Link>

                    <Link
                      href="/learn-more"
                      className="mt-3 sm:mt-0 w-full sm:w-auto flex items-center justify-center px-8 py-3 border border-blue-200 text-base font-medium rounded-md text-blue-700 bg-white hover:bg-blue-50 transition duration-150 md:py-4 md:text-lg md:px-10"
                    >
                      Learn more
                    </Link>
                  </div>
                </div>
              </main>
            </div>
          </div>
          <div className="lg:absolute lg:inset-y-0 lg:right-0 lg:w-1/2 hidden lg:block">
            <div className="h-56 w-full bg-gradient-to-br from-blue-100 to-indigo-200 sm:h-72 md:h-96 lg:w-full lg:h-full flex items-center justify-center rounded-bl-3xl shadow-inner">
              <img
                src="/resume-verification.svg"
                alt="Resume verification illustration"
                className="max-h-full max-w-full p-8"
              />
            </div>
          </div>
        </div>

        {/* Features Section - Redesigned with modern cards and better spacing */}
        <div className="py-16 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center">
              <h2 className="text-base text-blue-600 font-semibold tracking-wide uppercase">
                Features
              </h2>
              <p className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
                Blockchain-powered verification
              </p>
              <p className="mt-4 max-w-2xl text-xl text-gray-500 mx-auto">
                Our platform provides tamper-proof credential verification
                through advanced blockchain technology.
              </p>
            </div>

            <div className="mt-16">
              <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
                {/* Feature cards with improved visual styling */}
                <div className="bg-gradient-to-br from-white to-blue-50 rounded-xl shadow-md hover:shadow-lg transition duration-300 overflow-hidden">
                  <div className="p-6">
                    <div className="flex items-center">
                      <div className="flex items-center justify-center h-12 w-12 rounded-md bg-blue-600 text-white">
                        <Shield className="h-6 w-6" />
                      </div>
                      <h3 className="ml-3 text-xl font-medium text-gray-900">
                        Immutable Records
                      </h3>
                    </div>
                    <div className="mt-4 text-base text-gray-500">
                      All verifications are permanently stored on the
                      blockchain, making them tamper-proof and always
                      accessible.
                    </div>
                  </div>
                </div>

                <div className="bg-gradient-to-br from-white to-blue-50 rounded-xl shadow-md hover:shadow-lg transition duration-300 overflow-hidden">
                  <div className="p-6">
                    <div className="flex items-center">
                      <div className="flex items-center justify-center h-12 w-12 rounded-md bg-blue-600 text-white">
                        <Database className="h-6 w-6" />
                      </div>
                      <h3 className="ml-3 text-xl font-medium text-gray-900">
                        Decentralized Trust
                      </h3>
                    </div>
                    <div className="mt-4 text-base text-gray-500">
                      Eliminate reliance on central authorities with our
                      decentralized verification system.
                    </div>
                  </div>
                </div>

                <div className="bg-gradient-to-br from-white to-blue-50 rounded-xl shadow-md hover:shadow-lg transition duration-300 overflow-hidden">
                  <div className="p-6">
                    <div className="flex items-center">
                      <div className="flex items-center justify-center h-12 w-12 rounded-md bg-blue-600 text-white">
                        <Award className="h-6 w-6" />
                      </div>
                      <h3 className="ml-3 text-xl font-medium text-gray-900">
                        Credential Authenticity
                      </h3>
                    </div>
                    <div className="mt-4 text-base text-gray-500">
                      Verify educational credentials, work experience, and
                      certifications with confidence.
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* CTA Section - Enhanced with modern gradient background */}
        <div className="bg-gradient-to-r from-blue-600 to-indigo-700">
          <div className="max-w-2xl mx-auto text-center py-16 px-4 sm:py-20 sm:px-6 lg:px-8">
            <h2 className="text-3xl font-extrabold text-white sm:text-4xl">
              <span className="block">Ready to verify with confidence?</span>
            </h2>
            <p className="mt-4 text-lg leading-6 text-blue-100">
              Join organizations worldwide that rely on our blockchain platform
              for secure resume verification.
            </p>
            <div className="mt-8 flex flex-col sm:flex-row justify-center gap-4">
              <Link
                href="/register"
                className="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-blue-600 bg-white hover:bg-gray-50 shadow-md hover:shadow-lg transition"
              >
                Create free account
              </Link>
              <Link
                href="/demo"
                className="inline-flex items-center justify-center px-5 py-3 border border-white text-base font-medium rounded-md !text-white hover:bg-blue-500 transition"
              >
                Request a demo
              </Link>
            </div>
          </div>
        </div>

        {/* Footer - Redesigned with simpler, cleaner layout */}
        <footer className="bg-gray-800">
          <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-2 gap-8 md:grid-cols-4">
              <div>
                <h3 className="text-sm font-semibold text-gray-400 tracking-wider uppercase">
                  Solutions
                </h3>
                <ul className="mt-4 space-y-4">
                  <li>
                    <Link
                      href="/solutions/verification"
                      className="text-base text-gray-300 hover:text-white"
                    >
                      Resume Verification
                    </Link>
                  </li>
                  <li>
                    <Link
                      href="/solutions/credentials"
                      className="text-base text-gray-300 hover:text-white"
                    >
                      Credential Checks
                    </Link>
                  </li>
                  <li>
                    <Link
                      href="/solutions/references"
                      className="text-base text-gray-300 hover:text-white"
                    >
                      Reference Validation
                    </Link>
                  </li>
                </ul>
              </div>
              <div>
                <h3 className="text-sm font-semibold text-gray-400 tracking-wider uppercase">
                  Company
                </h3>
                <ul className="mt-4 space-y-4">
                  <li>
                    <Link
                      href="/about"
                      className="text-base text-gray-300 hover:text-white"
                    >
                      About
                    </Link>
                  </li>
                  <li>
                    <Link
                      href="/careers"
                      className="text-base text-gray-300 hover:text-white"
                    >
                      Careers
                    </Link>
                  </li>
                  <li>
                    <Link
                      href="/contact"
                      className="text-base text-gray-300 hover:text-white"
                    >
                      Contact
                    </Link>
                  </li>
                </ul>
              </div>
              <div>
                <h3 className="text-sm font-semibold text-gray-400 tracking-wider uppercase">
                  Resources
                </h3>
                <ul className="mt-4 space-y-4">
                  <li>
                    <Link
                      href="/docs"
                      className="text-base text-gray-300 hover:text-white"
                    >
                      Documentation
                    </Link>
                  </li>
                  <li>
                    <Link
                      href="/blog"
                      className="text-base text-gray-300 hover:text-white"
                    >
                      Blog
                    </Link>
                  </li>
                  <li>
                    <Link
                      href="/support"
                      className="text-base text-gray-300 hover:text-white"
                    >
                      Support
                    </Link>
                  </li>
                </ul>
              </div>
              <div>
                <h3 className="text-sm font-semibold text-gray-400 tracking-wider uppercase">
                  Legal
                </h3>
                <ul className="mt-4 space-y-4">
                  <li>
                    <Link
                      href="/privacy"
                      className="text-base text-gray-300 hover:text-white"
                    >
                      Privacy
                    </Link>
                  </li>
                  <li>
                    <Link
                      href="/terms"
                      className="text-base text-gray-300 hover:text-white"
                    >
                      Terms
                    </Link>
                  </li>
                  <li>
                    <Link
                      href="/security"
                      className="text-base text-gray-300 hover:text-white"
                    >
                      Security
                    </Link>
                  </li>
                </ul>
              </div>
            </div>
            <div className="mt-8 border-t border-gray-700 pt-8 md:flex md:items-center md:justify-between">
              <div className="flex space-x-6 md:order-2">
                <Link
                  href="https://facebook.com"
                  className="text-gray-400 hover:text-gray-300"
                >
                  <span className="sr-only">Facebook</span>
                  <svg
                    className="h-6 w-6"
                    fill="currentColor"
                    viewBox="0 0 24 24"
                    aria-hidden="true"
                  >
                    <path
                      fillRule="evenodd"
                      d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z"
                      clipRule="evenodd"
                    />
                  </svg>
                </Link>
                <Link
                  href="https://twitter.com"
                  className="text-gray-400 hover:text-gray-300"
                >
                  <span className="sr-only">Twitter</span>
                  <svg
                    className="h-6 w-6"
                    fill="currentColor"
                    viewBox="0 0 24 24"
                    aria-hidden="true"
                  >
                    <path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84" />
                  </svg>
                </Link>
                <Link
                  href="https://linkedin.com"
                  className="text-gray-400 hover:text-gray-300"
                >
                  <span className="sr-only">LinkedIn</span>
                  <svg
                    className="h-6 w-6"
                    fill="currentColor"
                    viewBox="0 0 24 24"
                    aria-hidden="true"
                  >
                    <path
                      fillRule="evenodd"
                      d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"
                      clipRule="evenodd"
                    />
                  </svg>
                </Link>
              </div>
              <p className="mt-8 text-base text-gray-400 md:mt-0 md:order-1">
                &copy; {new Date().getFullYear()} ResVerify. All rights
                reserved.
              </p>
            </div>
          </div>
        </footer>
      </div>
    </>
  );
};

export default HomePage;
