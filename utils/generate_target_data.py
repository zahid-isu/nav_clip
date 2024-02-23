import json
import os
import random


# Function to determine relative position
def determine_relative_position(obj1, obj2):
    # center of each object
    obj1_center_x = obj1["origin"][0] + obj1["dimension"][0] / 2
    obj1_center_y = obj1["origin"][1] + obj1["dimension"][1] / 2
    obj2_center_x = obj2["origin"][0] + obj2["dimension"][0] / 2
    obj2_center_y = obj2["origin"][1] + obj2["dimension"][1] / 2

    # horizontal and vertical distances between centers
    dx = abs(obj1_center_x - obj2_center_x)
    dy = abs(obj1_center_y - obj2_center_y)

    # sum of half-widths of the objects
    half_width1 = obj1["dimension"][0] / 2
    half_width2 = obj2["dimension"][0] / 2

    # Check if obj1 is in front of or behind obj2 based on horizontal distance
    if dx < half_width1 + half_width2:
        if obj1_center_y < obj2_center_y:
            return "behind"
        else:
            return "in front"

    # Check left or right based on horizontal position
    if obj1_center_x < obj2_center_x:
        return "to the left"
    elif obj1_center_x > obj2_center_x:
        return "to the right"
    else:
        return "on the same vertical line"

# generate target data from a single JSON file
def generate_target_data_from_json(json_file_path, swap_objects=False):
    # Load the source json
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    captures = data["captures"][0]
    annotations = captures["annotations"][0]["values"]
    target_data = []

    for i in range(len(annotations)):
        for j in range(len(annotations)):
            if i != j:
                obj1 = annotations[i]
                obj2 = annotations[j]
                relative_position = determine_relative_position(obj1, obj2)
                #True_caption
                if relative_position =="behind":
                    true_caption = f"The {(' ').join(obj1['labelName'].split('_')).lower()} is {relative_position} the {(' ').join(obj2['labelName'].split('_')).lower()}."
                else:
                    true_caption = f"The {(' ').join(obj1['labelName'].split('_')).lower()} is {relative_position} of the {(' ').join(obj2['labelName'].split('_')).lower()}."
                
                #False_caption: swap_objects= True or swap_sp_words= left -> right
                if swap_objects: 
                    if relative_position =="behind":
                        false_caption = f"The {(' ').join(obj2['labelName'].split('_')).lower()} is {relative_position} the {(' ').join(obj1['labelName'].split('_')).lower()}."
                    else:
                        false_caption = f"The {(' ').join(obj2['labelName'].split('_')).lower()} is {relative_position} of the {(' ').join(obj1['labelName'].split('_')).lower()}."
                else: 
                    if relative_position =="behind":
                        false_caption = f"The {(' ').join(obj1['labelName'].split('_')).lower()} is in front of the {(' ').join(obj2['labelName'].split('_')).lower()}."
                    else:
                        if relative_position== "to the right":
                            false_caption = f"The {(' ').join(obj1['labelName'].split('_')).lower()} is to the left of the {(' ').join(obj2['labelName'].split('_')).lower()}."
                        else:
                            false_caption = f"The {(' ').join(obj1['labelName'].split('_')).lower()} is to the right of the {(' ').join(obj2['labelName'].split('_')).lower()}."

                transformed_data = {
                "image_id": captures["filename"].split(".")[0][4:],
                "true_caption": true_caption,
                "false_caption": false_caption,
                "relation_info": {
                    "object": str(obj2["instanceId"]),
                    "name": relative_position 
                },
                "primary_object_id": str(obj1["instanceId"]),
                "primary_object_name": (' ').join(obj1["labelName"].split('_')).lower(),
                "bbox_x": obj1["origin"][0],
                "bbox_y": obj1["origin"][1],
                "bbox_w": obj1["dimension"][0],
                "bbox_h": obj1["dimension"][1],
                "relation_name": relative_position, 
                "image_path": "unity/unity_data/" + captures["filename"]
                }
                target_data.append(transformed_data)
                
    return target_data

# Function to generate target data from a folder of JSON files
def generate_target_data_from_folder(folder_path, swap_objects=False):
    target_data = []
    
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            json_file_path = os.path.join(folder_path, filename)
            target_data.extend(generate_target_data_from_json(json_file_path, swap_objects))
    
    return target_data
            
if __name__ == "__main__":
    folder_path = 'unity/unity_data/'  # Replace with your folder path
    target_data = generate_target_data_from_folder(folder_path, swap_objects=True)

    # Save the target JSON file
    target_data_sorted = sorted(target_data, key=lambda x: x['image_id'])
    print(len(target_data_sorted))

    with open('target_data.json', 'w') as outfile:
        json.dump(target_data_sorted, outfile, indent=4)

    # Print the first few items in target_data for verification
    for item in target_data_sorted[:5]:
        print(item)


