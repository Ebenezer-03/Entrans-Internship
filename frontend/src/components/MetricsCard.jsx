import React from 'react';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

const MetricsCard = ({ title, value, change, icon: Icon }) => {
    const isPositive = change?.startsWith('+');
    const isNeutral = change === 'N/A' || !change;

    return (
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
            <div className="flex justify-between items-start">
                <div>
                    <p className="text-sm font-medium text-gray-500 mb-1">{title}</p>
                    <h3 className="text-3xl font-bold text-gray-800">{value}</h3>
                </div>
                <div className="p-3 bg-primary/10 rounded-xl text-primary">
                    {Icon && <Icon size={24} />}
                </div>
            </div>

            <div className="mt-4 flex items-center space-x-2">
                {isNeutral ? (
                    <span className="flex items-center text-gray-400 text-sm font-medium">
                        <Minus size={16} className="mr-1" />
                        Stable
                    </span>
                ) : (
                    <span className={`flex items-center text-sm font-medium ${isPositive ? 'text-green-500' : 'text-red-500'}`}>
                        {isPositive ? <TrendingUp size={16} className="mr-1" /> : <TrendingDown size={16} className="mr-1" />}
                        {change}
                    </span>
                )}
                <span className="text-xs text-gray-400">vs last run</span>
            </div>
        </div>
    );
};

export default MetricsCard;
