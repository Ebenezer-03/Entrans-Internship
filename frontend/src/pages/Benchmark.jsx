import React, { useEffect, useState } from 'react';
import { api } from '../api/client';
import { BarChart3, Activity, Zap } from 'lucide-react';

const Benchmark = () => {
    const [loading, setLoading] = useState(false);
    const [results, setResults] = useState(null);

    useEffect(() => {
        runBenchmark();
    }, []);

    const runBenchmark = async () => {
        setLoading(true);
        try {
            const response = await api.benchmark();
            if (response.data.status === 'success') {
                // Extract metrics block
                const metricsBlock = response.data.ui_blocks.find(b => b.type === 'metrics');
                if (metricsBlock) {
                    setResults(metricsBlock.items); // Fixed: was metricsBlock.data
                }
            }
        } catch (error) {
            console.error("Benchmark failed:", error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="p-8 space-y-8">
            <div>
                <h1 className="text-3xl font-bold text-gray-800">Model Benchmark</h1>
                <p className="text-gray-500 mt-1">Compare performance of Traditional, NLU, and LLM models.</p>
            </div>

            <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100">
                <div className="flex items-center justify-between mb-8">
                    <div>
                        <h3 className="text-xl font-bold text-gray-800">Performance Metrics</h3>
                        <p className="text-sm text-gray-500">Accuracy, F1 Score, and Latency comparison</p>
                    </div>
                    <button
                        onClick={runBenchmark}
                        disabled={loading}
                        className="px-6 py-3 bg-primary text-white rounded-xl hover:bg-primary/90 transition-all disabled:opacity-50 flex items-center space-x-2"
                    >
                        {loading ? <Activity className="animate-spin" /> : <Zap size={20} />}
                        <span>Run Benchmark</span>
                    </button>
                </div>

                {results ? (
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        {results.map((metric, idx) => (
                            <div key={idx} className="p-6 bg-gray-50 rounded-xl border border-gray-100">
                                <p className="text-sm text-gray-500 mb-1">{metric.label}</p>
                                <h4 className="text-2xl font-bold text-gray-800">{metric.value}</h4>
                                <span className="text-xs text-green-600 font-medium">{metric.change} vs baseline</span>
                            </div>
                        ))}
                    </div>
                ) : (
                    <div className="text-center py-12 bg-gray-50 rounded-xl border border-dashed border-gray-200">
                        <BarChart3 className="mx-auto text-gray-300 mb-3" size={48} />
                        <p className="text-gray-500">Click "Run Benchmark" to start the evaluation.</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Benchmark;
