"""
Script Name: 03_mce_suitability_analysis.py
Description: Executes a Multi-Criteria Evaluation (MCE) using the Weighted 
             Overlay tool to identify highly suitable areas (e.g., for water infrastructure).
"""

import os
import arcpy

def check_spatial_license():
    """Validates and securely checks out the ArcGIS Spatial Analyst extension."""
    if arcpy.CheckExtension("Spatial") == "Available":
        arcpy.CheckOutExtension("Spatial")
        arcpy.AddMessage("Spatial Analyst extension checked out successfully.")
    else:
        raise arcpy.ExecuteError("Spatial Analyst license is unavailable. Execution halted.")

def run_suitability_model(output_raster, workspace):
    """Constructs the Weighted Overlay table and executes the MCE model."""
    try:
        check_spatial_license()
        arcpy.env.overwriteOutput = True
        arcpy.env.workspace = workspace

        arcpy.AddMessage("Building Multi-Criteria Evaluation (MCE) model...")

        # 1. Define input rasters (Assuming they are in the active workspace)
        kd_raster = "Kernel_Density"
        lulc_raster = "Reclass_LULC"
        school_raster = "Reclass_School"
        dorm_raster = "Reclass_Dormitories"
        road_raster = "Reclass_Road"

        # 2. Construct the Weighted Overlay Table dynamically using f-strings
        # Syntax: ('Raster' Weight% 'Field' (Old Value New Value;...); ...)
        # Weights must equal exactly 100%
        overlay_table = (
            f"('{kd_raster}' 5 'VALUE' (1 1; 2 1; 3 1; NODATA NODATA); "
            f"'{lulc_raster}' 15 'VALUE' (0 1; 5 5; NODATA NODATA); "
            f"'{school_raster}' 30 'VALUE' (0 1; 1 1; 2 2; 3 3; 4 4; 5 5; NODATA NODATA); "
            f"'{dorm_raster}' 25 'VALUE' (0 1; 1 1; 2 2; 3 3; 4 4; 5 5; NODATA NODATA); "
            f"'{road_raster}' 25 'VALUE' (0 1; 1 1; 2 2; 3 3; 4 4; 5 5; NODATA NODATA))"
        )
        
        # Define evaluation scale (1 to 9, step of 1)
        evaluation_scale = "1 9 1"
        
        # Combine into the final tool parameter format
        full_wo_parameter = f"{overlay_table}; {evaluation_scale}"

        # 3. Execute Geoprocessing
        arcpy.AddMessage("Running Weighted Overlay Spatial Analyst tool...")
        arcpy.gp.WeightedOverlay_sa(full_wo_parameter, output_raster)

        arcpy.AddMessage(f"SUCCESS: Suitability surface saved to {output_raster}")

    except arcpy.ExecuteError:
        arcpy.AddError("ArcPy Geoprocessing Error: " + arcpy.GetMessages(2))
    except Exception as e:
        arcpy.AddError(f"Unexpected Script Error: {str(e)}")
    finally:
        arcpy.CheckInExtension("Spatial")
        arcpy.AddMessage("Spatial Analyst extension checked back in.")

if __name__ == "__main__":
    # Standardize relative paths for reproducible GitHub cloning
    current_directory = os.path.dirname(os.path.abspath(__file__))
    project_workspace = os.path.join(current_directory, "Data", "MCE_Inputs.gdb")
    
    # Ensure output directory exists
    output_dir = os.path.join(current_directory, "Outputs")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Define final output path
    OUTPUT_MCE_RASTER = os.path.join(output_dir, "mce_water_suitability.tif")

    # Execute main workflow
    run_suitability_model(OUTPUT_MCE_RASTER, project_workspace)
