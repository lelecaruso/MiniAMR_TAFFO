from subprocess import run
from random import randint
import matplotlib.pyplot as plt


NUM_TSTEPS = 10
NUM_VARS = 40
STAGE_PER_TS = 20

args = [
    "--num_refine", "4",
    "--max_blocks", "9000",
    "--init_x", "1",
    "--init_y", "1",
    "--init_z", "1",
    "--npx", "1",
    "--npy", "1",
    "--npz", "1",
    "--nx", "8",
    "--ny", "8",
    "--nz", "8",
    "--num_objects", "1",
    "--object", "2",
    "0", "-1.71", "-1.71", "-1.71",
    "0.04", "0.04", "0.04",
    "1.7", "1.7", "1.7",
    "0.0", "0.0", "0.0",
    "--num_tsteps", str(NUM_TSTEPS),
    "--report_diffusion",
    "--checksum_freq", "1"
]


def run_with_taffo(seed):
    return run(["./miniAMR.x", "--seed", str(seed)] + args, capture_output=True)


def run_base(seed):
    return run(["./miniAMR.base", "--seed", str(seed)] + args, capture_output=True)


def parse_output(output):
    base = -10
    data = []

    for step in range(1, NUM_TSTEPS + 1):
        data.append([])
        for stage in range(STAGE_PER_TS):
            data[step - 1].append([])
            for var in range(NUM_VARS):
                base = output.find(f'{step} var {var}', base + 10)

                if base == -1:
                    print(f"Could not find {step} var {var}")
                    continue

                sum = float(output[output.find('sum', base) + 4: output.find('old', base)])
                old = float(output[output.find('old', base) + 4: output.find('diff', base)])
                data[step - 1][stage].append((sum, old))

    return data


def error():
    #if __name__ == "__main__":
    seed = randint(0, 2 ** 32 - 1)

    output_taffo = run_with_taffo(seed).stdout.decode()
    output_base = run_base(seed).stdout.decode()

    data_taffo = parse_output(output_taffo)
    #print(data_taffo)
    data_base = parse_output(output_base)
    #print(data_base)

    # calculate difference between the two runs
    differences = []


    for step in range(0, NUM_TSTEPS):
        for j in range(STAGE_PER_TS):
            for k in range(NUM_VARS):
                diff = abs(data_taffo[step][j][k][0] - data_base[step][j][k][0])
                differences.append(diff)

    return differences

if __name__ == "__main__":
    errors = error()
    print(errors)  # Stampare le differenze calcolate

    seed = randint(0, 2 ** 32 - 1)

    output_taffo = run_with_taffo(seed).stdout.decode()
    output_base = run_base(seed).stdout.decode()

    data_taffo = parse_output(output_taffo)
    # print(data_taffo)
    data_base = parse_output(output_base)

    def flatten(arr):
        result = []
        for a in arr:
            for b in a:
                for c in b:
                    result.append(c[0])
        return result

    data_taffo = flatten(data_taffo)
    #print(data_taffo[:50])
    data_base = flatten(data_base)

    def plot_runs(data_taffo,data_base):

        plt.plot(data_taffo[:50], color='blue')
        plt.plot(data_base[:50], color='red')
        plt.title('Differences between runs N.B. blue = taffo, red = base')
        plt.xlabel('iter')
        plt.ylabel('Checksum value')
        plt.xticks(range(0, len(data_taffo[:50]), int(len(data_taffo[:50]) / 25)))
        plt.grid(True)

        plt.show()

    plot_runs(data_taffo,data_base)


    def plot_diff(errors):

        plt.plot(errors[:50], color='blue')
        plt.title('Errore assoluto: Differences between values of the two')
        plt.xlabel('iter')
        plt.ylabel('diff')
        plt.xticks(range(0, len(errors[:50]), int(len(errors[:50]) / 25)))
        plt.grid(True)

        plt.show()


    plot_diff(errors)




