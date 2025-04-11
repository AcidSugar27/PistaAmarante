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

def print_podium(title, resultados):
    print(f"\n🏆 PODIO: {title} 🏆\n")
    podium = sorted(resultados, key=lambda x: x[1])[:3]  # Top 3 por tiempo
    emojis = ["🥇", "🥈", "🥉"]

    for i, (name, time_exec, memory) in enumerate(podium):
        icon = emojis[i]
        trophy = " 🏆" if i == 0 else ""
        print(f"  {icon} {name} - {time_exec:.5f} s - Memoria: {memory:.3f} MB{trophy}")
    print("\n" + "-" * 40)



def race():
    print("\n" + "=" * 30)
    print("🏁  CARRERA AMARANTE  🏁")
    print("=" * 30 + "\n")

    countdown()

    data = [random.randint(0, 1000) for _ in range(3000)]
    search_number = random.choice(data)

    sorting_algorithms = [
        (bubble_sort, data[:]),
        (quick_sort, data[:]),
        (insertion_sort, data[:]),
    ]

    searching_algorithms = [
        (sequential_search, data[:], search_number),
        (binary_search, sorted(data[:]), search_number)
    ]

    results_sort = []
    results_search = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {}

        for alg in sorting_algorithms:
            futures[executor.submit(time_and_memory, *alg)] = ('sort', alg[0].__name__)
        for alg in searching_algorithms:
            futures[executor.submit(time_and_memory, *alg)] = ('search', alg[0].__name__)

        for future in concurrent.futures.as_completed(futures):
            category, name = futures[future]
            name, time_exec, memory, _ = future.result()
            generate(name, time_exec)

            if category == 'sort':
                results_sort.append((name, time_exec, memory))
            else:
                results_search.append((name, time_exec, memory))

    print_podium("ALGORTIMOS DE ORDENAMIENTO", results_sort)
    print_podium("ALGORITMOS DE BÚSQUEDA", results_search)

    # Guardar en archivo
    with open("reporte/carrerafinalizada.txt", "w", encoding="utf-8") as f:
        f.write("🏁 RESULTADOS DE LA CARRERA 🏁\n\n")
        for name, time_exec, memory in results_sort + results_search:
            f.write(f"{name}: {time_exec:.5f} s | Memoria: {memory:.3f} MB\n")

if __name__ == "__main__":
    race()

