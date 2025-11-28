import React from 'react';
import { FileText, ExternalLink } from 'lucide-react';

const RAGResults = ({ data }) => {
    return (
        <div className="w-full max-w-2xl bg-white rounded-xl shadow-lg border border-gray-100 overflow-hidden">
            <div className="bg-gray-50 p-4 border-b border-gray-100 flex justify-between items-center">
                <div className="flex items-center space-x-2 text-primary font-semibold">
                    <FileText size={18} />
                    <span>RAG Retrieval Results</span>
                </div>
                <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full">
                    {data.sources.length} Sources
                </span>
            </div>

            <div className="p-4 space-y-4">
                <div>
                    <h4 className="text-sm font-medium text-gray-500 mb-2 uppercase tracking-wider">Generated Answer</h4>
                    <p className="text-gray-800 leading-relaxed">{data.final_answer}</p>
                </div>

                <div>
                    <h4 className="text-sm font-medium text-gray-500 mb-2 uppercase tracking-wider">Sources</h4>
                    <div className="space-y-2">
                        {data.sources.map((source, idx) => (
                            <a
                                key={idx}
                                href={`#article-${idx}`}
                                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-primary/10 transition-colors cursor-pointer group"
                            >
                                <span className="text-sm text-gray-700 truncate flex-1 group-hover:text-primary">{source}</span>
                                <ExternalLink size={14} className="text-gray-400 ml-2 group-hover:text-primary" />
                            </a>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default RAGResults;
