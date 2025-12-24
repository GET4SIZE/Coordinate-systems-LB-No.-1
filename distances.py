"""
Функції для обчислення відстаней між точками
у різних системах координат
"""

import math
from coordinate_systems import (
    CartesianPoint2D, PolarPoint,
    CartesianPoint3D, SphericalPoint
)


def distance_2d_cartesian(p1: CartesianPoint2D, p2: CartesianPoint2D) -> float:
    """
    Евклідова відстань між двома точками у декартовій системі 2D
    d = √((x₂ - x₁)² + (y₂ - y₁)²)
    """
    return math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)


def distance_2d_polar(p1: PolarPoint, p2: PolarPoint) -> float:
    """
    Відстань між двома точками у полярній системі координат
    Використовує теорему косинусів:
    d = √(r₁² + r₂² - 2·r₁·r₂·cos(θ₂ - θ₁))
    """
    return math.sqrt(
        p1.radius**2 + 
        p2.radius**2 - 
        2 * p1.radius * p2.radius * math.cos(p2.angle - p1.angle)
    )


def distance_3d_cartesian(p1: CartesianPoint3D, p2: CartesianPoint3D) -> float:
    """
    Евклідова відстань між двома точками у декартовій системі 3D
    d = √((x₂ - x₁)² + (y₂ - y₁)² + (z₂ - z₁)²)
    """
    return math.sqrt(
        (p2.x - p1.x)**2 + 
        (p2.y - p1.y)**2 + 
        (p2.z - p1.z)**2
    )


def distance_3d_spherical_chord(p1: SphericalPoint, p2: SphericalPoint) -> float:
    """
    Пряма відстань (хорда) між двома точками у сферичній системі координат
    Застосовується для точок з різними радіусами
    
    d = √(ρ₁² + ρ₂² - 2·ρ₁·ρ₂·[sin(φ₁)·sin(φ₂)·cos(θ₂ - θ₁) + cos(φ₁)·cos(φ₂)])
    """
    cos_angle_diff = math.cos(p2.azimuth - p1.azimuth)
    
    term = (math.sin(p1.polar_angle) * math.sin(p2.polar_angle) * cos_angle_diff +
            math.cos(p1.polar_angle) * math.cos(p2.polar_angle))
    
    return math.sqrt(
        p1.radius**2 + 
        p2.radius**2 - 
        2 * p1.radius * p2.radius * term
    )


def distance_3d_spherical_arc(p1: SphericalPoint, p2: SphericalPoint) -> float:
    """
    Дугова відстань (по поверхні сфери) між двома точками
    Використовує формулу великого кола (haversine-подібна)
    
    Умова: p1.radius == p2.radius (точки на одній сфері)
    
    d = R · arccos(sin(φ₁)·sin(φ₂)·cos(θ₂ - θ₁) + cos(φ₁)·cos(φ₂))
    """
    # Використовуємо середнє значення радіусів для підвищення точності
    radius = (p1.radius + p2.radius) / 2
    
    cos_angle_diff = math.cos(p2.azimuth - p1.azimuth)
    
    cos_arc = (math.sin(p1.polar_angle) * math.sin(p2.polar_angle) * cos_angle_diff +
               math.cos(p1.polar_angle) * math.cos(p2.polar_angle))
    
    # Обмежуємо значення для уникнення помилок округлення
    cos_arc = max(-1, min(1, cos_arc))
    
    return radius * math.acos(cos_arc)
