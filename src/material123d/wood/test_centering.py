#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify that cuts are properly centered at origin
"""

import trimesh
import numpy as np
from pathlib import Path
from rich import print
from advanced_grain_cutter import AdvancedGrainCutter, Parameters

def test_centering():
    """Test that all cuts are properly centered at origin"""
    
    print("[blue]Testing cut centering functionality...[/blue]")
    
    # Initialize cutter
    P = Parameters()
    P.do_export = False  # Don't export during testing
    cutter = AdvancedGrainCutter(P)
    
    # Get mesh info
    bounds = cutter.working_mesh.bounds
    mesh_center = (bounds[0] + bounds[1]) / 2
    
    print(f"Original mesh center: [{mesh_center[0]:.2f}, {mesh_center[1]:.2f}, {mesh_center[2]:.2f}]")
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Box intersection
    print("\n1. Testing box intersection centering...")
    tests_total += 1
    box_cut = cutter.create_wood_plank_cut(plank_size=(50, 50, 10), plank_center=mesh_center.tolist())
    if box_cut:
        cut_bounds = box_cut.bounds
        cut_center = (cut_bounds[0] + cut_bounds[1]) / 2
        center_distance = np.linalg.norm(cut_center)
        
        print(f"   Cut center: [{cut_center[0]:.3f}, {cut_center[1]:.3f}, {cut_center[2]:.3f}]")
        print(f"   Distance from origin: {center_distance:.3f}")
        
        if center_distance < 0.001:  # Very close to origin (accounting for floating point precision)
            print("   [green]✓ Box cut properly centered at origin[/green]")
            tests_passed += 1
        else:
            print("   [red]✗ Box cut not centered at origin[/red]")
    else:
        print("   [yellow]⚠ Box cut failed[/yellow]")
    
    # Test 2: Cylindrical cut
    print("\n2. Testing cylindrical cut centering...")
    tests_total += 1
    cylinder_cut = cutter.create_cylindrical_cut(center=mesh_center.tolist(), radius=10, height=20)
    if cylinder_cut:
        cut_bounds = cylinder_cut.bounds
        cut_center = (cut_bounds[0] + cut_bounds[1]) / 2
        center_distance = np.linalg.norm(cut_center)
        
        print(f"   Cut center: [{cut_center[0]:.3f}, {cut_center[1]:.3f}, {cut_center[2]:.3f}]")
        print(f"   Distance from origin: {center_distance:.3f}")
        
        if center_distance < 0.001:
            print("   [green]✓ Cylindrical cut properly centered at origin[/green]")
            tests_passed += 1
        else:
            print("   [red]✗ Cylindrical cut not centered at origin[/red]")
    else:
        print("   [yellow]⚠ Cylindrical cut failed[/yellow]")
    
    # Test 3: Spherical cut
    print("\n3. Testing spherical cut centering...")
    tests_total += 1
    sphere_cut = cutter.create_spherical_cut(center=mesh_center.tolist(), radius=15)
    if sphere_cut:
        cut_bounds = sphere_cut.bounds
        cut_center = (cut_bounds[0] + cut_bounds[1]) / 2
        center_distance = np.linalg.norm(cut_center)
        
        print(f"   Cut center: [{cut_center[0]:.3f}, {cut_center[1]:.3f}, {cut_center[2]:.3f}]")
        print(f"   Distance from origin: {center_distance:.3f}")
        
        if center_distance < 0.001:
            print("   [green]✓ Spherical cut properly centered at origin[/green]")
            tests_passed += 1
        else:
            print("   [red]✗ Spherical cut not centered at origin[/red]")
    else:
        print("   [yellow]⚠ Spherical cut failed[/yellow]")
    
    # Test 4: Planar cut
    print("\n4. Testing planar cut centering...")
    tests_total += 1
    z_mid = mesh_center[2]
    planar_cut = cutter.create_planar_cut(
        plane_origin=(0, 0, z_mid),
        plane_normal=(0, 0, 1),
        keep_positive=True
    )
    if planar_cut:
        cut_bounds = planar_cut.bounds
        cut_center = (cut_bounds[0] + cut_bounds[1]) / 2
        center_distance = np.linalg.norm(cut_center)
        
        print(f"   Cut center: [{cut_center[0]:.3f}, {cut_center[1]:.3f}, {cut_center[2]:.3f}]")
        print(f"   Distance from origin: {center_distance:.3f}")
        
        if center_distance < 0.001:
            print("   [green]✓ Planar cut properly centered at origin[/green]")
            tests_passed += 1
        else:
            print("   [red]✗ Planar cut not centered at origin[/red]")
    else:
        print("   [yellow]⚠ Planar cut failed[/yellow]")
    
    # Summary
    print(f"\n[blue]Test Results: {tests_passed}/{tests_total} tests passed[/blue]")
    
    if tests_passed == tests_total:
        print("[green]🎉 All cuts are properly centered at origin![/green]")
    else:
        print(f"[yellow]⚠ {tests_total - tests_passed} test(s) failed[/yellow]")
    
    return tests_passed == tests_total

if __name__ == "__main__":
    success = test_centering()
    exit(0 if success else 1)
