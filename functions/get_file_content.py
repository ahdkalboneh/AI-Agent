import os
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)

        full_file_path = os.path.normpath(
            os.path.join(working_directory_abs, file_path)
        )

        if os.path.commonpath([working_directory_abs, full_file_path]) != working_directory_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(full_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(full_file_path, "r", encoding="utf-8") as f:
            content = f.read(MAX_CHARS)

            extra = f.read(1)
            if extra:
                content += f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content

    except Exception as e:
        return f"Error: {str(e)}"
