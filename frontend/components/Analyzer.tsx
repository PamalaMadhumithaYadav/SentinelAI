"use client";

import React, { useState } from "react";
import { AlertCircle, ShieldAlert, ArrowRight } from "lucide-react";

interface DecisionTrace {
    llm_threat: string;
    confidence: number;
    risk_score: number;
    base_action: string;
    memory_hits: number;
    final_action: string;
}

interface AnalysisResult {
    threat_type: string;
    risk_score: number;
    action: string;
    confidence_level: string;
    decision_trace: DecisionTrace;
    reason: string;
}

const Analyzer = () => {
    const [message, setMessage] = useState("");
    const [result, setResult] = useState<AnalysisResult | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleAnalyze = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!message.trim()) return;

        setLoading(true);
        setError("");
        setResult(null);

        const payload = { message };

        const callProxy = async () => {
            const res = await fetch("/api/analyze", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
            });

            if (!res.ok) {
                throw new Error("Backend not reachable");
            }

            return res.json();
        };

        try {
            const data = await callProxy();
            setResult(data);
        } catch {
            try {
                // Cloud Run cold start retry
                setError("Waking up security agent…");
                await new Promise((resolve) => setTimeout(resolve, 2000));

                const data = await callProxy();
                setResult(data);
                setError("");
            } catch {
                setError("Failed to connect to the security agent. Please try again.");
            }
        } finally {
            setLoading(false);
        }
    };

    const getRiskColor = (score: number) => {
        if (score < 50) return "text-green-500";
        if (score < 80) return "text-yellow-500";
        return "text-red-500";
    };

    const getActionBadge = (action: string) => {
        switch (action) {
            case "block":
                return (
                    <span className="px-3 py-1 rounded-full bg-red-100 text-red-800 text-sm font-medium">
                        BLOCK
                    </span>
                );
            case "flag":
                return (
                    <span className="px-3 py-1 rounded-full bg-yellow-100 text-yellow-800 text-sm font-medium">
                        FLAG
                    </span>
                );
            default:
                return (
                    <span className="px-3 py-1 rounded-full bg-green-100 text-green-800 text-sm font-medium">
                        ALLOW
                    </span>
                );
        }
    };

    return (
        <div className="w-full max-w-3xl mx-auto bg-white dark:bg-gray-800 rounded-xl shadow-2xl border border-gray-200 dark:border-gray-700">
            <div className="p-8">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-2">
                    <ShieldAlert className="h-6 w-6 text-blue-500" />
                    Live Threat Analyzer
                </h2>

                <form onSubmit={handleAnalyze} className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            Paste a suspicious message (email, SMS, or chat)
                        </label>
                        <textarea
                            rows={4}
                            className="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white"
                            placeholder="e.g. 'Update your password immediately at http://fake-link.com'"
                            value={message}
                            onChange={(e) => setMessage(e.target.value)}
                        />
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full flex items-center justify-center py-3 px-6 rounded-lg text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50"
                    >
                        {loading ? "Analyzing…" : <>Analyze Message <ArrowRight className="ml-2 h-5 w-5" /></>}
                    </button>
                </form>

                {error && (
                    <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center gap-3 text-red-700">
                        <AlertCircle className="h-5 w-5" />
                        {error}
                    </div>
                )}

                {result && (
                    <div className="mt-8 border-t pt-8">
                        <div className="grid grid-cols-2 gap-4 mb-6">
                            <div className="p-4 bg-gray-100 dark:bg-gray-700 rounded-lg">
                                <p className="text-sm text-gray-500">Threat Type</p>
                                <p className="text-lg font-bold capitalize">{result.threat_type}</p>
                            </div>
                            <div className="p-4 bg-gray-100 dark:bg-gray-700 rounded-lg">
                                <p className="text-sm text-gray-500">Risk Score</p>
                                <p className={`text-2xl font-bold ${getRiskColor(result.risk_score)}`}>
                                    {result.risk_score}/100
                                </p>
                            </div>
                        </div>

                        <div className="flex justify-between items-center mb-4">
                            <span className="font-medium">Recommended Action</span>
                            {getActionBadge(result.action)}
                        </div>

                        <div className="p-4 bg-blue-50 dark:bg-blue-900/30 rounded-lg">
                            <p className="font-medium mb-2">Analysis Reason</p>
                            <p className="text-sm">{result.reason}</p>
                        </div>

                        <details className="mt-6">
                            <summary className="cursor-pointer text-sm text-gray-500">
                                View Decision Trace (Debug)
                            </summary>
                            <pre className="mt-2 p-4 bg-black text-green-400 text-xs rounded-lg overflow-x-auto">
                                {JSON.stringify(result.decision_trace, null, 2)}
                            </pre>
                        </details>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Analyzer;