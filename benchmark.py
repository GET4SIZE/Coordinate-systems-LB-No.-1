"""
Бенчмаркінг продуктивності обчислень відстаней
у різних системах координат
"""

import time
import random
import math
from typing import List, Tuple
from coordinate_systems import (
    CartesianPoint2D, PolarPoint,
    CartesianPoint3D, SphericalPoint
)
from distances import (
    distance_2d_cartesian, distance_2d_polar,
    distance_3d_cartesian, distance_3d_spherical_chord,
    distance_3d_spherical_arc
)


def generate_2d_test_data(n: int) -> Tuple[List[Tuple[PolarPoint, PolarPoint]], 
                                             List[Tuple[CartesianPoint2D, CartesianPoint2D]]]:
    """
    Генерує n пар точок для 2D бенчмарків
    Повертає: (список пар полярних точок, список пар декартових точок)
    """
    random.seed(42)  # Для відтворюваності результатів
    
    polar_pairs = []
    for _ in range(n):
        # Генеруємо випадкові полярні координати
        r1 = random.uniform(1, 100)
        angle1 = random.uniform(0, 2 * math.pi)
        r2 = random.uniform(1, 100)
        angle2 = random.uniform(0, 2 * math.pi)
        
        p1 = PolarPoint(r1, angle1)
        p2 = PolarPoint(r2, angle2)
        polar_pairs.append((p1, p2))
    
    # Конвертуємо у декартові координати
    cartesian_pairs = [
        (CartesianPoint2D.from_polar(p1), CartesianPoint2D.from_polar(p2))
        for p1, p2 in polar_pairs
    ]
    
    return polar_pairs, cartesian_pairs


def generate_3d_test_data(n: int) -> Tuple[List[Tuple[SphericalPoint, SphericalPoint]], 
                                             List[Tuple[CartesianPoint3D, CartesianPoint3D]]]:
    """
    Генерує n пар точок для 3D бенчмарків
    Умова: для кожної пари радіуси однакові (для дугової відстані)
    Повертає: (список пар сферичних точок, список пар декартових точок)
    """
    random.seed(42)
    
    spherical_pairs = []
    for _ in range(n):
        # Генеруємо спільний радіус для пари
        radius = random.uniform(10, 100)
        
        # Перша точка
        azimuth1 = random.uniform(0, 2 * math.pi)
        polar_angle1 = random.uniform(0, math.pi)
        
        # Друга точка (з тим же радіусом)
        azimuth2 = random.uniform(0, 2 * math.pi)
        polar_angle2 = random.uniform(0, math.pi)
        
        p1 = SphericalPoint(radius, azimuth1, polar_angle1)
        p2 = SphericalPoint(radius, azimuth2, polar_angle2)
        spherical_pairs.append((p1, p2))
    
    # Конвертуємо у декартові координати
    cartesian_pairs = [
        (CartesianPoint3D.from_spherical(p1), CartesianPoint3D.from_spherical(p2))
        for p1, p2 in spherical_pairs
    ]
    
    return spherical_pairs, cartesian_pairs


def benchmark_2d(n: int = 100_000):
    """Бенчмарк для 2D відстаней"""
    print("=" * 70)
    print(f"БЕНЧМАРК 2D (n = {n:,} пар точок)")
    print("=" * 70)
    
    print(f"\nГенерація тестових даних...")
    polar_pairs, cartesian_pairs = generate_2d_test_data(n)
    print(f"✓ Згенеровано {n:,} пар точок")
    
    # Бенчмарк А: Полярні координати
    print("\n[A] Обчислення у полярних координатах (теорема косинусів)...")
    start = time.perf_counter()
    polar_distances = [distance_2d_polar(p1, p2) for p1, p2 in polar_pairs]
    time_polar = time.perf_counter() - start
    print(f"    Час виконання: {time_polar:.6f} секунд")
    
    # Бенчмарк Б: Декартові координати
    print("\n[B] Обчислення у декартових координатах (евклідова відстань)...")
    start = time.perf_counter()
    cartesian_distances = [distance_2d_cartesian(c1, c2) for c1, c2 in cartesian_pairs]
    time_cartesian = time.perf_counter() - start
    print(f"    Час виконання: {time_cartesian:.6f} секунд")
    
    # Аналіз
    print("\n" + "-" * 70)
    print("РЕЗУЛЬТАТИ:")
    ratio = time_polar / time_cartesian
    print(f"  Полярна:    {time_polar:.6f} с")
    print(f"  Декартова:  {time_cartesian:.6f} с")
    print(f"  Співвідношення (Polar/Cartesian): {ratio:.2f}x")
    
    if time_polar < time_cartesian:
        faster = "Полярна"
        percent = ((time_cartesian - time_polar) / time_cartesian) * 100
    else:
        faster = "Декартова"
        percent = ((time_polar - time_cartesian) / time_polar) * 100
    
    print(f"  Швидша система: {faster} (на {percent:.1f}%)")
    
    return {
        'polar': time_polar,
        'cartesian': time_cartesian,
        'ratio': ratio
    }


