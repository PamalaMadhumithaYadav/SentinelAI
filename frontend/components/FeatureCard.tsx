import React from 'react';
import { Shield, AlertTriangle, Lock, UserX } from 'lucide-react';

interface FeatureCardProps {
    title: string;
    description: string;
    icon: 'shield' | 'alert' | 'lock' | 'user';
}

const icons = {
    shield: Shield,
    alert: AlertTriangle,
    lock: Lock,
    user: UserX,
};

const FeatureCard: React.FC<FeatureCardProps> = ({ title, description, icon }) => {
    const Icon = icons[icon];

    return (
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 border border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-center h-12 w-12 rounded-md bg-blue-500 text-white mb-4">
                <Icon className="h-6 w-6" />
            </div>
            <h3 className="text-lg font-medium text-gray-900 dark:text-white">{title}</h3>
            <p className="mt-2 text-base text-gray-500 dark:text-gray-400">{description}</p>
        </div>
    );
};

export default FeatureCard;
