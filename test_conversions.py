"""
Тести для перевірки коректності перетворень між системами координат
"""

import math
from coordinate_systems import (
    CartesianPoint2D, PolarPoint,
    CartesianPoint3D, SphericalPoint
)


def test_2d_conversions():
    """Тестування перетворень між декартовою та полярною системами (2D)"""
    print("=" * 70)
    print("ТЕСТУВАННЯ 2D ПЕРЕТВОРЕНЬ")
    print("=" * 70)
    
    # Тестові точки
    test_cases_2d = [
        CartesianPoint2D(1, 0),
        CartesianPoint2D(0, 1),
        CartesianPoint2D(3, 4),
        CartesianPoint2D(-2, 2),
        CartesianPoint2D(5, -5),
    ]
    
    for i, original in enumerate(test_cases_2d, 1):
        print(f"\nТест {i}:")
        print(f"  Оригінал (Декартова):  {original}")
        
        # Декартова -> Полярна
        polar = PolarPoint.from_cartesian(original)
        print(f"  Перетворено (Полярна): {polar}")
        
        # Полярна -> Декартова (зворотне перетворення)
        back = CartesianPoint2D.from_polar(polar)
        print(f"  Назад (Декартова):     {back}")
        
        # Перевірка точності
        error_x = abs(original.x - back.x)
        error_y = abs(original.y - back.y)
        max_error = max(error_x, error_y)
        
        print(f"  Похибка: x={error_x:.2e}, y={error_y:.2e}, max={max_error:.2e}")
        
        if max_error < 1e-10:
            print("  ✓ Перетворення КОРЕКТНЕ")
        else:
            print("  ✗ Перетворення НЕКОРЕКТНЕ")


def test_3d_conversions():
    """Тестування перетворень між декартовою та сферичною системами (3D)"""
    print("\n" + "=" * 70)
    print("ТЕСТУВАННЯ 3D ПЕРЕТВОРЕНЬ")
    print("=" * 70)
    
    # Тестові точки
    test_cases_3d = [
        CartesianPoint3D(1, 0, 0),
        CartesianPoint3D(0, 1, 0),
        CartesianPoint3D(0, 0, 1),
        CartesianPoint3D(3, 4, 5),
        CartesianPoint3D(-2, 3, -4),
        CartesianPoint3D(1, 1, 1),
    ]
    
    for i, original in enumerate(test_cases_3d, 1):
        print(f"\nТест {i}:")
        print(f"  Оригінал (Декартова):   {original}")
        
        # Декартова -> Сферична
        spherical = SphericalPoint.from_cartesian(original)
        print(f"  Перетворено (Сферична): {spherical}")
        
        # Сферична -> Декартова (зворотне перетворення)
        back = CartesianPoint3D.from_spherical(spherical)
        print(f"  Назад (Декартова):      {back}")
        
        # Перевірка точності
        error_x = abs(original.x - back.x)
        error_y = abs(original.y - back.y)
        error_z = abs(original.z - back.z)
        max_error = max(error_x, error_y, error_z)
        
        print(f"  Похибка: x={error_x:.2e}, y={error_y:.2e}, z={error_z:.2e}, max={max_error:.2e}")
        
        if max_error < 1e-10:
            print("  ✓ Перетворення КОРЕКТНЕ")
        else:
            print("  ✗ Перетворення НЕКОРЕКТНЕ")


def test_distance_equivalence():
    """Перевірка еквівалентності обчислення відстаней"""
    print("\n" + "=" * 70)
    print("ПЕРЕВІРКА ЕКВІВАЛЕНТНОСТІ ВІДСТАНЕЙ")
    print("=" * 70)
    
    from distances import (
        distance_2d_cartesian, distance_2d_polar,
        distance_3d_cartesian, distance_3d_spherical_chord
    )
    
    # Тест 2D
    print("\n2D: Порівняння відстаней у декартовій та полярній системах")
    c1 = CartesianPoint2D(1, 2)
    c2 = CartesianPoint2D(4, 6)
    p1 = PolarPoint.from_cartesian(c1)
    p2 = PolarPoint.from_cartesian(c2)
    
    dist_cart = distance_2d_cartesian(c1, c2)
    dist_polar = distance_2d_polar(p1, p2)
    
    print(f"  Точка 1: {c1}")
    print(f"  Точка 2: {c2}")
    print(f"  Відстань (декартова): {dist_cart:.6f}")
    print(f"  Відстань (полярна):   {dist_polar:.6f}")
    print(f"  Різниця: {abs(dist_cart - dist_polar):.2e}")
    
    if abs(dist_cart - dist_polar) < 1e-10:
        print("  ✓ Відстані СПІВПАДАЮТЬ")
    else:
        print("  ✗ Відстані НЕ СПІВПАДАЮТЬ")
    
    # Тест 3D
    print("\n3D: Порівняння відстаней у декартовій та сферичній системах")
    c3d_1 = CartesianPoint3D(1, 2, 3)
    c3d_2 = CartesianPoint3D(4, 5, 6)
    s1 = SphericalPoint.from_cartesian(c3d_1)
    s2 = SphericalPoint.from_cartesian(c3d_2)
    
    dist_cart_3d = distance_3d_cartesian(c3d_1, c3d_2)
    dist_spher_chord = distance_3d_spherical_chord(s1, s2)
    
    print(f"  Точка 1: {c3d_1}")
    print(f"  Точка 2: {c3d_2}")
    print(f"  Відстань (декартова):      {dist_cart_3d:.6f}")
    print(f"  Відстань (сферична-хорда): {dist_spher_chord:.6f}")
    print(f"  Різниця: {abs(dist_cart_3d - dist_spher_chord):.2e}")
    
    if abs(dist_cart_3d - dist_spher_chord) < 1e-10:
        print("  ✓ Відстані СПІВПАДАЮТЬ")
    else:
        print("  ✗ Відстані НЕ СПІВПАДАЮТЬ")


if __name__ == "__main__":
    test_2d_conversions()
    test_3d_conversions()
    test_distance_equivalence()
    
    print("\n" + "=" * 70)
    print("ТЕСТУВАННЯ ЗАВЕРШЕНО")
    print("=" * 70)
