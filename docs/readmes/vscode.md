## Visual Studio Code Integration

To reproduce the example setup included with the OpenSBT framework in [Microsoft Visual Studio Code](https://code.visualstudio.com/) copy the following `launch.json` and `tasks.json` files in the `.vscode` directory of your workspace. Make sure to replace all `/path/to/` paths according to your setup.

### launch.json

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "OpenSBT",
            "type": "python",
            "request": "launch",
            "program": "run.py",
            "console": "integratedTerminal",
            "justMyCode": true,
            "env": {
                "CARLA_ROOT": "/path/to/carla/repository",
                "PYTHONPATH": "/path/to/carla/repository/PythonAPI/carla/dist/carla-0.9.13-py3.7-linux-x86_64.egg:/path/to/carla/repository/PythonAPI/carla/agents:/path/to/carla/repository/PythonAPI/carla:/path/to/carla/scenario/runner/repository",
                "SCENARIO_RUNNER_ROOT": "/path/to/carla/scenario/runner/repository"
            },
            "args": [
                "-e", "1",
                "-n", "30",
                "-i", "50",
                "-t", "01:00:00",
                "-v"
            ],
            "preLaunchTask": "start",
            "postDebugTask": "stop"
        }
    ]
}
```

### tasks.json

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "make_directory",
            "type": "shell",
            "command": "mkdir",
            "args": [
                "-p",
                "/tmp/recordings"
            ]
        },
        {
            "label": "carla_start",
            "type": "shell",
            "command": "docker",
            "args": [
                "compose",
                "-f", "/path/to/opensbt/carla/runner/docker-compose.yml",
                "up",
                "-d",
                "--scale", "carla-server=2"
            ]
        },
        {
            "label": "carla_stop",
            "type": "shell",
            "command": "docker",
            "args": [
                "compose",
                "-f", "/path/to/opensbt/carla/runner/docker-compose.yml",
                "down"
            ]
        },
        {
            "label": "start",
            "dependsOn": [
                "make_directory",
                "carla_start"
            ]
        },
        {
            "label": "stop",
            "dependsOn": [
                "carla_stop"
            ]
        }
    ]
}
