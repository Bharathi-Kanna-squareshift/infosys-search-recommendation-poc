// src/RecommendationsDisplay.js
import React, { useState, useEffect } from 'react';
import useUserId from './useUserId'; // Import the hook to get the user ID

// --- Helper function to fetch recommendations ---
async function fetchRecommendations(userId, setRecommendations, setLoading, setError) {
    if (!userId) {
        console.log("Recommendations fetch skipped: No userId yet.");
        return; // Don't fetch if userId isn't available yet
    }

    setLoading(true);
    setError(null);
    console.log(`Attempting to fetch recommendations for user: ${userId}`); // Log attempt
    try {
        // Construct the correct API endpoint URL
        const apiUrl = `http://localhost:8000/api/recommendations/${userId}`;
        console.log(`Fetching recommendations from: ${apiUrl}`); // Log the URL

        const response = await fetch(apiUrl);

        if (!response.ok) {
            // Try to get error details from the response body
            let errorDetail = `HTTP error! Status: ${response.status}`;
            try {
                const errorData = await response.json();
                if (errorData.detail) {
                    errorDetail = `Error: ${errorData.detail}`;
                }
                console.error("API Error Response Body:", errorData); // Log error body
            } catch (e) {
                // Ignore if parsing error body fails, log the original text
                const textResponse = await response.text();
                 console.error("API Error Response Text:", textResponse);
            }
            throw new Error(errorDetail);
        }

        // --- RESPONSE PARSING MODIFICATION ---
        const rawData = await response.json();
        console.log("Received RAW recommendations data:", rawData); // Log the raw data

        // Safely extract the array of actual result documents ('hits')
        const hits = rawData?.hits?.hits || [];
        console.log(`Extracted ${hits.length} hits from raw data.`);

        // Map the raw Elasticsearch hits to the simplified format needed for display
        const simplifiedRecs = hits.map(hit => {
            // Safely access the title text, handling potential variations
            let titleText = null;
            const titleSource = hit?._source?.title;
            if (typeof titleSource === 'object' && titleSource !== null && titleSource.text) {
                titleText = titleSource.text;
            } else if (typeof titleSource === 'string') { // Handle if title is just a string in _source
                titleText = titleSource;
            }

            return {
                id: hit?._id,          // Get the document ID
                title: titleText,     // Get the extracted title text
                url: hit?._source?.url, // Get the URL from _source
                score: hit?._score      // Get the relevance score
            };
        }).filter(rec => rec.id); // Filter out any potential null/undefined entries if ID parsing failed

        console.log("Processed simplified recommendations:", simplifiedRecs);
        setRecommendations(simplifiedRecs); // Set the processed, simplified array to state

    } catch (error) {
        console.error("Failed to fetch or process recommendations:", error);
        setError(error.message || "Could not fetch or process recommendations.");
        setRecommendations([]); // Clear recommendations on error
    } finally {
        setLoading(false);
    }
}


function RecommendationsDisplay() {
    const userId = useUserId(); // Get the user ID
    const [recommendations, setRecommendations] = useState([]);
    const [isLoading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    // --- Effect to fetch recommendations when userId changes ---
    useEffect(() => {
        fetchRecommendations(userId, setRecommendations, setLoading, setError);
        // Dependency array: re-run effect if userId changes
    }, [userId]);

    // --- Log state for debugging before render ---
    // console.log("Rendering RecommendationsDisplay - State:", { userId, isLoading, error, recommendations });

    // --- Render Logic ---
    // The JSX part doesn't need to change because we are transforming
    // the fetched data into the format the JSX expects before setting the state.

    return (
        <div className="document-list">
            {isLoading && <div className="loading-indicator">Loading recommendations...</div>}

            {error && <div className="error-message">{error}</div>}

            {/* This condition now works correctly because 'recommendations' state IS an array */}
            {!isLoading && !error && recommendations.length === 0 && (
                <div className="placeholder-item">No recommendations available.</div>
            )}

            {!isLoading && !error && recommendations.length > 0 && (
                recommendations.map((rec) => (
                    // Use the unique 'id' from the processed data for the key
                    <div key={rec.id} className="document-item">
                        {/* Title - Make it a link if URL exists */}
                        {rec.title && (
                            <h3 className="result-title">
                                {rec.url ? (
                                    <a href={rec.url} target="_blank" rel="noopener noreferrer">
                                        {rec.title} {/* Display plain title text */}
                                    </a>
                                ) : (
                                    <span>{rec.title}</span> /* Display title without link */
                                )}
                            </h3>
                        )}
                        {/* Optionally display the score */}
                        {/* rec.score != null && <p style={{ fontSize: '0.8em', color: 'grey' }}>Score: {rec.score.toFixed(2)}</p> */}
                    </div>
                ))
            )}
        </div>
    );
}

export default RecommendationsDisplay;