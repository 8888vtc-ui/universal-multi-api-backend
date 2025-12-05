'use client';

import { ChatMessage } from '@/lib/api';

interface MessageBubbleProps {
    message: ChatMessage;
    isRTL: boolean;
}

export default function MessageBubble({ message, isRTL }: MessageBubbleProps) {
    const isUser = message.role === 'user';

    return (
        <div
            className={`flex ${isUser ? (isRTL ? 'justify-start' : 'justify-end') : (isRTL ? 'justify-end' : 'justify-start')} mb-4`}
        >
            <div
                className={`max-w-[80%] rounded-2xl px-4 py-3 ${isUser
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-100 text-gray-900 dark:bg-gray-800 dark:text-gray-100'
                    }`}
            >
                <p className="text-sm md:text-base whitespace-pre-wrap break-words">
                    {message.content}
                </p>
            </div>
        </div>
    );
}
