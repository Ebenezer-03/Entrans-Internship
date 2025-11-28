import React, { useState, useEffect } from 'react';
import { Save, Key, Shield, AlertTriangle } from 'lucide-react';
import { api } from '../api/client';

const Settings = () => {
    const [apiKey, setApiKey] = useState('');
    const [saved, setSaved] = useState(false);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        // Check if key is already set (mock check)
        const checkStatus = async () => {
            try {
                const response = await api.getSettings();
                if (response.data.has_api_key) {
                    setApiKey('********************');
                    setSaved(true);
                }
            } catch (e) {
                console.log("Settings fetch failed", e);
            }
        };
        checkStatus();
    }, []);

    const handleSave = async () => {
        setLoading(true);
        try {
            await api.saveSettings({ google_api_key: apiKey });
            setSaved(true);
            alert("API Key saved! The system will restart to apply changes.");
        } catch (error) {
            console.error("Failed to save settings:", error);
            alert("Failed to save API Key.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="p-8 max-w-4xl mx-auto space-y-8">
            <div>
                <h1 className="text-3xl font-bold text-gray-800">Settings</h1>
                <p className="text-gray-500 mt-1">Configure your AI Agent.</p>
            </div>

            <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 space-y-6">
                <div className="flex items-center space-x-3 mb-4">
                    <div className="w-10 h-10 bg-primary/10 rounded-full flex items-center justify-center text-primary">
                        <Key size={20} />
                    </div>
                    <div>
                        <h3 className="text-lg font-bold text-gray-800">Gemini API Key</h3>
                        <p className="text-sm text-gray-500">Required for "ChatGPT-like" smart responses.</p>
                    </div>
                </div>

                <div className="space-y-4">
                    <div className="bg-blue-50 p-4 rounded-xl border border-blue-100 flex items-start space-x-3">
                        <Shield className="text-blue-600 shrink-0 mt-1" size={18} />
                        <p className="text-sm text-blue-800">
                            Your API Key is stored locally. We use <strong>Gemini 1.5 Flash</strong> for fast and accurate responses.
                            <br />
                            <a href="https://aistudio.google.com/app/apikey" target="_blank" rel="noopener noreferrer" className="underline font-medium hover:text-blue-900">
                                Get a free API Key here
                            </a>
                        </p>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Enter your Google API Key</label>
                        <div className="flex space-x-4">
                            <input
                                type="password"
                                value={apiKey}
                                onChange={(e) => {
                                    setApiKey(e.target.value);
                                    setSaved(false);
                                }}
                                placeholder="AIzaSy..."
                                className="flex-1 p-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary/20 outline-none transition-all"
                            />
                            <button
                                onClick={handleSave}
                                disabled={loading || !apiKey}
                                className={`px-6 py-3 rounded-xl font-medium transition-all flex items-center space-x-2 ${saved
                                        ? 'bg-green-500 text-white'
                                        : 'bg-primary text-white hover:bg-primary/90'
                                    }`}
                            >
                                <Save size={18} />
                                <span>{saved ? 'Saved' : (loading ? 'Saving...' : 'Save Key')}</span>
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 opacity-75">
                <div className="flex items-center space-x-3 mb-4">
                    <div className="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center text-gray-500">
                        <AlertTriangle size={20} />
                    </div>
                    <div>
                        <h3 className="text-lg font-bold text-gray-800">Advanced Configuration</h3>
                        <p className="text-sm text-gray-500">RAG parameters and model selection (Coming Soon)</p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Settings;
