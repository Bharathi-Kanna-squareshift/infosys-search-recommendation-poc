import React, { useEffect } from 'react'; 
import {
  SearchProvider,
  SearchBox,
  ErrorBoundary
  
} from "@elastic/react-search-ui";
import FastAPIConnector from './FastAPIConnector';
import CustomResultsDisplay from './CustomResultsDisplay'; 
import RecommendationsDisplay from './RecommendationsDisplay'; 

import "@elastic/react-search-ui-views/lib/styles/styles.css"; 
import './App.css'; 

import useUserId from './useUserId';
import apm from './Apm'; 

const connector = new FastAPIConnector('http://localhost:8000/api/search');


const config = {
  apiConnector: connector,
  alwaysSearchOnInitialLoad: false, 
  searchQuery: {
    resultsPerPage: 20,
    result_fields: {
      title: { raw: {}, snippet: { size: 150, fallback: true } }, 
      url: { raw: {} }, 
      body_content: { snippet: { size: 200, fallback: true } }, 
      
    },
    
    search_fields: {
      title: { weight: 3 }, 
      body_content: { weight: 1 },
      
    },
  },
  
  autocompleteQuery: {
    results: {
      resultsPerPage: 5, 
      result_fields: {
        
        title: { snippet: { size: 100, fallback: true } }
      },
      search_fields: {
         
        title: {},
        body_content: {}
      }
    }
  }
};

function App() {
  const userId = useUserId();

  useEffect(() => {
    if (userId) {
      console.log(`Setting APM user context with ID: ${userId}`);
      apm.setUserContext({ id: userId });
    }
  }, [userId]);


  return (
    <SearchProvider config={config}>
      {/* Catches errors within the Search UI context */}
      <ErrorBoundary>
        {/* Main container from your App.css */}
        <div className="app-container">
          {/* Header section */}
          <header className="app-header">
            <h1>Infosys Demo</h1>
            {/* Optional: Display userId for debugging */}
            {/* {userId && <p style={{fontSize: '0.8em', color: 'grey'}}>User: {userId}</p>} */}
          </header>

          {/* Search input section */}
          <section className="search-section">
            {/* The SearchBox component uses the SearchProvider context */}
            <SearchBox
              autocompleteSuggestions={true}
            />
          </section>

          {/* Main content area holding results and recommendations */}
          <main className="content-area">
            {/* Section for displaying search results */}
            <section className="results-section" aria-labelledby="results-heading">
              <h2 id="results-heading">Search Results</h2>
              {/* This component uses the SearchProvider context */}
              <CustomResultsDisplay />
            </section>

            {/* Section for displaying recommendations */}
            <aside className="recommendations-section" aria-labelledby="recommendations-heading">
              <h2 id="recommendations-heading">Recommendations</h2>
              {/* *** USE the RecommendationsDisplay component *** */}
              {/* This component fetches its own data using the userId */}
              <RecommendationsDisplay />
            </aside>
          </main>

          {/* Optional Footer for pagination controls (would use SearchProvider context) */}
          {/* Add Paging, PagingInfo, ResultsPerPage components here later if needed */}
          {/* <footer className="search-footer">
            <PagingInfo />
            <ResultsPerPage />
            <Paging />
          </footer> */}

        </div>
      </ErrorBoundary>
    </SearchProvider>
  );
}

export default App;