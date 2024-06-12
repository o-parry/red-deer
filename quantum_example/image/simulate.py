from sys import argv
from json import dump

from qiskit import transpile
from qiskit_aer import AerSimulator
from qiskit.circuit.random import random_circuit
from qiskit.providers.fake_provider import FakeProvider

# Read the array task ID from the command line.
array_task_id = int(argv[1])
# The args file will be copied into the image (see %files section in image.def).
args_file = "/image/args.csv"
# The results folder is inside the working directory for the job (see job.bash).
# By default, Apptainer automatically binds the working directory.
results_file = f"results/{array_task_id}.json"

# Look up the line in args.csv corresponding to the array task ID to get the
# arguments for this particular array task.
with open(args_file) as f:
    for i, line in enumerate(f):
        if i == array_task_id: 
            num_qubits, depth, fake_backend_name = line.strip().split(",", 2)

circuit = random_circuit(int(num_qubits), int(depth), measure=True)
fake_backend = FakeProvider().get_backend(fake_backend_name)
simulator = AerSimulator.from_backend(fake_backend)
circuit = transpile(circuit, simulator)
# This is intended to be a single-threaded array task, so make sure we only
# use a single thread.
job = simulator.run(circuit, max_parallel_threads=1)
results = job.result().get_counts(circuit)
with open(results_file, "w") as f: dump(results, f, indent=4)
