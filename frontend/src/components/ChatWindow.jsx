import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User } from 'lucide-react';
import { api } from '../api/client';
import RAGResults from './RAGResults';

const ChatWindow = () => {
    const [messages, setMessages] = useState([
        { type: 'chat_reply', message: 'Hello! I am your AI News Intelligence Agent. How can I help you today?', sender: 'ai' }
    ]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(scrollToBottom, [messages]);

    const handleSend = async () => {
        if (!input.trim()) return;

        const userMsg = { type: 'chat_reply', message: input, sender: 'user' };
        setMessages(prev => [...prev, userMsg]);
        setInput('');
        setLoading(true);

        try {
            // Determine intent (simple heuristic for demo)
            let response;
            if (input.toLowerCase().includes('news') || input.toLowerCase().includes('search')) {
                response = await api.ragSearch(input);
            } else if (input.toLowerCase().includes('classify')) {
                response = await api.classify(input);
            } else {
                // Default to RAG for generic queries in this demo
                response = await api.ragSearch(input);
            }

            if (response.data.status === 'success' || response.data.status === 'error') {
                // Append all UI blocks from response
                const newBlocks = response.data.ui_blocks.map(block => ({
                    ...block,
                    sender: 'ai'
                }));
                setMessages(prev => [...prev, ...newBlocks]);
            }
        } catch (error) {
            setMessages(prev => [...prev, { type: 'chat_reply', message: 'Error: Could not connect to AI agent.', sender: 'ai' }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-full bg-background">
            <div className="flex-1 overflow-y-auto p-6 space-y-6">
                {messages.map((msg, idx) => (
                    <div key={idx} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`flex max-w-3xl ${msg.sender === 'user' ? 'flex-row-reverse' : 'flex-row'} items-start space-x-3`}>

                            <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${msg.sender === 'user' ? 'bg-gradient-pink ml-3' : 'bg-primary mr-3'
                                }`}>
                                {msg.sender === 'user' ? <User size={16} className="text-white" /> : <Bot size={16} className="text-white" />}
                            </div>

                            <div className={`space-y-2 ${msg.sender === 'user' ? 'items-end' : 'items-start'} flex flex-col`}>
                                {/* Render different block types */}
                                {msg.type === 'chat_reply' && (
                                    <div className={`p-4 rounded-2xl shadow-sm ${msg.sender === 'user'
                                        ? 'bg-white text-gray-800 rounded-tr-none'
                                        : 'bg-white text-gray-800 rounded-tl-none'
                                        }`}>
                                        <p>{msg.message}</p>
                                    </div>
                                )}

                                {msg.type === 'card' && (
                                    <div className="bg-white p-4 rounded-xl shadow-md border border-gray-100 w-full">
                                        <h3 className="font-bold text-primary mb-2">{msg.title}</h3>
                                        <pre className="text-sm bg-gray-50 p-2 rounded overflow-x-auto">
                                            {JSON.stringify(msg.content, null, 2)}
                                        </pre>
                                    </div>
                                )}

                                {msg.type === 'rag_result' && (
                                    <RAGResults data={msg} />
                                )}
                            </div>
                        </div>
                    </div>
                ))}
                {loading && (
                    <div className="flex justify-start">
                        <div className="bg-white p-4 rounded-2xl rounded-tl-none shadow-sm flex items-center space-x-2">
                            <div className="w-2 h-2 bg-primary rounded-full animate-bounce" />
                            <div className="w-2 h-2 bg-primary rounded-full animate-bounce delay-75" />
                            <div className="w-2 h-2 bg-primary rounded-full animate-bounce delay-150" />
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            <div className="p-4 bg-white border-t border-gray-100">
                <div className="flex items-center space-x-4 max-w-4xl mx-auto">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                        placeholder="Ask about news, classify text, or run benchmarks..."
                        className="flex-1 p-4 rounded-xl bg-gray-50 border-none focus:ring-2 focus:ring-primary/20 outline-none transition-all"
                    />
                    <button
                        onClick={handleSend}
                        disabled={loading}
                        className="p-4 bg-primary hover:bg-primary/90 text-white rounded-xl transition-all shadow-lg shadow-primary/30 disabled:opacity-50"
                    >
                        <Send size={20} />
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ChatWindow;
