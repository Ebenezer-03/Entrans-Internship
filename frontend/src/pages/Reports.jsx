import React from 'react';
import { api } from '../api/client';
import { FileText, Download } from 'lucide-react';

const Reports = () => {
    const handleReportGeneration = async () => {
        try {
            const response = await api.generatePdfReport();
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'ai_news_report.pdf');
            document.body.appendChild(link);
            link.click();
            link.remove();
        } catch (error) {
            console.error("Failed to generate report:", error);
        }
    };

    return (
        <div className="p-8 space-y-8">
            <div>
                <h1 className="text-3xl font-bold text-gray-800">Reports</h1>
                <p className="text-gray-500 mt-1">Generate and download system analysis reports.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {/* Daily Report Card */}
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-all group">
                    <div className="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center mb-4 group-hover:bg-primary group-hover:text-white transition-colors text-primary">
                        <FileText size={24} />
                    </div>
                    <h3 className="text-lg font-bold text-gray-800 mb-2">Daily Performance Report</h3>
                    <p className="text-sm text-gray-500 mb-6">Comprehensive summary of classification accuracy, RAG queries, and system health.</p>

                    <button
                        onClick={handleReportGeneration}
                        className="w-full py-3 border border-gray-200 rounded-xl text-gray-600 font-medium hover:bg-gray-50 transition-colors flex items-center justify-center space-x-2"
                    >
                        <Download size={18} />
                        <span>Download PDF</span>
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Reports;
