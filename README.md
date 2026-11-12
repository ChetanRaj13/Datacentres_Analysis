# India AI Data Centre Sustainability Dashboard

**TISS Dissertation Project (Analytics & Sustainability Studies)**  
*Evaluating the Environmental Constraints of India's AI Infrastructure Boom.*

An interactive geospatial and analytical dashboard evaluating the spatial collision between 118 hyperscale/colocation data centres and district-level groundwater stress budgets from the Central Ground Water Board (CGWB 2025).

---

## Live Demo
Access the live dashboard here:
👉 **`https://<your-username>.github.io/<your-repo-name>/`**

---

## Key Features
- **Map Explorer:** Interactive nationwide choropleth across 643 districts of India based on CGWB 2025 Dynamic Groundwater Extraction rates.
- **118 Tracked Campuses:** Precise marker sizing by IT load capacity (MW), with distinction between verified ground coordinates and centroid approximations.
- **Dynamic Filtering:** Search by facility/operator/district, filter by State, CGWB stress category, and verified coordinate precision.
- **Summary Analytics:** 10 KPI summary cards and 9 analytical charts powered by Chart.js (State distributions, MW pipeline vs. live load, domestic tap water vulnerability via Jal Jeevan Mission, urban tier concentration, and groundwater stress rankings).

---

## Tech Stack
- Vanilla HTML5 / CSS3 / JavaScript (ES6+)
- [Leaflet.js](https://leafletjs.com/) for GIS mapping
- [Chart.js](https://www.chartjs.org/) for data visualizations
- Zero build tools or frameworks required — run locally by opening `index.html` or host via GitHub Pages.

