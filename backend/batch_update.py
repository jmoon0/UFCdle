# Script to run batch updates
import requests
import time
import json

def run_batch_update(base_url, batch_size=3, max_retries=3):
    """Run the complete batch update process with a retry mechanism."""

    progress_response = requests.get(f"{base_url}/api/admin/db-progress")
    if progress_response.status_code == 200:
        progress = progress_response.json()
        print(f"Starting update: {progress['database_count']}/{progress['scraped_count']} fighters in database")
    
    start_index = 0
    total_updated = 0
    total_added = 0
    total_errors = 0
    
    while True:
        print(f"\n--- Processing batch starting at index {start_index} ---")

        batch_processed_successfully = False
        
        # --- START: Retry Loop ---
        for attempt in range(max_retries):
            try:
                payload = {
                    "batch_size": batch_size,
                    "start_index": start_index
                }
                
                response = requests.post(
                    f"{base_url}/api/admin/update-db",
                    json=payload,
                    timeout=30  # Keep the timeout for a single attempt
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if result.get("success"):

                        batch_results = result.get("results", {})
                        total_updated += batch_results.get("updated", 0)
                        total_added += batch_results.get("added", 0)
                        total_errors += batch_results.get("skipped", 0)
                        
                        # Print progress
                        progress = result.get("progress", {})
                        print(f" {result.get('message')}")
                        print(f"   Progress: {progress.get('percentage', 0)}%")
                        print(f"   This batch: +{batch_results.get('updated', 0)} updated, +{batch_results.get('added', 0)} added, {batch_results.get('skipped', 0)} skipped")
                        
                        # Show errors if any
                        if batch_results.get("errors"):
                            print(f"   Errors: {batch_results['errors'][:3]}")
                        
                        # Set up next batch
                        start_index = progress.get("next_start", start_index + batch_size)
                        
                        # Mark as successful to exit the retry loop
                        batch_processed_successfully = True

                        if not progress.get("has_more"):
                            break 
                        
                        print("   Waiting 5 seconds before next batch...")
                        time.sleep(5)
                        break 
                    
                    else:
                        print(f"Batch failed with success=false: {result}")
                        break # Break from retry loop, as this is a server-side failure
                else:
                    print(f"HTTP {response.status_code}: {response.text}")
                    time.sleep(10 * (attempt + 1))
                    
            except requests.exceptions.Timeout:
                print(f"⏱️  Timeout on attempt {attempt + 1}/{max_retries}. Retrying in {10 * (attempt + 1)} seconds...")
                time.sleep(10 * (attempt + 1))
                
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                break

        # --- END: Retry Loop ---

        # Check the progress of the overall update
        progress = result.get("progress", {}) if 'result' in locals() and result else {}
        if not progress.get("has_more"):
            print(f"\n Update complete!")
            print(f"Total: {total_updated} updated, {total_added} added, {total_errors} errors")
            break
        
        # If a batch failed all retries, skip it and move on  
        if not batch_processed_successfully:
            print(f"❌ Batch at index {start_index} failed after {max_retries} retries. Skipping.")
            start_index += batch_size

if __name__ == "__main__":
    BASE_URL = "https://ufcdle.vercel.app"
    
    print("Starting batch update process...")
    run_batch_update(BASE_URL, batch_size=4, max_retries=3)