import React, { useState, useCallback, useRef, useEffect } from 'react';
import { GoogleGenAI, LiveServerMessage, Modality } from '@google/genai';
import { SessionStatus, type TranscriptionEntry } from '../types/live';
import { encode, decode, decodeAudioData } from '../services/audioUtils';
import Visualizer from './Visualizer';
import TranscriptionList from './TranscriptionList';

// Use environment variable for API key
const API_KEY = import.meta.env.VITE_GEMINI_API_KEY || '';
if (!API_KEY) {
  console.warn("Gemini API Key is missing. Please set VITE_GEMINI_API_KEY in your .env file.");
}

const MODEL_NAME = 'gemini-2.5-flash-native-audio-preview-12-2025';

const LiveAudioSession: React.FC = () => {
  const [status, setStatus] = useState<SessionStatus>(SessionStatus.IDLE);
  const [transcriptions, setTranscriptions] = useState<TranscriptionEntry[]>([]);
  const [isModelTalking, setIsModelTalking] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // References for non-state audio processing
  const audioContexts = useRef<{
    input: AudioContext;
    output: AudioContext;
  } | null>(null);
  const audioSources = useRef<Set<AudioBufferSourceNode>>(new Set());
  const nextStartTime = useRef<number>(0);
  const sessionRef = useRef<any>(null);
  const micStream = useRef<MediaStream | null>(null);
  const transcriptionRef = useRef({ user: '', model: '' });

  const stopSession = useCallback(() => {
    if (sessionRef.current) {
      try { sessionRef.current.close(); } catch(e) {}
      sessionRef.current = null;
    }
    if (micStream.current) {
      micStream.current.getTracks().forEach(track => track.stop());
      micStream.current = null;
    }
    audioSources.current.forEach(source => {
      try { source.stop(); } catch(e) {}
    });
    audioSources.current.clear();
    setStatus(SessionStatus.IDLE);
    setIsModelTalking(false);
  }, []);

  const startSession = async () => {
    try {
      setStatus(SessionStatus.CONNECTING);
      setError(null);
      
      const ai = new GoogleGenAI({ apiKey: API_KEY });

      // Initialize Audio Contexts
      if (!audioContexts.current) {
        audioContexts.current = {
          input: new (window.AudioContext || (window as any).webkitAudioContext)({ sampleRate: 16000 }),
          output: new (window.AudioContext || (window as any).webkitAudioContext)({ sampleRate: 24000 })
        };
      }

      const { input: inputCtx, output: outputCtx } = audioContexts.current;

      // Request microphone
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      micStream.current = stream;

      const sessionPromise = ai.live.connect({
        model: MODEL_NAME,
        config: {
          responseModalities: [Modality.AUDIO],
          speechConfig: {
            voiceConfig: { prebuiltVoiceConfig: { voiceName: 'Puck' } },
          },
          systemInstruction: 'You are the Spatial Engine AI, an expert in spatial analysis, lighting optimization, and energy efficiency. You are NOT Gemini; you are a specialized expert system for the Spatial Engine platform. Respond briefly, naturally, and professionally. Focus on helping the user with spatial auditing, lux calculations, and energy reports.',
        },
        callbacks: {
          onopen: () => {
            setStatus(SessionStatus.ACTIVE);
            
            // Set up mic streaming to API
            const source = inputCtx.createMediaStreamSource(stream);
            const scriptProcessor = inputCtx.createScriptProcessor(4096, 1, 1);
            
            scriptProcessor.onaudioprocess = (e) => {
              const inputData = e.inputBuffer.getChannelData(0);
              const l = inputData.length;
              const int16 = new Int16Array(l);
              for (let i = 0; i < l; i++) {
                int16[i] = inputData[i] * 32768;
              }
              const pcmBlob = {
                data: encode(new Uint8Array(int16.buffer)),
                mimeType: 'audio/pcm;rate=16000',
              };

              sessionPromise.then((session) => {
                if (sessionRef.current) {
                  session.sendRealtimeInput({ media: pcmBlob });
                }
              });
            };

            source.connect(scriptProcessor);
            scriptProcessor.connect(inputCtx.destination);
          },
          onmessage: async (message: LiveServerMessage) => {
            // Handle Transcriptions
            if (message.serverContent?.inputTranscription) {
              const text = message.serverContent.inputTranscription.text;
              transcriptionRef.current.user += text;
            } else if (message.serverContent?.outputTranscription) {
              const text = message.serverContent.outputTranscription.text;
              transcriptionRef.current.model += text;
            }

            if (message.serverContent?.turnComplete) {
              const userText = transcriptionRef.current.user.trim();
              const modelText = transcriptionRef.current.model.trim();
              
              if (userText || modelText) {
                setTranscriptions(prev => [
                  ...prev,
                  ...(userText ? [{ id: Date.now() + '-u', role: 'user' as const, text: userText, timestamp: Date.now() }] : []),
                  ...(modelText ? [{ id: Date.now() + '-m', role: 'model' as const, text: modelText, timestamp: Date.now() }] : [])
                ]);
              }
              transcriptionRef.current = { user: '', model: '' };
            }

            // Handle Audio Output
            const base64Audio = message.serverContent?.modelTurn?.parts?.[0]?.inlineData?.data;
            if (base64Audio) {
              setIsModelTalking(true);
              nextStartTime.current = Math.max(nextStartTime.current, outputCtx.currentTime);
              
              const audioBuffer = await decodeAudioData(
                decode(base64Audio),
                outputCtx,
                24000,
                1
              );
              
              const source = outputCtx.createBufferSource();
              source.buffer = audioBuffer;
              const gainNode = outputCtx.createGain();
              source.connect(gainNode).connect(outputCtx.destination);
              
              source.addEventListener('ended', () => {
                audioSources.current?.delete(source);
                if (audioSources.current?.size === 0) {
                  setIsModelTalking(false);
                }
              });

              source.start(nextStartTime.current);
              nextStartTime.current += audioBuffer.duration;
              audioSources.current.add(source);
            }

            const interrupted = message.serverContent?.interrupted;
            if (interrupted) {
              audioSources.current.forEach(src => {
                try { src.stop(); } catch(e) {}
              });
              audioSources.current.clear();
              nextStartTime.current = 0;
              setIsModelTalking(false);
            }
          },
          onerror: (e) => {
            console.error('Gemini Live Error:', e);
            setError('An error occurred while connecting to the API.');
            stopSession();
          },
          onclose: () => {
            console.log('Session closed');
            stopSession();
          },
        }
      });

      const session = await sessionPromise;
      sessionRef.current = session;

    } catch (err: any) {
      console.error('Startup error:', err);
      setError(err.message || 'Failed to access microphone or connect to API.');
      setStatus(SessionStatus.IDLE);
    }
  };

  useEffect(() => {
    return () => {
      stopSession();
    };
  }, [stopSession]);

  return (
    <div className="flex flex-col h-full w-full">
        {/* Header/Status */}
        <div className="flex justify-between items-center bg-black/20 p-4 rounded-lg border border-white/5 mb-4">
             <div className="flex items-center gap-3">
                <div className={`w-2 h-2 rounded-full ${status === SessionStatus.ACTIVE ? 'bg-green-500 animate-pulse' : 'bg-red-500/50'}`}></div>
                <span className="text-[10px] uppercase tracking-widest text-slate-400 font-semibold">
                {status === SessionStatus.ACTIVE ? 'Online' : status === SessionStatus.CONNECTING ? 'Connecting' : 'Offline'}
                </span>
            </div>
            {error && (
                <div className="text-red-400 text-xs text-center animate-fade-in">
                    {error}
                </div>
            )}
             <p className="text-[10px] text-slate-600 uppercase tracking-widest font-medium">
               Model: {MODEL_NAME}
             </p>
        </div>

        {/* Interaction Area */}
        <div className="flex flex-col md:flex-row flex-1 gap-4 min-h-0 overflow-hidden">
          {/* Visual Side */}
          <div className="flex flex-col items-center justify-center w-full md:w-1/2 lg:w-1/3 bg-black/20 rounded-xl border border-white/5 p-4 relative overflow-hidden">
            <Visualizer 
              isActive={status === SessionStatus.ACTIVE} 
              isModelTalking={isModelTalking} 
            />
            
            <div className="text-center mt-6 z-10">
              <p className={`text-sm transition-colors ${status === SessionStatus.ACTIVE ? 'text-slate-300' : 'text-slate-500'}`}>
                {status === SessionStatus.ACTIVE 
                  ? (isModelTalking ? 'Gemini is speaking...' : 'Listening...') 
                  : 'Press the button below to start'}
              </p>
            </div>
          </div>

          {/* Transcription Side */}
          <div className="flex-1 bg-black/20 rounded-xl border border-white/5 flex flex-col relative overflow-hidden h-full">
            <div className="px-4 py-2 border-b border-white/5 text-[10px] text-slate-500 uppercase tracking-wider font-bold bg-white/5">
              Transcription (Beta)
            </div>
            <TranscriptionList entries={transcriptions} />
          </div>
        </div>

        {/* Footer / Controls */}
        <div className="mt-4 flex justify-center">
            {status === SessionStatus.IDLE || status === SessionStatus.ERROR ? (
              <button
                onClick={startSession}
                className="group relative px-8 py-3 bg-accent-primary hover:bg-accent-secondary text-white rounded-full font-bold transition-all transform hover:scale-105 active:scale-95 shadow-lg shadow-accent-primary/20"
              >
                <div className="flex items-center gap-2">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                  <span>Connect Gemini Live</span>
                </div>
              </button>
            ) : status === SessionStatus.CONNECTING ? (
              <button disabled className="px-8 py-3 bg-slate-800 text-slate-500 rounded-full font-bold flex items-center gap-3 cursor-not-allowed">
                <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span>Connecting...</span>
              </button>
            ) : (
              <button
                onClick={stopSession}
                className="px-8 py-3 bg-red-500/10 hover:bg-red-500/20 border border-red-500/30 text-red-500 rounded-full font-bold transition-all transform hover:scale-105 active:scale-95 flex items-center gap-2"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
                <span>End Session</span>
              </button>
            )}
        </div>
    </div>
  );
};

export default LiveAudioSession;
