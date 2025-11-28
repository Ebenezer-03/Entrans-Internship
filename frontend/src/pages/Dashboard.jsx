import React, { useEffect, useState } from 'react';
import { api } from '../api/client';
import { Download, Database, Zap, BarChart3, FileText, Activity, MessageSquare } from 'lucide-react';

const Dashboard = () => {
    const [metrics, setMetrics] = useState([]);
    const [recentActivity, setRecentActivity] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchData();
        // Auto-refresh every 3 seconds
        const interval = setInterval(fetchData, 3000);
        return () => clearInterval(interval);
    }, []);

    const fetchData = async () => {
        try {
            const [metricsRes, activityRes] = await Promise.all([
                api.getMetrics(),
                api.getRecentActivity()
            ]);

            if (metricsRes.data.status === 'success') {
                setMetrics(metricsRes.data.metrics);
            }

            if (activityRes.data.status === 'success') {
                setRecentActivity(activityRes.data.activities);
            }

            setLoading(false);
        } catch (error) {
            console.error("Failed to fetch dashboard data:", error);
            setLoading(false);
        }
    };

    const downloadReport = async () => {
        try {
            const response = await api.generatePdfReport();
            const blob = new Blob([response.data], { type: 'application/pdf' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'report.pdf';
            a.click();
        } catch (error) {
            console.error("PDF download failed:", error);
        }
    };

    const getIcon = (iconName) => {
        const icons = {
            'Database': Database,
            'Zap': Zap,
            'BarChart3': BarChart3,
            'FileText': FileText
        };
        const Icon = icons[iconName] || Database;
        return <Icon size={24} />;
    };

    const getModeIcon = (mode) => {
        if (mode === 'rag') {
            return <Database size={16} className="text-primary" />;
        }
        return <MessageSquare size={16} className="text-purple-500" />;
    };

    const getModeLabel = (mode) => {
        return mode === 'rag' ? 'RAG Search' : 'Chat';
    };

    return (
        <div className="p-8 space-y-8">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold text-gray-800">Dashboard</h1>
                    <p className="text-gray-500 mt-1">Real-time system overview and analytics</p>
                </div>
                <button
                    onClick={downloadReport}
                    className="px-6 py-3 bg-primary text-white rounded-xl hover:bg-primary/90 transition-all flex items-center space-x-2"
                >
                    <Download size={20} />
                    <span>Download Report</span>
                </button>
            </div>

            {/* Metrics Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {metrics.map((metric, idx) => (
                    <div key={idx} className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                        <div className="flex items-center justify-between mb-3">
                            <div className="p-3 bg-primary/10 rounded-xl text-primary">
                                {getIcon(metric.icon)}
                            </div>
                            <span className="text-xs text-green-600 font-medium">{metric.change}</span>
                        </div>
                        <h3 className="text-2xl font-bold text-gray-800 mb-1">{metric.value}</h3>
                        <p className="text-sm text-gray-500">{metric.title}</p>
                    </div>
                ))}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Recent Activity */}
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
                    <div className="flex items-center justify-between mb-6">
                        <h3 className="text-xl font-bold text-gray-800 flex items-center space-x-2">
                            <Activity size={24} className="text-primary" />
                            <span>Recent Activity</span>
                        </h3>
                        <div className="flex items-center space-x-2">
                            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                            <span className="text-xs text-gray-500">Live</span>
                        </div>
                    </div>

                    {loading ? (
                        <div className="space-y-4">
                            {[1, 2, 3].map(i => (
                                <div key={i} className="h-16 bg-gray-100 rounded-xl animate-pulse"></div>
                            ))}
                        </div>
                    ) : recentActivity.length > 0 ? (
                        <div className="space-y-3 max-h-96 overflow-y-auto">
                            {recentActivity.map((activity, idx) => (
                                <div key={idx} className="p-4 bg-gray-50 rounded-xl border border-gray-100 hover:border-primary/30 transition-colors">
                                    <div className="flex items-start justify-between">
                                        <div className="flex-1">
                                            <div className="flex items-center space-x-2 mb-1">
                                                {getModeIcon(activity.mode)}
                                                <span className="text-xs font-medium text-gray-500">{getModeLabel(activity.mode)}</span>
                                            </div>
                                            <p className="text-sm text-gray-800 line-clamp-2">{activity.query}</p>
                                        </div>
                                        <span className="text-xs text-gray-400 ml-3 whitespace-nowrap">{activity.timestamp}</span>
                                    </div>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <div className="text-center py-12 text-gray-400">
                            <Activity size={48} className="mx-auto mb-3 opacity-30" />
                            <p>No activity yet. Start by asking a question!</p>
                        </div>
                    )}
                </div>

                {/* System Status */}
                <div className="bg-gradient-to-br from-primary to-purple-600 p-6 rounded-2xl shadow-lg text-white">
                    <h3 className="text-xl font-bold mb-3">System Status</h3>
                    <p className="text-white/80 mb-6">All systems operational. Gemini AI connected.</p>

                    <div className="space-y-3">
                        <div className="flex items-center justify-between p-3 bg-white/10 rounded-xl backdrop-blur-sm">
                            <div className="flex items-center space-x-3">
                                <div className="w-3 h-3 bg-green-400 rounded-full"></div>
                                <span>Gemini 2.0 Flash</span>
                            </div>
                            <span className="text-sm text-white/70">Online</span>
                        </div>

                        <div className="flex items-center justify-between p-3 bg-white/10 rounded-xl backdrop-blur-sm">
                            <div className="flex items-center space-x-3">
                                <div className="w-3 h-3 bg-green-400 rounded-full"></div>
                                <span>Database</span>
                            </div>
                            <span className="text-sm text-white/70">Connected</span>
                        </div>

                        <div className="flex items-center justify-between p-3 bg-white/10 rounded-xl backdrop-blur-sm">
                            <div className="flex items-center space-x-3">
                                <div className="w-3 h-3 bg-green-400 rounded-full"></div>
                                <span>RAG System</span>
                            </div>
                            <span className="text-sm text-white/70">Active</span>
                        </div>
                    </div>

                    <div className="mt-6 p-4 bg-white/10 rounded-xl backdrop-blur-sm">
                        <p className="text-sm text-white/90 mb-2">Quick Stats</p>
                        <div className="grid grid-cols-2 gap-3">
                            <div>
                                <p className="text-2xl font-bold">{metrics.find(m => m.title === 'Total Articles')?.value || '0'}</p>
                                <p className="text-xs text-white/70">Articles Indexed</p>
                            </div>
                            <div>
                                <p className="text-2xl font-bold">{metrics.find(m => m.title === 'Total Queries')?.value || '0'}</p>
                                <p className="text-xs text-white/70">Queries Processed</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
