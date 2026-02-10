"use client";

import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line } from 'recharts';

const dataLosses = [
    { year: '2020', losses: 4.2 },
    { year: '2021', losses: 6.9 },
    { year: '2022', losses: 10.3 },
    { year: '2023', losses: 12.5 },
];

const dataThreats = [
    { name: 'Phishing', value: 300497 },
    { name: 'Personal Breach', value: 55851 },
    { name: 'Non-Payment', value: 50523 },
    { name: 'Extortion', value: 48771 },
    { name: 'Tech Support', value: 37570 },
];

const StatsSection = () => {
    return (
        <section className="py-12 bg-gray-900 text-white">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="text-center mb-12">
                    <h2 className="text-3xl font-extrabold sm:text-4xl">
                        The Rising Cost of Cybercrime
                    </h2>
                    <p className="mt-4 text-xl text-gray-400">
                        Real-world data showing the impact of digital threats.
                    </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    {/* Chart 1: Financial Losses */}
                    <div className="bg-gray-800 p-6 rounded-lg shadow-xl">
                        <h3 className="text-xl font-bold mb-4">Annual Losses (Billions USD)</h3>
                        <div className="h-64">
                            <ResponsiveContainer width="100%" height="100%">
                                <LineChart data={dataLosses}>
                                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                                    <XAxis dataKey="year" stroke="#9CA3AF" />
                                    <YAxis stroke="#9CA3AF" />
                                    <Tooltip
                                        contentStyle={{ backgroundColor: '#1F2937', border: 'none' }}
                                        itemStyle={{ color: '#F3F4F6' }}
                                    />
                                    <Line type="monotone" dataKey="losses" stroke="#3B82F6" strokeWidth={3} />
                                </LineChart>
                            </ResponsiveContainer>
                        </div>
                    </div>

                    {/* Chart 2: Top Threats */}
                    <div className="bg-gray-800 p-6 rounded-lg shadow-xl">
                        <h3 className="text-xl font-bold mb-4">Top Threats by Volume</h3>
                        <div className="h-64">
                            <ResponsiveContainer width="100%" height="100%">
                                <BarChart data={dataThreats} layout="vertical">
                                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                                    <XAxis type="number" stroke="#9CA3AF" />
                                    <YAxis dataKey="name" type="category" width={100} stroke="#9CA3AF" />
                                    <Tooltip
                                        contentStyle={{ backgroundColor: '#1F2937', border: 'none' }}
                                        itemStyle={{ color: '#F3F4F6' }}
                                    />
                                    <Bar dataKey="value" fill="#EF4444" radius={[0, 4, 4, 0]} />
                                </BarChart>
                            </ResponsiveContainer>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
};

export default StatsSection;
