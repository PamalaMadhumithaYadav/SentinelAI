import React from 'react';
import { ShieldCheck } from 'lucide-react';

const Hero = () => {
    return (
        <div className="bg-white dark:bg-gray-900 overflow-hidden relative">
            <div className="absolute inset-0 z-0">
                <div className="absolute inset-0 bg-gradient-to-r from-blue-500/10 to-purple-500/10 dark:from-blue-900/20 dark:to-purple-900/20" />
            </div>
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16 text-center lg:pt-32 z-10 relative">
                <div className="mx-auto max-w-3xl">
                    <div className="flex justify-center mb-6">
                        <span className="inline-flex items-center px-4 py-1.5 rounded-full text-sm font-semibold bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200">
                            <ShieldCheck className="w-4 h-4 mr-2" />
                            Production-Grade Security Agent
                        </span>
                    </div>
                    <h1 className="text-4xl font-extrabold text-gray-900 dark:text-white sm:text-5xl md:text-6xl tracking-tight mb-6">
                        Protect Yourself From <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-400 dark:to-purple-400">Cyber Threats</span> in Real Time
                    </h1>
                    <p className="mt-4 text-xl text-gray-500 dark:text-gray-400 max-w-2xl mx-auto mb-10">
                        Our advanced AI analyzes messages instantly to detect phishing, scams, malware, and impersonation attempts with military-grade precision.
                    </p>
                    <div className="flex justify-center gap-4">
                        <a href="#analyzer" className="px-8 py-3 rounded-lg bg-blue-600 text-white font-semibold hover:bg-blue-700 transition shadow-lg shadow-blue-500/30">
                            Analyze a Message
                        </a>
                        <a href="#features" className="px-8 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-200 font-semibold hover:bg-gray-200 dark:hover:bg-gray-700 transition">
                            Learn More
                        </a>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Hero;
