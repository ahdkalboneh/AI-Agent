import os
import subprocess


def run_python_file(
    working_directory: str,
    file_path: str,
    args: list[str] | None = None
) -> str:
    try:
        # 1. absolute working directory
        working_directory_abs = os.path.abspath(working_directory)

        # 2. build full path
        full_file_path = os.path.normpath(
            os.path.join(working_directory_abs, file_path)
        )

        # 3. security check (inside working directory)
        if os.path.commonpath([working_directory_abs, full_file_path]) != working_directory_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # 4. must be a python file
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # 5. must exist and be file
        if not os.path.isfile(full_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        # 6. build command
        command = ["python", full_file_path]

        if args:
            command.extend(args)

        # 7. run process
        result = subprocess.run(
            command,
            cwd=working_directory_abs,
            capture_output=True,
            text=True,
            timeout=30
        )

        # 8. format output
        output_parts = []

        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")

        if not result.stdout and not result.stderr:
            output_parts.append("No output produced")
        else:
            if result.stdout:
                output_parts.append(f"STDOUT: {result.stdout}")
            if result.stderr:
                output_parts.append(f"STDERR: {result.stderr}")

        return "\n".join(output_parts).strip()

    except Exception as e:
        return f"Error: {str(e)}"
