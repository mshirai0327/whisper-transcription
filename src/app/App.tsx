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

    const [selectedModel, setSelectedModel] = useState('base');
    const [selectedLanguage, setSelectedLanguage] = useState('ja');

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
            formData.append('model', selectedModel); // 選択されたモデル
            formData.append('language', selectedLanguage); // 選択された言語

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
    }, [selectedFile, selectedModel, selectedLanguage]);

    return (
        <div className="min-h-screen bg-gray-100 py-8 px-4">
            <div className="max-w-4xl mx-auto">
                <header className="mb-8 text-center">
                    <div className="flex items-center justify-center gap-3 mb-2">
                        <AudioLines className="w-10 h-10 text-blue-600" />
                        <h1 className="text-gray-900 font-bold text-3xl">音声文字起こしサービス</h1>
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

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 bg-white p-6 rounded-lg shadow-sm">
                        <div className="space-y-2">
                            <label className="block text-sm font-medium text-gray-700">
                                モデル
                            </label>
                            <select
                                value={selectedModel}
                                onChange={(e) => setSelectedModel(e.target.value)}
                                disabled={isProcessing}
                                className="w-full p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                            >
                                <option value="tiny">Tiny (高速・低精度)</option>
                                <option value="base">Base (標準)</option>
                                <option value="small">Small (高精度)</option>
                                <option value="medium">Medium (より高精度)</option>
                                <option value="large">Large (最高精度・低速)</option>
                            </select>
                        </div>
                        <div className="space-y-2">
                            <label className="block text-sm font-medium text-gray-700">
                                言語
                            </label>
                            <select
                                value={selectedLanguage}
                                onChange={(e) => setSelectedLanguage(e.target.value)}
                                disabled={isProcessing}
                                className="w-full p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                            >
                                <option value="ja">日本語</option>
                                <option value="en">英語</option>
                                <option value="auto">自動検出</option>
                            </select>
                        </div>
                    </div>

                    <div className="flex gap-4">
                        <button
                            onClick={startTranscription}
                            disabled={!selectedFile || isProcessing}
                            className="flex-1 px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-all shadow-md active:scale-[0.98]"
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
                </div>
            </div>
        </div>
    );
}
