import json
import os
import glob
import fcntl
import time

class CreateStoryboard:
    """
    Class definition. Identify all unprocessed items from the input JSON tracker and pass them through the generate_storyboard() method.
    
    Takes in the following variables as class variables
    - A config file in json format
    - Path of the input JSON tracker processing outputs from the previous stage (example name: fit_scenes_tracker.json)
    - Google api key
    - Claude api key
    - a system prompt (just placeholder string)
    - a user prompt (just placeholder string)
    - Folder path of the RAG template descriptions
    - Folder path of the RAG template scripts
    - Index json file pointing to the RAG templates
    - A JSON output tracker (example name: storyboard_tracker.json) indicating the status of processed file content. The tracker should be a nested dictionary containing the following fields within 
    each sub-dictionary
       - Path to the output of this particular stage
       - The name of the topic being processed
       - A boolean value to indicate processed/unprocessed status
       - Every main key in the dictionary will be a unique identifier for every unprocessed file
       - Reason for failure

    Behavior of the class
    - Compare the input JSON tracker against the contents of the JSON output tracker
    - Identify all the unprocessed files
       - Presence of a False processed status in the input indicates unprocessed item (Do not pick this up)
       - Missing item or presence of a False processed status in the output indicates it is yet to be processed
    - Call the generate_storyboard() method for each of the unprocessed files
    - Update the JSON output tracker based on the status of processed (add an entry only if generate_storyboard() method execution is successful)
    - If any stage of the execution fails, capture the exception reason in the corrresponding field of the JSON output tracker
    - Implement a file lock for the JSON output tracker as it is likely to be modified by other code scripts
    """
    
    def __init__(self, config, input_tracker_path, google_api_key, claude_api_key, 
                 system_prompt, user_prompt, rag_template_desc_folder, rag_template_script_folder,
                 index_json_path, output_tracker_path):
        self.config = config
        self.input_tracker_path = input_tracker_path
        self.google_api_key = google_api_key
        self.claude_api_key = claude_api_key
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt
        self.rag_template_desc_folder = rag_template_desc_folder
        self.rag_template_script_folder = rag_template_script_folder
        self.index_json_path = index_json_path
        self.output_tracker_path = output_tracker_path
        
        # Initialize output tracker file if it doesn't exist
        if not os.path.exists(self.output_tracker_path):
            # Ensure the directory exists
            tracker_dir = os.path.dirname(self.output_tracker_path)
            if tracker_dir and not os.path.exists(tracker_dir):
                os.makedirs(tracker_dir, exist_ok=True)
                
            with open(self.output_tracker_path, 'w') as f:
                json.dump({}, f)

    def _load_tracker(self, filepath):
        """
        Load a JSON tracker with a shared lock (read lock).
        """
        if not os.path.exists(filepath):
            return {}
            
        try:
            with open(filepath, 'r') as f:
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
            print(f"Error loading tracker {filepath}: {e}")
            return {}

    def _save_tracker(self, filepath, data):
        """
        Save a JSON tracker with an exclusive lock (write lock).
        """
        try:
            with open(filepath, 'w') as f:
                # Acquire an exclusive lock
                fcntl.flock(f, fcntl.LOCK_EX)
                try:
                    json.dump(data, f, indent=4)
                finally:
                    fcntl.flock(f, fcntl.LOCK_UN)
        except Exception as e:
            print(f"Error saving tracker {filepath}: {e}")

    def generate_storyboard(self, topic_name, input_data):
        """
        Placeholder for the generate_storyboard logic.
        """
        print(f"  [Simulated] Generating storyboard for {topic_name}...")
        # Simulate processing delay
        # time.sleep(0.5)
        
        return {
            "storyboard_content": f"Storyboard content for {topic_name}...",
            "metadata": {
                "source": topic_name,
                "timestamp": time.time(),
                "config_used": self.config.get("name", "unknown")
            }
        }

    def process_items(self):
        """
        Main logic to process items from input tracker to output tracker.
        """
        # 1. Load Input Tracker
        input_tracker = self._load_tracker(self.input_tracker_path)
        if not input_tracker:
            print(f"Input tracker is empty or missing: {self.input_tracker_path}")
            return

        print(f"Found {len(input_tracker)} items in input tracker.")

        # 2. Iterate through items in input tracker
        for topic_name, input_entry in input_tracker.items():
            
            # Check if input item is fully processed
            if not input_entry.get("processed", False):
                print(f"Skipping {topic_name}: Input not marked as processed.")
                continue

            # Load Output Tracker to define current state
            output_tracker = self._load_tracker(self.output_tracker_path)

            # Check if already processed in output tracker
            if topic_name in output_tracker and output_tracker[topic_name].get("processed", False):
                print(f"Skipping {topic_name}: Already processed in output tracker.")
                continue

            print(f"Processing {topic_name}...")
            
            try:
                # 3. Call generate_storyboard
                # We might need data from the input entry, output path, etc.
                # Assuming input_entry has 'output_path' from previous stage we might want to read?
                # For now, just passing the entry itself.
                
                output_data = self.generate_storyboard(topic_name, input_entry)

                # Define output path
                # Assuming standard 'output' folder structure adjacent to trackers or defined in config
                output_dir = os.path.dirname(self.output_tracker_path)
                storyboard_output_path = os.path.join(output_dir, f"{topic_name}_storyboard.json")
                
                with open(storyboard_output_path, 'w') as out_f:
                    json.dump(output_data, out_f, indent=4)

                # 4. Update Output Tracker (Success)
                output_tracker = self._load_tracker(self.output_tracker_path)
                output_tracker[topic_name] = {
                    "output_path": storyboard_output_path,
                    "topic_name": topic_name,
                    "processed": True,
                    "failure_reason": None
                }
                self._save_tracker(self.output_tracker_path, output_tracker)
                print(f"Successfully generated storyboard for {topic_name}.")

            except Exception as e:
                print(f"Error processing {topic_name}: {e}")
                # 5. Update Output Tracker (Failure)
                output_tracker = self._load_tracker(self.output_tracker_path)
                output_tracker[topic_name] = {
                    "output_path": None,
                    "topic_name": topic_name,
                    "processed": False,
                    "failure_reason": str(e)
                }
                self._save_tracker(self.output_tracker_path, output_tracker)