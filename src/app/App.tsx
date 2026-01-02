import { useState, useEffect, useCallback } from 'react';
import { FileUploadArea } from './components/FileUploadArea';
import { ProcessingStatus } from './components/ProcessingStatus';
import { TranscriptionResult } from './components/TranscriptionResult';
import { AudioLines } from 'lucide-react';

interface TranscriptionData {
    text: string;
    fileName: string;
    processingTime: number;
}

export default function App() {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [isProcessing, setIsProcessing] = useState(false);
    const [startTime, setStartTime] = useState<Date | null>(null);
    const [transcription, setTranscription] = useState<TranscriptionData | null>(null);

    // リロード防止
    useEffect(() => {
        const handleBeforeUnload = (e: BeforeUnloadEvent) => {
            if (isProcessing) {
                e.preventDefault();
                e.returnValue = '処理中です。ページを離れると処理が中断されます。';
                return e.returnValue;
            }
        };

        window.addEventListener('beforeunload', handleBeforeUnload);
        return () => window.removeEventListener('beforeunload', handleBeforeUnload);
    }, [isProcessing]);

    const handleFileSelect = useCallback((file: File) => {
        setSelectedFile(file);
        setTranscription(null);
    }, []);

    const startTranscription = useCallback(async () => {
        if (!selectedFile) return;

        setIsProcessing(true);
        const now = new Date();
        setStartTime(now);

        try {
            // FormDataを作成してファイルをアップロード
            const formData = new FormData();
            formData.append('file', selectedFile);
            formData.append('model', 'base'); // モデル名を指定
            formData.append('language', 'ja'); // 日本語を指定

            // バックエンドAPIにリクエスト
            const response = await fetch('/api/transcribe', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || '文字起こし処理に失敗しました');
            }

            const result = await response.json();

            setTranscription({
                text: result.text,
                fileName: result.fileName,
                processingTime: result.processingTime,
            });

        } catch (error) {
            console.error('文字起こしエラー:', error);
            alert(`エラーが発生しました: ${error instanceof Error ? error.message : '不明なエラー'}`);
        } finally {
            setIsProcessing(false);
            setStartTime(null);
        }
    }, [selectedFile]);

    return (
        <div className="min-h-screen bg-gray-100 py-8 px-4">
            <div className="max-w-4xl mx-auto">
                <header className="mb-8 text-center">
                    <div className="flex items-center justify-center gap-3 mb-2">
                        <AudioLines className="w-10 h-10 text-blue-600" />
                        <h1 className="text-gray-900">音声文字起こしサービス</h1>
                    </div>
                    <p className="text-gray-600">
                        音声ファイルをアップロードして、自動で文字起こしを行います
                    </p>
                </header>

                <div className="space-y-6">
                    <FileUploadArea
                        onFileSelect={handleFileSelect}
                        selectedFile={selectedFile}
                        disabled={isProcessing}
                    />

                    <div className="flex gap-4">
                        <button
                            onClick={startTranscription}
                            disabled={!selectedFile || isProcessing}
                            className="flex-1 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
                        >
                            {isProcessing ? '処理中...' : '文字起こし開始'}
                        </button>
                    </div>

                    <ProcessingStatus
                        isProcessing={isProcessing}
                        startTime={startTime}
                        estimatedEndTime={null}
                    />

                    {transcription && (
                        <TranscriptionResult
                            text={transcription.text}
                            fileName={transcription.fileName}
                            processingTime={transcription.processingTime}
                        />
                    )}

                    {!isProcessing && !transcription && selectedFile && (
                        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                            <p className="text-yellow-800 text-sm">
                                <strong>注意:</strong> これはデモ版です。実際の音声認識を行うには、外部APIとの連携が必要です。
                            </p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
