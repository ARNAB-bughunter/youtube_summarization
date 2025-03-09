import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown'

const formStyle = {
    background: "white",
    padding: "20px",
    borderRadius: "8px",
    boxShadow: "0 0 10px rgba(126, 245, 66, 1)",
    margin: "10px",
    minWidth: "300px",
};



const summaryStyle = {
    background: "white",
    padding: "20px",
    borderRadius: "8px",
    boxShadow: "0 0 10px rgba(126, 245, 66, 1)",
    margin: "10px",
};




const inputContainer = {
    position: "relative",
    marginBottom: "10px"
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

const buttonStyleNormal = {
    backgroundColor: "#28a745",
    color: "white",
    border: "none",
    padding: "10px",
    cursor: "pointer",
    width: "100%",
    fontSize: "16px",
    borderRadius: "4px"
};

const copyButtonStyle = {
    backgroundColor: "#28a745",
    color: "white",
    border: "none",
    padding: "10px",
    cursor: "pointer",
    fontSize: "10px",
    borderRadius: "4px"
};

const buttonStyleDisable = {
    backgroundColor: "#505050",
    color: "white",
    border: "none",
    padding: "10px",
    cursor: "not-allowed",
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


const textareaStyle = {
    width: "100%",
    borderRadius: "4px",
    marginTop: "10px",
    resize: "none",
    maxWidth: "300px"
}

const textareaStyleURL = {
    width: "100%",
    background: "#e0e0e0",
    borderRadius: "4px",
    marginTop: "10px",
    height: "20px", // Increase height for better visibility
    resize: "none",
    whiteSpace: "nowrap", // Prevents wrapping
    overflow: "hidden", // Hides overflow text
    textOverflow: "ellipsis" // Adds "..." if text overflows
};

const progressBar = (progress) => ({
    width: `${progress}%`,
    height: "100%",
    background: "repeating-linear-gradient(-45deg, #4CAF50, #4CAF50 10px, #66BB6A 10px, #66BB6A 20px)",
    borderRadius: "4px",
    transition: "width 0.3s ease-in-out",
    animation: "moveStripe 1s linear infinite"
});



const UrlForm = () => {
    const [isFocused, setIsFocused] = useState(false);
    const [value, setValue] = useState("");
    const [loading, setLoading] = useState(false);
    const [summary, setSummary] = useState("");
    const [progress, setProgress] = useState(0);
    const [thumbnailURL, setThumbnailURL] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!value.trim()) {
            alert("Please enter a YouTube URL");
            return;
        }

        setLoading(true);
        setSummary("");
        setProgress(0);
        setThumbnailURL("");

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
            try {
                const data = JSON.parse(event.data); // Parse JSON string into an object

                console.log('data', data);

                let progress = Number(data.progress); // Convert progress to a number
                console.log("WebSocket message:", progress);

                setProgress(progress);

                if (data.thumbnail_url) {
                    setThumbnailURL(data.thumbnail_url);
                }

                if (progress === 100) {
                    ws.close();
                    setSummary(data.summary || "Summary is ready.");
                    setLoading(false);
                }
            } catch (error) {
                console.error("Error parsing WebSocket message:", error);
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


    const handleCopy = () => {
        navigator.clipboard.writeText(summary)
            .then(() => alert("Summary Copied to clipboard!"))
            .catch(err => console.error("Failed to copy:", err));
    };

    return (
        <>
            <div>
                <h1 style={{color:"#42f5cb",}}>YouTube Video Summarizer</h1>
            </div>
            <div style={formStyle}>
                <form onSubmit={handleSubmit}>
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
                    <button type="submit" style={loading ? buttonStyleDisable : buttonStyleNormal} disabled={loading}>
                        {loading ? "Processing..." : "Summarize"}
                    </button>
                </form>
                {loading && (
                    <>
                        <p>Please wait a moment...</p>
                        <div style={progressContainer}>
                            <div style={progressBar(progress)}></div>
                        </div>
                    </>
                )}
            </div>
                {summary && (
                <>
                <div style={summaryStyle}>
                    <div style={{ padding: "10px", background: "#f8f9fa", borderRadius: "4px" }}>
                        
                        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", width: "100%" }}>
                            <p style={{fontWeight:"bold"}}>Key Points</p>
                            <button style={ copyButtonStyle } onClick={handleCopy}> 
                                COPY
                            </button>
                        </div>                       
                        
                            <div style={textareaStyle}>
                                <ReactMarkdown>{summary}</ReactMarkdown>
                            </div>
                    </div>
                
                </div>
                <div>{thumbnailURL && <div style={summaryStyle} dangerouslySetInnerHTML={{ __html: thumbnailURL }} />}</div>
                </>
                )}
            

            {/* <div dangerouslySetInnerHTML={{ __html: youtubevideo }} /> */}
        </>
    );
};

export default UrlForm;
