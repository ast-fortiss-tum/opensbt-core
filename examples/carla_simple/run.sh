# we need to create recordings directory and give full rights
mkdir -p tmp/recordings 
current_perms=$(stat -c "%a" tmp/recordings)
if [ "$current_perms" -ne 777 ]; then
    sudo chmod 777 -R tmp/recordings
fi

# REPLACE THE PATHS WITH THE ACTUAL PATHS IN YOUR SYSTEM

export CARLA_ROOT=~/CARLA_0.9.13
export PYTHONPATH=~/CARLA_0.9.13/PythonAPI/carla/dist/carla-0.9.13-py3.7-linux-x86_64.egg:~/CARLA_0.9.13/PythonAPI/carla/agents:~/CARLA_0.9.13/PythonAPI/carla:~/scenario_runner
export SCENARIO_RUNNER_ROOT=~/scenario_runner

# run experiment
python -m examples.carla_simple.run_carla_exp