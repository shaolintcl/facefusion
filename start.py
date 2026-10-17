"""Start FaceFusion with the project's environment and NVIDIA acceleration."""

import os
from pathlib import Path
import subprocess
import sys


def main() -> int:
    root = Path(__file__).resolve().parent
    python = root / '.venv' / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    if not python.is_file():
        print('Project environment not found: ' + str(python), file=sys.stderr)
        return 1

    env = os.environ.copy()
    env['GRADIO_ANALYTICS_ENABLED'] = 'False'
    env.setdefault('FACEFUSION_LANGUAGE', 'zh-CN')
    env['PYTHONUTF8'] = '1'
    if os.name == 'nt':
        cuda = env.get('CUDA_PATH')
        if cuda and (Path(cuda) / 'bin').is_dir():
            env['PATH'] = str(Path(cuda) / 'bin') + os.pathsep + env.get('PATH', '')

    return subprocess.call(
        [str(python), str(root / 'facefusion.py'), 'run',
         '--execution-providers', 'cuda', '--open-browser', *sys.argv[1:]],
        cwd=root,
        env=env,
    )


if __name__ == '__main__':
    raise SystemExit(main())
