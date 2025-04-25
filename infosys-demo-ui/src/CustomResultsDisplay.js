import React, { useEffect, useState } from 'react';
import { useSearch } from "@elastic/react-search-ui"; 
import apm from './Apm'; 

function CustomResultsDisplay() {
  const { results, wasSearched, searchTerm, isLoading, error } = useSearch();

  // State to track the last search term logged to APM
  // Prevents logging the same search multiple times on re-renders
  const [lastTrackedSearchTerm, setLastTrackedSearchTerm] = useState('');

  useEffect(() => {
    // Check if:
    // 1. A search was actually performed (wasSearched is true)
    // 2. There is a search term
    // 3. The current search term is different from the last one we tracked
    if (wasSearched && searchTerm && searchTerm !== lastTrackedSearchTerm) {
      // It's generally safe to call apm methods after init.
      // The agent handles queueing if not immediately ready.
      console.log(`RUM: Tracking search for term: "${searchTerm}"`);

      // Add custom labels to the *current active transaction*
      apm.addLabels({
        'search_term': searchTerm,
        'search_result_count': results.length, // Log how many results were found
        'search_action': 'submit' // Indicate this was a user-triggered search
      });

      // Update the state to remember this term was tracked
      setLastTrackedSearchTerm(searchTerm);
    }
    // Dependencies: run when search term, search status, or results change
  }, [searchTerm, wasSearched, results, lastTrackedSearchTerm]);


  if (isLoading) {
    return <div className="loading-indicator">Loading results...</div>;
  }

  if (error) {
    return <div className="error-message">Error fetching results: {error}</div>;
  }

  if (!wasSearched && results.length === 0) {
    return <div className="placeholder-item">Enter a query in the search box above to see results.</div>;
  }

  if (wasSearched && results.length === 0) {
    return <div className="placeholder-item">No results found for "{searchTerm}". Try a different query.</div>;
  }

  return (
    <div className="document-list">
      {results.map((result) => (
        <div key={result._meta?.id || JSON.stringify(result)} className="document-item">
          {/* Title */}
          {result.title?.raw && (
            <h3 className="result-title">
              {result.url?.raw ? (
                <a href={result.url.raw} target="_blank" rel="noopener noreferrer">
                  {/* Display snippet if available, fallback to raw title */}
                  {/* Use dangerouslySetInnerHTML for snippets as they contain <em> tags */}
                  <span dangerouslySetInnerHTML={{ __html: result.title.snippet || result.title.raw }} />
                </a>
              ) : (
                // Display title without link if no URL
                 <span dangerouslySetInnerHTML={{ __html: result.title.snippet || result.title.raw }} />
              )}
            </h3>
          )}

          {/* Snippet (Show body snippet only if title snippet wasn't displayed or doesn't exist) */}
          {result.body_content?.snippet && !(result.title?.snippet) && (
             <p
              className="snippet" // Use your CSS class for snippets
              dangerouslySetInnerHTML={{ __html: result.body_content.snippet }}
            />
          )}

          {/* URL (Show separately only if it wasn't used in the title link) */}
           {result.url?.raw && !result.title?.raw && (
             <p><a href={result.url.raw} target="_blank" rel="noopener noreferrer">{result.url.raw}</a></p>
          )}

          {/* You could add other fields here, e.g., */}
          {/* result.timestamp?.raw && <p className="timestamp">{new Date(result.timestamp.raw).toLocaleDateString()}</p> */}
        </div>
      ))}
    </div>
  );
}

export default CustomResultsDisplay;