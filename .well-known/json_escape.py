import json

def main():
    # Open the input file and read all content
    with open('ai-plugin.source', 'r') as f:
        content = f.read()

    # Escape the string so it can be inserted into another JSON object
    escaped_content = json.dumps(content)

    # Create the final JSON object
    final_json = {
        "description_for_model": escaped_content
    }

    # Write the final JSON object to the output file
    with open('output.json', 'w') as f:
        f.write(json.dumps(final_json, indent=4))

if __name__ == "__main__":
    main()
