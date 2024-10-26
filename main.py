import requests
import time

def get_emote_set(set_id):
    """Fetches information about an emote set using the 7TV API"""
    url = f"https://7tv.io/v3/emote-sets/{set_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch emote set: {response.status_code}")

def add_emote_to_set(set_id, emote_id, emote_name, auth_token):
    """Adds an emote to the target set using the GraphQL API"""
    url = "https://7tv.io/v3/gql"
    
    cookies = {
        'seventv-auth': auth_token
    }
    
    headers = {
        'accept': '*/*',
        'content-type': 'application/json',
        'origin': 'https://7tv.app',
        'referer': 'https://7tv.app/'
    }
    
    json_data = [{
        'operationName': 'ChangeEmoteInSet',
        'variables': {
            'action': 'ADD',
            'id': set_id,
            'emote_id': emote_id,
            'name': emote_name
        },
        'query': '''
            mutation ChangeEmoteInSet($id: ObjectID!, $action: ListItemAction!, $emote_id: ObjectID!, $name: String) {
                emoteSet(id: $id) {
                    id
                    emotes(id: $emote_id, action: $action, name: $name) {
                        id
                        name
                    }
                }
            }
        '''
    }]
    
    try:
        response = requests.post(url, cookies=cookies, headers=headers, json=json_data)
        response_json = response.json() if response.text else {}
        
        if response.status_code not in [200, 204]:
            print(f"Error adding emote {emote_name}")
            print(f"Status code: {response.status_code}")
            print("Response:", response_json)
            return False
            
        if 'errors' in response_json[0]:
            if "conflicting" in response_json[0]:
                print(f"Emote {emote_name} already exists in the target set")
                return True
            
            else:
                print(f"GraphQL error adding emote {emote_name}:")
                print(response_json[0]['errors'])
                return False
        
        return True
        
    except Exception as e:
        print(f"Error adding emote {emote_name}: {str(e)}")
        return False

def copy_emote_set(source_set_id, target_set_id, auth_token):
    """Copies all emotes from one set to another"""
    try:
        # Fetch the source emote set
        source_set = get_emote_set(source_set_id)
        
        if not source_set or "emotes" not in source_set:
            print("Failed to load source emote set")
            return
        
        # Copy each emote
        total_emotes = len(source_set["emotes"])
        successful = 0
        
        print(f"Starting to copy {total_emotes} emotes...")
        
        for emote in source_set["emotes"]:
            emote_id = emote["id"]
            emote_name = emote["name"]
            
            print(f"Copying emote: {emote_name}")
            if add_emote_to_set(target_set_id, emote_id, emote_name, auth_token):
                successful += 1
                print(f"Successfully copied emote: {emote_name} | {successful}/{total_emotes}")
            else:
                print(f"Failed to copy emote: {emote_name} | {successful}/{total_emotes}")
            
            # Short wait between requests
            time.sleep(0.5)
        
        print(f"\nCopying completed!")
        print(f"Successfully copied: {successful}/{total_emotes} emotes")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Script usage
if __name__ == "__main__":
    SOURCE_SET_ID = "01G3M5YYJ800086RK1WFRADB1R"
    TARGET_SET_ID = "01JB4ACBH3PNY8MEMCG84896DY"
    AUTH_TOKEN = "seventv-auth"
    
    copy_emote_set(SOURCE_SET_ID, TARGET_SET_ID, AUTH_TOKEN)
