# Suitability Analysis: Multi-Criteria-Estimation-Analysis
Using MCE to do a suitability analysis with four factors 


# GIS Automation: MCE Suitability Analysis using ArcPy

This repository contains an automated **Multi-Criteria Evaluation (MCE)** model using the ArcPy `WeightedOverlay_sa` tool. This script acts as the final decision-making engine of the spatial analysis pipeline, synthesizing multiple input parameters into a single actionable suitability surface (e.g., identifying optimal locations for free water infrastructure).

## 📊 MCE Weighting Matrix
The model assigns specific percentage influences to five distinct spatial criteria (Totaling 100%). By extracting the raw ArcMap output into a dynamically formatted Python string, the model weights can be easily adjusted by stakeholders without breaking the code syntax.

| Input Raster / Factor | Influence Weight | Remap Scale Strategy |
| :--- | :---: | :--- |
| **Proximity to Schools** | `30%` | Highest priority (0-5 scaling) |
| **Proximity to Dormitories** | `25%` | High priority (0-5 scaling) |
| **Proximity to Roads** | `25%` | High priority (0-5 scaling) |
| **Land Use/Land Cover (LULC)** | `15%` | Binary reclassification (0 or 5) |
| **Kernel Density** | `5%` | Lowest priority (Flat scale of 1) |

*Note: The model utilizes a standard evaluation scale from 1 to 9, with NODATA areas explicitly masked out to prevent false suitability scoring.*

## 🚀 How to Use
1. Clone this repository to your local machine.
2. Ensure you have an active **ArcGIS Spatial Analyst** extension license.
3. Populate the `Data/MCE_Inputs.gdb` with your pre-processed and reclassified rasters.
4. Run the script via your ArcGIS Python environment:
   ```bash
   python 03_mce_suitability_analysis.py
