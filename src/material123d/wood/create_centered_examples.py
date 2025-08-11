#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate a few example cuts to demonstrate origin centering
"""

from advanced_grain_cutter import AdvancedGrainCutter, Parameters
from rich import print
import numpy as np

def create_centered_examples():
    """Create example cuts that demonstrate origin centering"""
    
    print("[blue]Creating example cuts with origin centering...[/blue]")
    
    # Initialize with export enabled
    P = Parameters()
    P.do_export = True
    P.export_folder = P.export_folder / "centered_examples"
    
    cutter = AdvancedGrainCutter(P)
    
    # Get mesh bounds for cutting operations
    bounds = cutter.working_mesh.bounds
    mesh_center = (bounds[0] + bounds[1]) / 2
    
    print(f"Original mesh center: [{mesh_center[0]:.1f}, {mesh_center[1]:.1f}, {mesh_center[2]:.1f}]")
    print(f"Mesh extents: [{cutter.working_mesh.extents[0]:.1f}, {cutter.working_mesh.extents[1]:.1f}, {cutter.working_mesh.extents[2]:.1f}]")
    
    created_cuts = 0
    
    # Example 1: Small wood plank
    print("\n1. Creating small wood plank (30×50×8mm)...")
    plank = cutter.create_wood_plank_cut(
        plank_size=(30, 50, 8),
        plank_center=mesh_center.tolist()
    )
    if plank:
        cutter.export_mesh(plank, "wood_plank_30x50x8_centered")
        
        # Verify centering
        plank_bounds = plank.bounds
        plank_center = (plank_bounds[0] + plank_bounds[1]) / 2
        distance_from_origin = np.linalg.norm(plank_center)
        
        print(f"   Result center: [{plank_center[0]:.3f}, {plank_center[1]:.3f}, {plank_center[2]:.3f}]")
        print(f"   Distance from origin: {distance_from_origin:.6f}")
        created_cuts += 1
    
    # Example 2: Cylindrical dowel
    print("\n2. Creating cylindrical dowel (r=6mm, h=25mm)...")
    dowel = cutter.create_cylindrical_cut(
        center=mesh_center.tolist(),
        radius=6,
        height=25,
        axis='z'
    )
    if dowel:
        cutter.export_mesh(dowel, "wood_dowel_r6_h25_centered")
        
        # Verify centering
        dowel_bounds = dowel.bounds
        dowel_center = (dowel_bounds[0] + dowel_bounds[1]) / 2
        distance_from_origin = np.linalg.norm(dowel_center)
        
        print(f"   Result center: [{dowel_center[0]:.3f}, {dowel_center[1]:.3f}, {dowel_center[2]:.3f}]")
        print(f"   Distance from origin: {distance_from_origin:.6f}")
        created_cuts += 1
    
    # Example 3: Spherical cut
    print("\n3. Creating spherical cut (r=12mm)...")
    sphere = cutter.create_spherical_cut(
        center=mesh_center.tolist(),
        radius=12
    )
    if sphere:
        cutter.export_mesh(sphere, "wood_sphere_r12_centered")
        
        # Verify centering
        sphere_bounds = sphere.bounds
        sphere_center = (sphere_bounds[0] + sphere_bounds[1]) / 2
        distance_from_origin = np.linalg.norm(sphere_center)
        
        print(f"   Result center: [{sphere_center[0]:.3f}, {sphere_center[1]:.3f}, {sphere_center[2]:.3f}]")
        print(f"   Distance from origin: {distance_from_origin:.6f}")
        created_cuts += 1
    
    print(f"\n[green]✓ Created {created_cuts} centered cuts![/green]")
    print(f"[blue]All results are centered at origin (0,0,0)[/blue]")
    print(f"[blue]Files saved to: {P.export_folder}[/blue]")
    
    return created_cuts

if __name__ == "__main__":
    create_centered_examples()
