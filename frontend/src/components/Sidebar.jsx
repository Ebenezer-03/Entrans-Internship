import React from 'react';
import { LayoutDashboard, MessageSquare, FileText, Settings, Activity } from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';

const Sidebar = () => {
    const location = useLocation();

    const menuItems = [
        { icon: LayoutDashboard, label: 'Dashboard', path: '/' },
        { icon: MessageSquare, label: 'Chat Agent', path: '/chat' },
        { icon: Activity, label: 'Benchmark', path: '/benchmark' },
        { icon: FileText, label: 'Reports', path: '/reports' },
    ];

    return (
        <div className="h-screen w-64 bg-sidebar-purple text-white flex flex-col shadow-2xl fixed left-0 top-0">
            <div className="p-6">
                <h1 className="text-2xl font-bold tracking-wider">
                    WRITE<span className="text-gradient-pink">BOT</span>
                </h1>
                <p className="text-xs text-gray-300 mt-1">AI News Intelligence</p>
            </div>

            <nav className="flex-1 px-4 space-y-2 mt-4">
                {menuItems.map((item) => {
                    const Icon = item.icon;
                    const isActive = location.pathname === item.path;

                    return (
                        <Link
                            key={item.path}
                            to={item.path}
                            className={`flex items-center space-x-3 px-4 py-3 rounded-xl transition-all duration-200 ${isActive
                                    ? 'bg-white/10 text-white shadow-lg backdrop-blur-sm border border-white/10'
                                    : 'text-gray-300 hover:bg-white/5 hover:text-white'
                                }`}
                        >
                            <Icon size={20} />
                            <span className="font-medium">{item.label}</span>
                        </Link>
                    );
                })}
            </nav>

            <div className="p-4 border-t border-white/10">
                <Link to="/settings" className="flex items-center space-x-3 px-4 py-2 text-gray-400 hover:text-white cursor-pointer transition-colors">
                    <Settings size={20} />
                    <span>Settings</span>
                </Link>
            </div>
        </div>
    );
};

export default Sidebar;
