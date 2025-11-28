import React from 'react';
import ChatWindow from '../components/ChatWindow';

const Chat = () => {
    return (
        <div className="h-screen flex flex-col">
            <div className="p-6 border-b border-gray-100 bg-white">
                <h1 className="text-2xl font-bold text-gray-800">AI Chat Agent</h1>
                <p className="text-gray-500 text-sm">Ask questions, classify text, or run analysis</p>
            </div>
            <div className="flex-1 overflow-hidden">
                <ChatWindow />
            </div>
        </div>
    );
};

export default Chat;
