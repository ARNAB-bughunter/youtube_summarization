import React, { useState, useEffect } from 'react';

const formStyle = {
    background: "white",
    padding: "20px",
    borderRadius: "8px",
    boxShadow: "0 0 10px rgba(0, 0, 0, 0.1)",
    width: "300px",
    margin: "auto"
};

const inputContainer = {
    position: "relative",
    marginBottom: "20px"
};

const inputStyle = {
    width: "calc(100% - 20px)",
    padding: "10px",
    border: "1px solid #ccc",
    borderRadius: "4px",
    outline: "none",
    fontSize: "16px",
    display: "block",
    background: "white"
};

const labelStyle = {
    position: "absolute",
    top: "50%",
    left: "10px",
    transform: "translateY(-50%)",
    background: "white",
    padding: "0 5px",
    color: "#888",
    fontSize: "16px",
    transition: "0.3s ease-in-out"
};

const labelFocused = {
    top: "0",
    fontSize: "12px",
    color: "#28a745"
};

const buttonStyle = {
    backgroundColor: "#28a745",
    color: "white",
    border: "none",
    padding: "10px",
    cursor: "pointer",
    width: "100%",
    fontSize: "16px",
    borderRadius: "4px"
};

const progressContainer = {
    width: "100%",
    background: "#e0e0e0",
    borderRadius: "4px",
    marginTop: "10px",
    height: "20px"
};

const progressBar = (progress) => ({
    width: `${progress}%`,
    height: "100%",
    background: "#28a745",
    borderRadius: "4px",
    transition: "width 0.3s ease-in-out"
});

const UrlForm = () => {
    const [isFocused, setIsFocused] = useState(false);
    const [value, setValue] = useState("");
    const [loading, setLoading] = useState(false);
    const [summary, setSummary] = useState("");
    const [progress, setProgress] = useState(0);
    const [taskId, setTaskId] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!value.trim()) {
            alert("Please enter a YouTube URL");
            return;
        }

        setLoading(true);
        setSummary("");
        setProgress(0);

        try {
            const encodedUrl = encodeURIComponent(value);
            const apiUrl = `http://0.0.0.0:8000/process/?youtube_url=${encodedUrl}`;

            const response = await fetch(apiUrl, {
                method: "POST",
                headers: {
                    "Accept": "application/json"
                }
            });

            console.log('response', response);

            if (!response.ok) {
                throw new Error("Failed to process video");
            }

            const data = await response.json();

            
            if (data.video_id) {
                setTaskId(data.video_id);
                listenForProgress(data.video_id); // Start WebSocket for progress updates
            }
        } catch (error) {
            console.log('error', error);
            alert(error.message);
            setLoading(false);
        }
    };

    const listenForProgress = (taskId) => {
        const ws = new WebSocket(`ws://localhost:8000/ws/status/${taskId}`);
        console.log("WebSocket created");
        

        ws.onmessage = (event) => {
            const data = event.data;
            let pogress = +data
            console.log("WebSocket message:", pogress);
            setProgress(data);

            if (pogress === 100) {
                ws.close();
                setSummary(data.summary || "Summary is ready.");
                setLoading(false);
            }
        };

        ws.onerror = (error) => {
            console.error("WebSocket Error:", error);
            ws.close();
            setLoading(false);
        };

        ws.onclose = () => {
            console.log("WebSocket closed");
        };
    };

    return (
        <>
            <div>
                <h1>YouTube Video Summary</h1>
            </div>
            <div>
                <form style={formStyle} onSubmit={handleSubmit}>
                    <div style={inputContainer}>
                        <label
                            htmlFor="url"
                            style={isFocused || value ? { ...labelStyle, ...labelFocused } : labelStyle}
                        >
                            YouTube Video URL
                        </label>
                        <input
                            type="text"
                            id="url"
                            name="url"
                            style={inputStyle}
                            required
                            value={value}
                            onFocus={() => setIsFocused(true)}
                            onBlur={() => setIsFocused(false)}
                            onChange={(e) => setValue(e.target.value)}
                        />
                    </div>
                    <button type="submit" style={buttonStyle} disabled={loading}>
                        {loading ? "Processing..." : "Summarize"}
                    </button>
                    {loading && (
                        <div style={progressContainer}>
                            <div style={progressBar(progress)}></div>
                        </div>
                    )}
                    {summary && (
                        <div style={{ marginTop: "20px", padding: "10px", background: "#f8f9fa", borderRadius: "4px" }}>
                            <h3>Summary:</h3>
                            <p>{summary}</p>
                        </div>
                    )}
                </form>
            </div>
        </>
    );
};

export default UrlForm;
