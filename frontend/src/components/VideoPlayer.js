import React, { useRef, useEffect, useState } from 'react';
import JSZip from 'jszip';

const VideoPlayer = ({ zipFile }) => {
    const [playing, setPlaying] = useState(false);
    const [currentTime, setCurrentTime] = useState(0);
    const [textData, setTextData] = useState([]);
    const [displayedText, setDisplayedText] = useState([]);
    const videoRef = useRef();
    const textContainerRef = useRef();
    const progressBarRef = useRef();

    const handlePlay = () => {
        if (videoRef.current.paused || videoRef.current.ended) {
            videoRef.current.play().catch((error) => console.error(error));
        } else {
            videoRef.current.pause();
        }
    };

    const handleTimeUpdate = () => {
        setCurrentTime(videoRef.current.currentTime);

        const newDisplayedText = textData.filter(
            (item) => item.timestamp <= currentTime
        );

        newDisplayedText.sort((a, b) => b.timestamp - a.timestamp);

        setDisplayedText(newDisplayedText);

        textContainerRef.current.scrollTop = textContainerRef.current.scrollHeight;

        const progress = (currentTime / videoRef.current.duration) * 100;
        progressBarRef.current.value = progress;
    };

    const handleProgressBarChange = (e) => {
        const progressValue = e.target.value;
        const newTime = (progressValue / 100) * videoRef.current.duration;
        setCurrentTime(newTime);
        videoRef.current.currentTime = newTime;
    };

    const handleVideoEnded = () => {
        setPlaying(false);
        setCurrentTime(0);
        progressBarRef.current.value = 0;
    };

    useEffect(() => {
        const processZipFile = async () => {
            try {
                const zip = new JSZip();
                const zipData = await zip.loadAsync(zipFile);

                const mp4File = await zipData.file('video.mp4').async('blob');
                const csvFile = await zipData.file('data.csv').async('text');

                const lines = csvFile.split('\n');
                const data = lines.map((line) => {
                    const [timestamp, text] = line.split(',');
                    return { timestamp: parseFloat(timestamp), text };
                });

                setTextData(data);
                setDisplayedText([]);
                videoRef.current.src = URL.createObjectURL(mp4File);

                videoRef.current.addEventListener('loadedmetadata', () => {
                    if (playing) {
                        videoRef.current.play().catch((error) => console.error(error));
                    }
                });

                videoRef.current.addEventListener('play', () => {
                    setPlaying(true);
                });

                videoRef.current.addEventListener('pause', () => {
                    setPlaying(false);
                });

                videoRef.current.addEventListener('ended', handleVideoEnded);

                videoRef.current.play().catch((error) => console.error(error));
            } catch (error) {
                console.error('Error processing zip file:', error);
            }
        };

        if (zipFile) {
            processZipFile();
        }
    }, [zipFile]);

    return (
        <>
            <video
                ref={videoRef}
                onTimeUpdate={handleTimeUpdate}
                onEnded={handleVideoEnded}
                className="w-full border-2 border-gray-300"
            />
            <div className="flex items-center mt-4">
                <button
                    onClick={handlePlay}
                    className="bg-blue-500 text-white p-2 rounded-md cursor-pointer hover:bg-blue-600"
                >
                    {playing ? 'Pause' : 'Play'}
                </button>
                <div className="flex-grow ml-4">
                    <input
                        type="range"
                        min="0"
                        max="100"
                        step="0.01"
                        onChange={handleProgressBarChange}
                        ref={progressBarRef}
                        className="w-full"
                    />
                </div>
                <div className="ml-4">{currentTime.toFixed(2)}</div>
            </div>
            <div ref={textContainerRef} className="mt-4 overflow-y-scroll max-h-200 border-2 border-gray-300 p-4 rounded-md">
                {displayedText.map((item, index) => (
                    <div
                        key={index}
                        className={`mb-1 p-1 rounded-md ${
                            item.timestamp <= currentTime ? 'bg-gray-100' : ''
                        }`}
                    >
                        {`${item.timestamp.toFixed(2)}: ${item.text}`}
                    </div>
                ))}
            </div>
        </>
    );
};

export default VideoPlayer;
