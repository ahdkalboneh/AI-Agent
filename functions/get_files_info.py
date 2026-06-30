import os

from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
        "directory": types.Schema(
            type=types.Type.STRING,
            description="Directory path relative to working directory"
        ),
    },
    required=["directory"]
 )
)

schema_get_file_content =  types.FunctionDeclaration(
    name="get_file_content",
    description="Read a file and return its contents (up to a limit)",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the file relative to working directory"
            )
        },
        required=["file_path"]
    )
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content to a file inside the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of file to write"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Text content to write into the file"
            )
        },
        required=["file_path", "content"]
    )
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a Python file inside the working directory with optional arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Python file path relative to working directory"
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of arguments"
            )
        },
        required=["file_path"]
    )
)

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)

        full_target_path = os.path.normpath(
            os.path.join(working_directory_abs, directory)
        )

        if os.path.commonpath([working_directory_abs, full_target_path]) != working_directory_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(full_target_path):
            return f'Error: "{directory}" is not a directory'

        items = []

        for item in os.listdir(full_target_path):
            if item == "__pycache__":
                continue
            item_path = os.path.join(full_target_path, item)

            is_dir = os.path.isdir(item_path)
            size = os.path.getsize(item_path)

            items.append(
                f"- {item}: file_size={size} bytes, is_dir={is_dir}"
            )

        return "\n".join(items)

    except Exception as e:
        return f"Error: {str(e)}"
