"""
Головний файл для запуску всіх тестів та бенчмарків
Лабораторна робота №1: Програмні моделі систем координат
"""

import sys
from test_conversions import (
    test_2d_conversions,
    test_3d_conversions,
    test_distance_equivalence
)
from benchmark import benchmark_2d, benchmark_3d


def print_menu():
    """Виводить меню вибору"""
    print("\n" + "=" * 70)
    print("ЛАБОРАТОРНА РОБОТА №1: ПРОГРАМНІ МОДЕЛІ СИСТЕМ КООРДИНАТ")
    print("=" * 70)
    print("\nОберіть опцію:")
    print("  1. Запустити тести коректності перетворень")
    print("  2. Запустити бенчмарки продуктивності")
    print("  3. Запустити все (тести + бенчмарки)")
    print("  4. Вийти")
    print("=" * 70)


def run_tests():
    """Запуск всіх тестів коректності"""
    print("\nЗАПУСК ТЕСТІВ КОРЕКТНОСТІ\n")
    test_2d_conversions()
    test_3d_conversions()
    test_distance_equivalence()
    print("\n" + "=" * 70)
    print("ТЕСТУВАННЯ ЗАВЕРШЕНО")
    print("=" * 70)


def run_benchmarks():
    """Запуск бенчмарків продуктивності"""
    print("\nЗАПУСК БЕНЧМАРКІВ ПРОДУКТИВНОСТІ\n")
    results_2d = benchmark_2d(100_000)
    results_3d = benchmark_3d(100_000)

    # Підсумок
    print("\n" + "=" * 70)
    print("ЗАГАЛЬНИЙ ПІДСУМОК БЕНЧМАРКІВ")
    print("=" * 70)
    print("\n2D Обчислення:")
    print(f"  ├─ Полярна система:    {results_2d['polar']:.6f} с")
    print(f"  ├─ Декартова система:  {results_2d['cartesian']:.6f} с")
    print(f"  └─ Співвідношення:     {results_2d['ratio']:.2f}x")

    print("\n3D Обчислення:")
    print(f"  ├─ Сферична (хорда):   {results_3d['chord']:.6f} с")
    print(f"  ├─ Сферична (дуга):    {results_3d['arc']:.6f} с")
    print(f"  └─ Декартова:          {results_3d['cartesian']:.6f} с")

    print("\n" + "=" * 70)
    print("✓ БЕНЧМАРКІНГ ЗАВЕРШЕНО")
    print("=" * 70)


def run_all():
    """Запуск всього: тести + бенчмарки"""
    run_tests()
    print("\n")
    run_benchmarks()


def interactive_mode():
    """Інтерактивний режим з меню"""
    while True:
        print_menu()
        choice = input("\nВаш вибір (1-4): ").strip()

        if choice == '1':
            run_tests()
        elif choice == '2':
            run_benchmarks()
        elif choice == '3':
            run_all()
        elif choice == '4':
            print("\nДо побачення!\n")
            break
        else:
            print("\nНевірний вибір. Спробуйте ще раз.")

        if choice in ['1', '2', '3']:
            input("\nНатисніть Enter для продовження...")


def main():
    """Головна функція"""
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg == 'test' or arg == 'tests':
            run_tests()
        elif arg == 'bench' or arg == 'benchmark':
            run_benchmarks()
        elif arg == 'all':
            run_all()
        else:
            print(f"Невідома команда: {sys.argv[1]}")
            print("Використання:")
            print("  python3 main.py            # Інтерактивний режим")
            print("  python3 main.py test       # Тільки тести")
            print("  python3 main.py benchmark  # Тільки бенчмарки")
            print("  python3 main.py all        # Все разом")
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
