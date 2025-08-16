# Script to run batch updates
import requests
import time
import json

def run_batch_update(base_url, batch_size=3):
    """Run the complete batch update process"""
    
    # Check initial progress
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
        
        # Send batch request
        payload = {
            "batch_size": batch_size,
            "start_index": start_index
        }
        
        try:
            response = requests.post(
                f"{base_url}/api/admin/update-db",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get("success"):
                    # Update totals
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
                        print(f"   Errors: {batch_results['errors'][:3]}")  # Show first 3 errors
                    
                    # Check if done
                    if not progress.get("has_more"):
                        print(f"\n Update complete!")
                        print(f"Total: {total_updated} updated, {total_added} added, {total_errors} errors")
                        break
                    
                    # Set up next batch
                    start_index = progress.get("next_start", start_index + batch_size)
                    
                    # Wait between batches to be nice to the server
                    print("   Waiting 5 seconds before next batch...")
                    time.sleep(5)
                    
                else:
                    print(f"Batch failed: {result}")
                    break
            else:
                print(f"HTTP {response.status_code}: {response.text}")
                break
                
        except requests.exceptions.Timeout:
            print(f"⏱️  Timeout for batch {start_index}, trying next batch...")
            start_index += batch_size
            time.sleep(10)
            
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    BASE_URL = "https://ufcdle.vercel.app"
    
    print("Starting batch update process...")
    run_batch_update(BASE_URL, batch_size=3)