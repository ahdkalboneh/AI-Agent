import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        # 1. absolute working directory
        working_directory_abs = os.path.abspath(working_directory)

        # 2. build full path safely
        full_file_path = os.path.normpath(
            os.path.join(working_directory_abs, file_path)
        )

        # 3. security check (no escaping working directory)
        if os.path.commonpath([working_directory_abs, full_file_path]) != working_directory_abs:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # 4. directory check (can't overwrite folders)
        if os.path.isdir(full_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # 5. ensure parent directories exist
        parent_dir = os.path.dirname(full_file_path)
        os.makedirs(parent_dir, exist_ok=True)

        # 6. write file (overwrite mode)
        with open(full_file_path, "w", encoding="utf-8") as f:
            f.write(content)

        # 7. success message
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {str(e)}"
