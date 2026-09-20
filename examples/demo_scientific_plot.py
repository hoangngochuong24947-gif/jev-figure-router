#!/usr/bin/env python3
"""
demo_scientific_plot.py — Nature-style publication plot generator
=============================================================================
Demonstrates how figure-router's 'scientific_plots' branch renders deterministic,
publication-ready vector figures using Matplotlib and SciencePlots styles.

Usage:
    python3 examples/demo_scientific_plot.py
Output:
    examples/nature_publication_demo.pdf
    examples/nature_publication_demo.png
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

def generate_nature_plot(output_pdf: str = "examples/nature_publication_demo.pdf",
                         output_png: str = "examples/nature_publication_demo.png"):
    print(">>> Initializing publication plot settings...")

    # Configure publication-grade styling
    try:
        import scienceplots
        plt.style.use(['science', 'nature'])
        print("[+] Applied scienceplots 'nature' theme successfully.")
    except Exception:
        print("[!] scienceplots not found, falling back to clean modern aesthetics.")
        plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
        plt.rcParams.update({
            'font.family': 'sans-serif',
            'font.size': 8,
            'axes.labelsize': 8,
            'xtick.labelsize': 7,
            'ytick.labelsize': 7,
            'legend.fontsize': 7,
            'figure.titlesize': 9,
            'lines.linewidth': 1.2,
        })

    # Nature standard double-panel width: 89mm (single column ~ 3.5 inches) or 183mm (double column)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.8, 2.6), dpi=300)

    # Panel A: Phonon Dispersion / Band Structure Simulation
    x = np.linspace(0, 4 * np.pi, 200)
    acoustic_mode = np.abs(np.sin(x / 4)) * 15
    optical_mode_1 = 20 + 3 * np.cos(x / 2)
    optical_mode_2 = 26 + 2 * np.sin(x / 3)

    ax1.plot(x, acoustic_mode, label=r'Acoustic ($\mathrm{LA}$)', color='#0072B2', lw=1.5)
    ax1.plot(x, optical_mode_1, label=r'Optical ($\mathrm{TO}_1$)', color='#D55E00', lw=1.5)
    ax1.plot(x, optical_mode_2, label=r'Optical ($\mathrm{LO}$)', color='#009E73', lw=1.5)

    ax1.set_xticks([0, np.pi, 2 * np.pi, 3 * np.pi, 4 * np.pi])
    ax1.set_xticklabels([r'$\Gamma$', r'$X$', r'$M$', r'$R$', r'$\Gamma$'])
    ax1.set_ylabel(r'Frequency $\omega$ ($\mathrm{THz}$)')
    ax1.set_xlabel('High-Symmetry Path')
    ax1.set_title(r'\textbf{a} Phonon Dispersion', loc='left', fontsize=8, fontweight='bold')
    ax1.legend(frameon=True, facecolor='white', framealpha=0.9, edgecolor='none', loc='upper right')
    ax1.grid(True, linestyle=':', alpha=0.6)

    # Panel B: Density of States (DOS)
    energies = np.linspace(0, 30, 200)
    dos_acoustic = np.exp(-((energies - 10)**2) / 12) * 4.2
    dos_optical = np.exp(-((energies - 22)**2) / 8) * 6.5 + np.exp(-((energies - 27)**2) / 5) * 5.0
    total_dos = dos_acoustic + dos_optical

    ax2.fill_betweenx(energies, 0, total_dos, color='#56B4E9', alpha=0.4, label='Total DOS')
    ax2.plot(total_dos, energies, color='#0072B2', lw=1.2)
    ax2.set_xlabel(r'Phonon DOS (states/$\mathrm{THz}$)')
    ax2.set_ylabel(r'Frequency $\omega$ ($\mathrm{THz}$)')
    ax2.set_title(r'\textbf{b} Projected Density of States', loc='left', fontsize=8, fontweight='bold')
    ax2.legend(frameon=True, facecolor='white', framealpha=0.9, edgecolor='none', loc='upper right')
    ax2.grid(True, linestyle=':', alpha=0.6)

    plt.tight_layout()

    # Save to publication vector formats
    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)
    fig.savefig(output_pdf, format='pdf', bbox_inches='tight')
    fig.savefig(output_png, format='png', dpi=300, bbox_inches='tight')
    plt.close(fig)

    print(f"[✓] Publication Vector PDF generated: {output_pdf}")
    print(f"[✓] High-Res Preview PNG generated   : {output_png}")

if __name__ == "__main__":
    generate_nature_plot()
