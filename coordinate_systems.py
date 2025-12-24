"""
Лабораторна робота №1: Програмні моделі систем координат
Імутабельні класи для представлення точок у різних системах координат
"""

from dataclasses import dataclass
from typing import Tuple
import math


@dataclass(frozen=True)
class CartesianPoint2D:
    """Точка у двовимірній декартовій системі координат"""
    x: float
    y: float
    
    @staticmethod
    def from_polar(polar_point: 'PolarPoint') -> 'CartesianPoint2D':
        """
        Перетворення з полярної системи координат у декартову
        x = r * cos(θ)
        y = r * sin(θ)
        """
        x = polar_point.radius * math.cos(polar_point.angle)
        y = polar_point.radius * math.sin(polar_point.angle)
        return CartesianPoint2D(x, y)
    
    def __repr__(self) -> str:
        return f"CartesianPoint2D(x={self.x:.4f}, y={self.y:.4f})"


@dataclass(frozen=True)
class PolarPoint:
    """Точка у полярній системі координат"""
    radius: float  # r - відстань від початку координат
    angle: float   # θ (theta) - кут у радіанах
    
    @staticmethod
    def from_cartesian(cartesian_point: 'CartesianPoint2D') -> 'PolarPoint':
        """
        Перетворення з декартової системи координат у полярну
        r = √(x² + y²)
        θ = atan2(y, x)
        """
        radius = math.sqrt(cartesian_point.x**2 + cartesian_point.y**2)
        angle = math.atan2(cartesian_point.y, cartesian_point.x)
        return PolarPoint(radius, angle)
    
    def __repr__(self) -> str:
        return f"PolarPoint(r={self.radius:.4f}, θ={self.angle:.4f} rad)"


@dataclass(frozen=True)
class CartesianPoint3D:
    """Точка у тривимірній декартовій системі координат"""
    x: float
    y: float
    z: float
    
    @staticmethod
    def from_spherical(spherical_point: 'SphericalPoint') -> 'CartesianPoint3D':
        """
        Перетворення зі сферичної системи координат у декартову
        x = ρ * sin(φ) * cos(θ)
        y = ρ * sin(φ) * sin(θ)
        z = ρ * cos(φ)
        """
        x = (spherical_point.radius * 
             math.sin(spherical_point.polar_angle) * 
             math.cos(spherical_point.azimuth))
        y = (spherical_point.radius * 
             math.sin(spherical_point.polar_angle) * 
             math.sin(spherical_point.azimuth))
        z = spherical_point.radius * math.cos(spherical_point.polar_angle)
        return CartesianPoint3D(x, y, z)
    
    def __repr__(self) -> str:
        return f"CartesianPoint3D(x={self.x:.4f}, y={self.y:.4f}, z={self.z:.4f})"


@dataclass(frozen=True)
class SphericalPoint:
    """Точка у сферичній системі координат"""
    radius: float        # ρ (rho) - відстань від початку координат
    azimuth: float       # θ (theta) - азимутальний кут у радіанах
    polar_angle: float   # φ (phi) - полярний кут у радіанах
    
    @staticmethod
    def from_cartesian(cartesian_point: 'CartesianPoint3D') -> 'SphericalPoint':
        """
        Перетворення з декартової системи координат у сферичну
        ρ = √(x² + y² + z²)
        θ = atan2(y, x)
        φ = acos(z / ρ)
        """
        radius = math.sqrt(
            cartesian_point.x**2 + 
            cartesian_point.y**2 + 
            cartesian_point.z**2
        )
        azimuth = math.atan2(cartesian_point.y, cartesian_point.x)
        
        # Уникаємо ділення на нуль
        if radius == 0:
            polar_angle = 0
        else:
            polar_angle = math.acos(cartesian_point.z / radius)
        
        return SphericalPoint(radius, azimuth, polar_angle)
    
    def __repr__(self) -> str:
        return (f"SphericalPoint(ρ={self.radius:.4f}, "
                f"θ={self.azimuth:.4f} rad, φ={self.polar_angle:.4f} rad)")
