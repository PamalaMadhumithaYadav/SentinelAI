import React from 'react';
import { Github, Twitter, Linkedin } from 'lucide-react';

const Footer = () => {
    return (
        <footer className="bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-800">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
                    <div className="col-span-1 md:col-span-2">
                        <span className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
                            🛡️ Chat Security Agent
                        </span>
                        <p className="mt-4 text-gray-500 dark:text-gray-400 max-w-xs">
                            Protecting digital conversations with advanced AI threat detection. secure, deterministic, and privacy-focused.
                        </p>
                    </div>
                    <div>
                        <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider">Product</h3>
                        <ul className="mt-4 space-y-4">
                            <li><a href="#" className="text-base text-gray-500 hover:text-gray-900 dark:hover:text-white">Features</a></li>
                            <li><a href="#" className="text-base text-gray-500 hover:text-gray-900 dark:hover:text-white">Security</a></li>
                            <li><a href="#" className="text-base text-gray-500 hover:text-gray-900 dark:hover:text-white">API Access</a></li>
                        </ul>
                    </div>
                    <div>
                        <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider">Legal</h3>
                        <ul className="mt-4 space-y-4">
                            <li><a href="#" className="text-base text-gray-500 hover:text-gray-900 dark:hover:text-white">Privacy</a></li>
                            <li><a href="#" className="text-base text-gray-500 hover:text-gray-900 dark:hover:text-white">Terms</a></li>
                        </ul>
                    </div>
                </div>
                <div className="mt-8 border-t border-gray-200 dark:border-gray-800 pt-8 flex justify-between items-center">
                    <p className="text-base text-gray-400">&copy; 2026 Chat Security Agent. All rights reserved.</p>
                    <div className="flex space-x-6">
                        <a href="#" className="text-gray-400 hover:text-gray-500">
                            <span className="sr-only">GitHub</span>
                            <Github className="h-6 w-6" />
                        </a>
                        <a href="#" className="text-gray-400 hover:text-gray-500">
                            <span className="sr-only">Twitter</span>
                            <Twitter className="h-6 w-6" />
                        </a>
                    </div>
                </div>
            </div>
        </footer>
    )
}

export default Footer;
