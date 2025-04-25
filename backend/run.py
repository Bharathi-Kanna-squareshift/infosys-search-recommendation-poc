# run.py
import uvicorn
import argparse
import os

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Run the FastAPI application using Uvicorn.")
    parser.add_argument(
        "--host",
        type=str,
        default=os.getenv("HOST", "127.0.0.1"), # Default to localhost, allow override via HOST env var
        help="Host IP address to bind the server to."
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("PORT", "8000")), # Default to 8000, allow override via PORT env var
        help="Port number to bind the server to."
    )
    parser.add_argument(
        "--reload",
        action="store_true", # Makes this a flag, default is False
        help="Enable auto-reload for development (changes trigger server restart)."
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=int(os.getenv("WORKERS", "1")), # Default to 1 worker
        help="Number of worker processes (set > 1 for production)."
    )

    args = parser.parse_args()

    # --- Important Note on Reload and Workers ---
    # Uvicorn's --reload mode is primarily for development and typically
    # runs with a single worker. Using --reload with multiple workers
    # (--workers > 1) might lead to unexpected behavior.
    # Production deployments should NOT use --reload.
    if args.reload and args.workers > 1:
        print("Warning: Using --reload with --workers > 1 is not recommended. Defaulting to 1 worker for reload mode.")
        effective_workers = 1
    else:
        effective_workers = args.workers


    print(f"--- Starting FastAPI Server ---")
    print(f"Application: app.main:app")
    print(f"Host:        {args.host}")
    print(f"Port:        {args.port}")
    print(f"Reload:      {args.reload}")
    print(f"Workers:     {effective_workers}")
    print(f"-----------------------------")


    # Run Uvicorn programmatically
    uvicorn.run(
        "app.main:app",  # The path to your FastAPI app instance 'app' in 'app/main.py'
        host=args.host,
        port=args.port,
        reload=args.reload, # Pass the reload flag
        workers=effective_workers, # Pass the number of workers
        log_level="info" # Set a default log level
        # You can add other uvicorn options here if needed, like:
        # ssl_keyfile="path/to/key.pem",
        # ssl_certfile="path/to/cert.pem",
    )