import json
import os
import glob
import fcntl
import time

class FitToContext:
    """
    Class definition. Identify all unprocessed inputs and pass them through the fit_scene() method.
    
    Takes in the following variables as class variables
    - A config file in json format
    - A folder name pointing to location of all unprocessed txt files
    - Google api key
    - Claude api key
    - a system prompt (just placeholder string)
    - a user prompt (just placeholder string)
    - Folder path of the RAG template descriptions
    - Index json file pointing to the RAG templates
    - A JSON output tracker (example name: fit_scenes_tracker.json) indicating the status of processed file content. The tracker should be a nested dictionary containing the following fields within 
    each sub-dictionary
       - Path to the output of this stage corresponding to the starting input .txt file
       - A boolean value to indicate processed/unprocessed status
       - The name of the topic being processed
       - Every main key in the dictionary will be a unique identifier for every unprocessed file
       - Reason for failure

    Behavior of the class
    - Compare the txt files in the input folder (named based on topic names) against the contents of the JSON output tracker
    - Identify all the unprocessed files
    - Call the fit_scene() method for each of the unprocessed files (returns JSON output)
    - Update the JSON output tracker based on the status of processed (add an entry only if fit_scene() method execution is successful)
    - If any stage of the execution fails, capture the exception reason in the corrresponding field of the JSON output tracker
    - Implement a file lock for the JSON output tracker as it is likely to be modified by other code scripts

    """
    def __init__(self, config, input_folder, google_api_key, claude_api_key, 
                 system_prompt, user_prompt, rag_template_folder, 
                 index_json_path, tracker_file):
        self.config = config
        self.input_folder = input_folder
        self.google_api_key = google_api_key
        self.claude_api_key = claude_api_key
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt
        self.rag_template_folder = rag_template_folder
        self.index_json_path = index_json_path
        self.tracker_file = tracker_file
        
        # Initialize tracker file if it doesn't exist
        if not os.path.exists(self.tracker_file):
            # Ensure the directory exists
            tracker_dir = os.path.dirname(self.tracker_file)
            if tracker_dir and not os.path.exists(tracker_dir):
                os.makedirs(tracker_dir, exist_ok=True)
                
            with open(self.tracker_file, 'w') as f:
                json.dump({}, f)

    def _load_tracker(self):
        """
        Load the JSON tracker with a shared lock (read lock).
        """
        try:
            with open(self.tracker_file, 'r') as f:
                # Acquire a shared lock
                fcntl.flock(f, fcntl.LOCK_SH)
                try:
                    content = f.read()
                    if not content:
                        return {}
                    data = json.loads(content)
                except json.JSONDecodeError:
                    data = {}
                finally:
                    fcntl.flock(f, fcntl.LOCK_UN)
            return data
        except Exception as e:
            print(f"Error loading tracker: {e}")
            return {}

    def _save_tracker(self, data):
        """
        Save the JSON tracker with an exclusive lock (write lock).
        """
        try:
            with open(self.tracker_file, 'w') as f:
                # Acquire an exclusive lock
                fcntl.flock(f, fcntl.LOCK_EX)
                try:
                    json.dump(data, f, indent=4)
                finally:
                    fcntl.flock(f, fcntl.LOCK_UN)
        except Exception as e:
            print(f"Error saving tracker: {e}")

    def fit_scene(self, file_content, topic_name):
        """
        Placeholder for the fit_scene logic.
        This would typically call the LLM APIs using the API keys and prompts.
        """
        print(f"  [Simulated] Running fit_scene for {topic_name} using keys: {self.google_api_key[:5]}... / {self.claude_api_key[:5]}...")
        # Simulate processing delay
        # time.sleep(0.5) 
        
        # Return a dictionary mimicking the expected output structure
        output_data = {
            "processed_content": f"Processed content for {topic_name}...",
            "metadata": {
                "source": topic_name,
                "timestamp": time.time(),
                "config_used": self.config.get("name", "unknown")
            }
        }
        
        # Define output path (placeholder logic)
        output_dir = os.path.join(os.path.dirname(self.input_folder), "output")
        output_file_path = os.path.join(output_dir, f"{topic_name}_processed.json")
        
        # Ensure output dir exists
        os.makedirs(output_dir, exist_ok=True)
        
        with open(output_file_path, 'w') as out_f:
            json.dump(output_data, out_f, indent=4)
            
        return output_file_path

    def process_files(self):
        """
        Main logic to process unprocessed files.
        """
        # 1. List all .txt files in the input folder
        if not os.path.exists(self.input_folder):
            print(f"Input folder '{self.input_folder}' does not exist.")
            return

        txt_files = glob.glob(os.path.join(self.input_folder, "*.txt"))
        print(f"Found {len(txt_files)} files in '{self.input_folder}'")

        # 2. Iterate through files and check tracker
        for file_path in txt_files:
            file_name = os.path.basename(file_path)
            topic_name = os.path.splitext(file_name)[0] # Main key as unique identifier

            # Load tracker dynamically to get the latest state
            tracker = self._load_tracker()

            # Check if unprocessed
            if topic_name in tracker and tracker[topic_name].get("processed", False):
                print(f"Skipping {topic_name}: Already processed.")
                continue

            print(f"Processing {topic_name}...")
            
            try:
                # Read input file
                with open(file_path, 'r') as f:
                    content = f.read()

                # 3. Call fit_scene (Writes file and returns path)
                output_file_path = self.fit_scene(content, topic_name)

                # 4. Update tracker (Success)
                # Re-load tracker to minimize race conditions
                tracker = self._load_tracker()
                tracker[topic_name] = {
                    "output_path": output_file_path,
                    "processed": True,
                    "topic_name": topic_name,
                    "failure_reason": None
                }
                self._save_tracker(tracker)
                print(f"Successfully processed {topic_name}.")

            except Exception as e:
                print(f"Error processing {topic_name}: {e}")
                # 5. Update tracker (Failure)
                tracker = self._load_tracker()
                tracker[topic_name] = {
                    "output_path": None,
                    "processed": False,
                    "topic_name": topic_name,
                    "failure_reason": str(e)
                }
                self._save_tracker(tracker)