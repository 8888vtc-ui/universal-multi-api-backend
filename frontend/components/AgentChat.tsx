
import React, { useState } from 'react';
import { Button } from './ui/Button';
import { Input } from './ui/Input';
import { Card, CardBody } from './ui/Card';

interface Step {
    type: 'thought' | 'action' | 'observation';
    content: string;
}

export const AgentChat: React.FC = () => {
    const [query, setQuery] = useState('');
    const [response, setResponse] = useState<string | null>(null);
    const [steps, setSteps] = useState<Step[]>([]);
    const [isLoading, setIsLoading] = useState(false);

    const handleSearch = async () => {
        if (!query.trim()) return;

        setIsLoading(true);
        setSteps([]);
        setResponse(null);

        try {
            const apiUrl = process.env.NEXT_PUBLIC_API_URL || '';
            const res = await fetch(`${apiUrl}/api/agent/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token') || ''}`
                },
                body: JSON.stringify({
                    message: query,
                    provider: 'groq'
                })
            });

            const data = await res.json();

            if (res.ok) {
                setResponse(data.response);
                // Simulate steps for demo (since backend doesn't stream yet)
                setSteps([
                    { type: 'thought', content: "User asked: " + query },
                    { type: 'thought', content: "Searching for relevant information..." },
                    { type: 'action', content: "Calling Search Tool" },
                    { type: 'observation', content: "Found 3 results" },
                    { type: 'thought', content: "Synthesizing answer..." }
                ]);
            } else {
                setResponse(`Error: ${data.detail}`);
            }
        } catch (err) {
            setResponse('Failed to contact agent.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="max-w-2xl mx-auto p-4 space-y-6">
            <Card>
                <CardBody className="space-y-4">
                    <h2 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                        🧠 Autonomous Agent
                    </h2>
                    <p className="text-gray-600">
                        Ask me anything. I can browse the web, remember facts, and reason.
                    </p>

                    <div className="flex gap-2">
                        <Input
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                            placeholder="e.g., What is the Bitcoin price and is it sunny in New York?"
                            onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                        />
                        <Button onClick={handleSearch} isLoading={isLoading}>
                            Think & Act
                        </Button>
                    </div>
                </CardBody>
            </Card>

            {/* Thinking Process */}
            {isLoading && (
                <div className="space-y-2 animate-pulse">
                    <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                    <div className="h-4 bg-gray-200 rounded w-1/2"></div>
                </div>
            )}

            {/* Results */}
            {(response || steps.length > 0) && (
                <Card className="border-t-4 border-t-purple-500">
                    <CardBody className="space-y-4">

                        {/* Steps Visualization */}
                        <div className="bg-gray-50 rounded-lg p-4 text-sm space-y-2 font-mono border border-gray-100">
                            <div className="text-xs text-gray-400 uppercase tracking-widest mb-2">Thinking Process</div>
                            {steps.map((step, i) => (
                                <div key={i} className={`
                        pl-3 border-l-2 
                        ${step.type === 'thought' ? 'border-blue-400 text-gray-600' :
                                        step.type === 'action' ? 'border-orange-400 text-orange-700' :
                                            'border-green-400 text-green-700'}
                    `}>
                                    <span className="font-bold uppercase text-[10px] mr-2 opactiy-50">{step.type}</span>
                                    {step.content}
                                </div>
                            ))}
                        </div>

                        {/* Final Answer */}
                        {response && (
                            <div className="mt-4 pt-4 border-t border-gray-100">
                                <div className="font-bold text-gray-900 mb-2">Final Answer:</div>
                                <div className="text-gray-800 leading-relaxed whitespace-pre-wrap">{response}</div>
                            </div>
                        )}
                    </CardBody>
                </Card>
            )}
        </div>
    );
};

