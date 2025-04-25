
class FastAPIConnector {
  /**
   * @param {string} backendSearchUrl 
   */
  constructor(backendSearchUrl) {
    if (!backendSearchUrl) {
      throw new Error("backendSearchUrl parameter is required when creating FastAPIConnector");
    }
    this.searchUrl = backendSearchUrl;
    console.log(`FastAPIConnector initialized with search URL: ${this.searchUrl}`);
  }

  /**
   * @param {object} requestState Current state from Search UI (searchTerm, pagination, filters, etc.)
   * @param {object} queryConfig Configuration options from SearchProvider (less commonly used with custom connectors)
   * @returns {Promise<object>} Promise resolving to the Search UI state update object
   */
  async onSearch(requestState, queryConfig) {
    console.log("FastAPIConnector: onSearch triggered with state:", JSON.stringify(requestState, null, 2));

    const {
      searchTerm = "", 
    } = requestState;

    // Prepare the request body matching the FastAPI SearchRequest model
    // which only expects a 'query' field.
    const backendRequestBody = {
      query: searchTerm,
    };

    console.log("FastAPIConnector: Sending request to backend:", this.searchUrl, "with body:", JSON.stringify(backendRequestBody, null, 2));

    try {
      const response = await fetch(this.searchUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json', 
        },
        body: JSON.stringify(backendRequestBody), 
      });

      let data;
      let parseError = null;
      try {
          // Try to parse the response as JSON regardless of status code initially
          data = await response.json();
      } catch (e) {
          console.error("FastAPIConnector: Failed to parse response as JSON.", e);
          parseError = e; 
      }

      if (!response.ok) {
        console.error(`FastAPIConnector: Backend returned HTTP status ${response.status}`, data || "Response body could not be parsed as JSON.");
        const errorMessage = data?.detail || `Search request failed: ${response.status} ${response.statusText}`;
        throw new Error(errorMessage); 
      }

      if (parseError) {
          console.error("FastAPIConnector: Backend returned OK status but response was not valid JSON.");
          throw new Error("Received unexpected non-JSON success response from backend.");
      }

      console.log("FastAPIConnector: Received successful response data from backend:", data);


      const transformedResponse = {
        results: data?.results ?? [],
        totalResults: data?.meta?.page?.total_results ?? 0, // Expects a number
        totalPages: data?.meta?.page?.total_pages ?? 0,     // Expects a number
        requestId: data?.meta?.request_id ?? "",           // Expects a string 
      };
      console.log("FastAPIConnector: Returning transformed response to Search UI:", transformedResponse);
      return transformedResponse; 

    } catch (error) {
      console.error(" CRITICAL: Error caught within FastAPIConnector onSearch execution:", error);

 
      return {
        results: [],
        totalResults: 0,
        totalPages: 0,
        requestId: "",
        error: error.message 
      };
    }
  }


  async onAutocomplete(requestState, queryConfig) {
    console.log("FastAPIConnector: onAutocomplete triggered (not implemented)", requestState);

    // TODO: Implement backend call for autocomplete suggestions if needed

    // Return empty results for now
    return {
      autocompletedResults: [],
      autocompletedSuggestions: {}
    };
  }

}

export default FastAPIConnector;