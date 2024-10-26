# 7TV Emote Set Copier

This Python script copies all emotes from a source emote set to a target emote set on 7TV. The script leverages the 7TV GraphQL API to achieve this.

## Requirements

- Python 3.x
- `requests` library

Install the `requests` library if you haven't already:

```bash
pip install requests
```

## Setup

1. **API Token**: You'll need an API token (`seventv-auth`) to authenticate with 7TV. You can obtain it through the 7TV platform.

2. **Emote Set IDs**:
   - Set the `SOURCE_SET_ID` to the ID of the emote set you want to copy from.
   - Set the `TARGET_SET_ID` to the ID of the emote set you want to copy to.

## Usage

1. Open the script and replace the following constants with your own values:
   - `SOURCE_SET_ID`: ID of the source emote set.
   - `TARGET_SET_ID`: ID of the target emote set.
   - `AUTH_TOKEN`: Your 7TV API token.

2. Run the script:

```bash
python main.py
```

The script will attempt to copy each emote from the source set to the target set, showing the success or failure of each emote transfer.

## Script Details

The script consists of three main functions:

- **`get_emote_set(set_id)`**: Fetches all emotes from the specified emote set using the 7TV API.
- **`add_emote_to_set(set_id, emote_id, emote_name, auth_token)`**: Adds an individual emote to the target set using the 7TV GraphQL API.
- **`copy_emote_set(source_set_id, target_set_id, auth_token)`**: Iterates through each emote in the source set and attempts to add it to the target set.

### Notes

- A short delay is added between each emote copy operation to avoid API rate limits.
- If an emote already exists in the target set, the script will skip it and log the result.

## License

This project is licensed under the MIT License.