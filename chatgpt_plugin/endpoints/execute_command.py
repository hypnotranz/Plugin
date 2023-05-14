# execute_command.py
import quart
import logging
import subprocess

async def execute_command():
    request_data = await quart.request.get_json(force=True)
    command = request_data.get("command")
    stdin = request_data.get("stdin")

    if not command:
        return quart.jsonify({"error": "No command provided"}), 400

    logging.info(f"Executing command: {command}")

    process = subprocess.Popen(
        command,
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    stdout, stderr = process.communicate(stdin)

    logging.info(f"Command output (stdout): {stdout}")
    logging.info(f"Command output (stderr): {stderr}")

    return quart.jsonify({"command": command, "stdout": stdout, "stderr": stderr})
