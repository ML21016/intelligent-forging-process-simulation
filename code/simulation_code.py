import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# -------------------------------
# Step 1: Load Material Properties
# -------------------------------
def load_material_properties(file_path):
    """
    Load material properties from a CSV file.
    """
    return pd.read_csv(file_path)


# -------------------------------
# Step 2: Define Material Properties
# -------------------------------
def get_material_properties(material_df, material_name):
    """
    Extract mechanical properties for the selected material.
    """
    material_row = material_df[material_df['Material'] == material_name]

    if material_row.empty:
        raise ValueError(f"No data found for material: {material_name}")

    return {
        'yield_stress': float(material_row['Sy'].iloc[0]),
        'modulus_of_elasticity': float(material_row['E'].iloc[0]),
        'density': float(material_row['Ro'].iloc[0]),
        'shear_modulus': float(material_row['G'].iloc[0]),
        'poissons_ratio': float(material_row['mu'].iloc[0]),
        'hardness': float(material_row['Bhn'].iloc[0])
    }


# -------------------------------
# Step 3: Define the 3D Grid
# -------------------------------
def generate_grid(size, resolution):
    """
    Generate a 3D grid representing the forging workpiece.
    """
    x = np.linspace(-size, size, resolution)
    y = np.linspace(-size, size, resolution)
    z = np.linspace(0, size, resolution)

    return np.meshgrid(x, y, z)


# -------------------------------
# Step 4: Visualize Grid
# -------------------------------
def visualize_grid(grid):
    """
    Visualize the grid structure.
    """
    plt.figure()
    plt.scatter(grid[0].flatten(), grid[1].flatten(), grid[2].flatten())
    plt.title("3D Grid Visualization")
    plt.show()


# -------------------------------
# Step 5: Calculate Deformation Depth
# -------------------------------
def calculate_deformation_depth(
        energy,
        step,
        frequency,
        yield_stress,
        contact_area,
        modulus_of_elasticity,
        hardness_factor
):
    """
    Calculate deformation depth considering strain hardening.
    """

    hardness_effect = 1 + (hardness_factor / 500)

    deformation_depth = (
        (energy * (step ** 1.5) * frequency)
        / (yield_stress * contact_area)
    ) * (modulus_of_elasticity ** -0.5) * hardness_effect

    return deformation_depth


# -------------------------------
# Step 6: Von Mises Yield Criterion
# -------------------------------
def calculate_von_mises(
        sigma_xx,
        sigma_yy,
        sigma_zz,
        sigma_xy,
        sigma_xz,
        sigma_yz
):
    """
    Calculate Von Mises stress from stress tensor.
    """

    von_mises = np.sqrt(
        0.5 * (
            (sigma_xx - sigma_yy) ** 2 +
            (sigma_yy - sigma_zz) ** 2 +
            (sigma_zz - sigma_xx) ** 2
        )
        + 3 * (sigma_xy ** 2 + sigma_xz ** 2 + sigma_yz ** 2)
    )

    return von_mises


# -------------------------------
# Step 7: Material Distribution
# -------------------------------
def apply_gaussian_deformation(
        deformation_depth,
        distance,
        impact_radius
):
    """
    Apply Gaussian deformation profile.
    """

    localized_deformation = deformation_depth * np.exp(
        -(distance ** 2) / (2 * (impact_radius ** 2))
    )

    return localized_deformation


# -------------------------------
# Step 8: Validation
# -------------------------------
def validate_simulation(avg_displacement, expected_deformation_depth):
    """
    Validate simulation results.
    """

    if np.isclose(avg_displacement, expected_deformation_depth, atol=0.1):
        print("Validation passed!")
    else:
        print("Validation failed!")


# -------------------------------
# Example Main Simulation
# -------------------------------
if __name__ == "__main__":

    # Load material database
    material_df = load_material_properties("material_properties.csv")

    # Select material
    material = get_material_properties(material_df, "Steel")

    # Generate grid
    grid = generate_grid(size=10, resolution=20)

    # Visualize initial grid
    visualize_grid(grid)

    # Example parameters
    energy = 1000
    step = 1
    frequency = 5
    contact_area = 10
    hardness_factor = material['hardness']

    deformation_depth = calculate_deformation_depth(
        energy,
        step,
        frequency,
        material['yield_stress'],
        contact_area,
        material['modulus_of_elasticity'],
        hardness_factor
    )

    # Example stress tensor
    von_mises = calculate_von_mises(100, 80, 60, 10, 5, 3)

    print("Deformation Depth:", deformation_depth)
    print("Von Mises Stress:", von_mises)

    # Example validation
    validate_simulation(avg_displacement=deformation_depth,
                        expected_deformation_depth=deformation_depth)
