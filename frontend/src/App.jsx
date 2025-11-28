import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import Chat from './pages/Chat';

import Benchmark from './pages/Benchmark';
import Reports from './pages/Reports';
import Settings from './pages/Settings';

function App() {
    return (
        <Router>
            <div className="flex bg-background min-h-screen">
                <Sidebar />
                <main className="flex-1 ml-64">
                    <Routes>
                        <Route path="/" element={<Dashboard />} />
                        <Route path="/chat" element={<Chat />} />
                        <Route path="/benchmark" element={<Benchmark />} />
                        <Route path="/reports" element={<Reports />} />
                        <Route path="/settings" element={<Settings />} />
                    </Routes>
                </main>
            </div>
        </Router>
    );
}

export default App;