def benchmark_3d(n: int = 100_000):
    """Бенчмарк для 3D відстаней"""
    print("\n" + "=" * 70)
    print(f"БЕНЧМАРК 3D (n = {n:,} пар точок)")
    print("=" * 70)
    
    print(f"\nГенерація тестових даних...")
    spherical_pairs, cartesian_pairs = generate_3d_test_data(n)
    print(f"✓ Згенеровано {n:,} пар точок")
    
    # Бенчмарк А: Сферична (хорда)
    print("\n[A] Обчислення у сферичних координатах (пряма відстань - хорда)...")
    start = time.perf_counter()
    chord_distances = [distance_3d_spherical_chord(s1, s2) for s1, s2 in spherical_pairs]
    time_chord = time.perf_counter() - start
    print(f"    Час виконання: {time_chord:.6f} секунд")
    
    # Бенчмарк Б: Сферична (дуга)
    print("\n[B] Обчислення у сферичних координатах (дугова відстань)...")
    start = time.perf_counter()
    arc_distances = [distance_3d_spherical_arc(s1, s2) for s1, s2 in spherical_pairs]
    time_arc = time.perf_counter() - start
    print(f"    Час виконання: {time_arc:.6f} секунд")
    
    # Бенчмарк В: Декартова
    print("\n[C] Обчислення у декартових координатах (евклідова відстань)...")
    start = time.perf_counter()
    cartesian_distances = [distance_3d_cartesian(c1, c2) for c1, c2 in cartesian_pairs]
    time_cartesian = time.perf_counter() - start
    print(f"    Час виконання: {time_cartesian:.6f} секунд")
    
    # Аналіз
    print("\n" + "-" * 70)
    print("РЕЗУЛЬТАТИ:")
    times = [
        ('Сферична (хорда)', time_chord),
        ('Сферична (дуга)', time_arc),
        ('Декартова', time_cartesian)
    ]
    times_sorted = sorted(times, key=lambda x: x[1])
    
    print(f"  Сферична (хорда):  {time_chord:.6f} с")
    print(f"  Сферична (дуга):   {time_arc:.6f} с")
    print(f"  Декартова:         {time_cartesian:.6f} с")
    
    print(f"\n  Рейтинг за швидкістю:")
    for i, (name, t) in enumerate(times_sorted, 1):
        print(f"    {i}. {name}: {t:.6f} с")
    
    fastest_time = times_sorted[0][1]
    slowest_time = times_sorted[-1][1]
    print(f"\n  Різниця між найшвидшою та найповільнішою: {(slowest_time/fastest_time):.2f}x")
    
    return {
        'chord': time_chord,
        'arc': time_arc,
        'cartesian': time_cartesian
    }


if __name__ == "__main__":
    # Запуск бенчмарків
    results_2d = benchmark_2d(100_000)
    results_3d = benchmark_3d(100_000)
    
    # Підсумок
    print("\n" + "=" * 70)
    print("ЗАГАЛЬНИЙ ПІДСУМОК")
    print("=" * 70)
    print("\n2D:")
    print(f"  Полярна система:    {results_2d['polar']:.6f} с")
    print(f"  Декартова система:  {results_2d['cartesian']:.6f} с")
    print(f"  Співвідношення:     {results_2d['ratio']:.2f}x")
    
    print("\n3D:")
    print(f"  Сферична (хорда):   {results_3d['chord']:.6f} с")
    print(f"  Сферична (дуга):    {results_3d['arc']:.6f} с")
    print(f"  Декартова:          {results_3d['cartesian']:.6f} с")
    
    print("\n" + "=" * 70)
