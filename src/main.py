import concurrent.futures
import time
import random
import memory_profiler

from src.sort import bubble_sort, quick_sort, insertion_sort
from src.grafico import generate
from src.search import sequential_search, binary_search

def time_and_memory(func, *args):
    "mide el tiempo y el uso de memorias de los diferentes algoritmos utilizados"
    start  = time.perf_counter()
    initial_memory = memory_profiler.memory_usage()[0]

    result = func(*args)

    final_memory = memory_profiler.memory_usage()[0]
    total_time = time.perf_counter() - start
    memory_used = final_memory - initial_memory

    return func.__name__, total_time, memory_used, result


def countdown():

    for i in range(3, 0, -1):
        print(f"\n   ⏳ {i}...")
        time.sleep(1)
    print("\n   🚦 ¡Listo! 🏁\n")
    time.sleep(1)
def race():
    "Se ejecutan los diferentes algoritmos de forma paralela y se muestran sus reporte"
    print("\n" + "=" * 30)
    print("🏁  CARRERA AMARANTE  🏁")
    print("=" * 30 + "\n")

    countdown()


    data = [random.randint(0, 1000) for _ in range(3000)]
    search_number = random.choice(data)

    algoritmos = [
        (bubble_sort, data[:]),
        (quick_sort, data[:]),
        (insertion_sort, data[:]),
        (sequential_search, data[:], search_number),
        (binary_search, sorted(data[:]), search_number)

    ]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(time_and_memory, *alg): alg[0].__name__ for alg in algoritmos}

        results = []
        for future in concurrent.futures.as_completed(futures):
            name, time, memory, _ = future.result()
            results.append((name, time, memory))
            generate(name, time)

    with open("reporte/carrerafinalizada.txt", "w", encoding="utf-8") as f:
        for name, time, memory in results:
            f.write(f"{name}: 🏁 {time:.5f} s | Memoria: {memory:.3f} MB\n")

if __name__ == "__main__":
    race()

