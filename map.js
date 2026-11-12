/**
 * map.js — Interactive Leaflet Map for India AI Data Centre Dashboard
 * Handles nationwide CGWB groundwater choropleth and 118 data centre markers
 */

(function (window) {
  'use strict';

  const MapView = {
    map: null,
    districtsLayer: null,
    markersLayer: null,
    geojsonData: null,
    facilitiesData: [],
    currentMetric: 'planned', // 'planned' or 'live'
    currentTierFilter: 'all', // 'all', 'verified', 'fallback'
    currentStateFilter: 'all',
    currentGWFilter: 'all',
    searchQuery: '',

    // Initialize Map View
    init: function (geojsonData, facilitiesData) {
      this.geojsonData = geojsonData;
      this.facilitiesData = facilitiesData;

      this.createMap();
      this.renderChoropleth();
      this.populateStateFilter();
      this.renderMarkers();
      this.setupEventListeners();

      // Force Leaflet to update its geometry and fit India bounds cleanly
      setTimeout(() => {
        if (this.map) {
          this.map.invalidateSize();
          if (this.districtsLayer && this.districtsLayer.getLayers().length > 0) {
            try {
              this.map.fitBounds(this.districtsLayer.getBounds(), { padding: [30, 30] });
            } catch (err) {}
          }
        }
      }, 120);

      window.addEventListener('resize', () => {
        if (this.map) {
          this.map.invalidateSize();
        }
      });
    },

    // Create Leaflet instance
    createMap: function () {
      const container = document.getElementById('leaflet-map-container');
      if (!container) return;
      const self = this;

      // Centered on India
      this.map = L.map('leaflet-map-container', {
        center: [22.0, 79.5],
        zoom: 5,
        minZoom: 4,
        maxZoom: 14,
        zoomControl: true,
        attributionControl: false
      });

      // No basemap tile layer needed — the 643-feature district choropleth covers all of India.
      // The map container background color shows through for ocean / areas outside India.
      // This eliminates tile loading, CORS/watermark issues, and basemap-choropleth misalignment.

      // Attribution (no basemap attribution needed; just project credit)
      L.control.attribution({ position: 'bottomright' })
        .addAttribution('TISS Dissertation | CGWB 2025 | India District Shapefile')
        .addTo(this.map);

      // Restrict panning to India region so user can't scroll into empty ocean
      this.map.setMaxBounds([[2, 60], [40, 102]]);
      this.map.options.maxBoundsViscosity = 0.9;

      // Dedicated pane for district polygons so all districts render seamlessly in one single layer
      this.map.createPane('districtsPane');
      this.map.getPane('districtsPane').style.zIndex = 400;

      // Dedicated high z-index pane for data centre markers so they always render above polygons
      this.map.createPane('dcMarkersPane');
      this.map.getPane('dcMarkersPane').style.zIndex = 650;

      // No zoomend re-render — L.circleMarker maintains fixed pixel radius at every zoom level
      // natively (unlike L.circle which scales geographically). Removing this prevents the blurry
      // flash caused by Leaflet scaling old SVG during zoom animation before replacement.

      // Create layers
      this.markersLayer = L.layerGroup().addTo(this.map);

      // Close all district tooltips on map drag, zoom, or background click
      this.map.on('movestart zoomstart click', function () {
        if (self.districtsLayer) {
          self.districtsLayer.eachLayer(l => {
            if (l.closeTooltip) l.closeTooltip();
          });
        }
      });

      // Close district tooltips when mouse leaves the map container
      container.addEventListener('mouseleave', function () {
        if (self.districtsLayer) {
          self.districtsLayer.eachLayer(l => {
            if (l.closeTooltip) l.closeTooltip();
          });
        }
      });
    },

    // Color mapper for CGWB 4 categories
    getCategoryColor: function (cat) {
      switch (cat) {
        case 'over_exploited':
          return '#dc2626'; // Deep Red
        case 'critical':
          return '#f97316'; // Orange
        case 'semi_critical':
          return '#f59e0b'; // Amber / Yellow
        case 'safe':
          return '#2b9a66'; // Green
        case 'unassessed':
        default:
          return '#cbd5e1'; // Neutral Slate Gray (Hilly / Unassessed)
      }
    },

    // Render Nationwide Groundwater Choropleth
    renderChoropleth: function () {
      if (!this.geojsonData) return;

      const self = this;

      this.districtsLayer = L.geoJSON(this.geojsonData, {
        pane: 'districtsPane',
        style: function (feature) {
          const props = feature.properties || {};
          const color = props.color || self.getCategoryColor(props.category);

          return {
            fillColor: color,
            weight: 0.8,
            opacity: 0.9,
            color: '#ffffff',
            fillOpacity: 0.68
          };
        },
        onEachFeature: function (feature, layer) {
          const props = feature.properties || {};

          // Hover interaction — clean fill-opacity elevation without dark border artifacts
          layer.on({
            mouseover: function (e) {
              const l = e.target;
              // Keep border color '#ffffff' to prevent dark double-line artifacts with adjacent polygons
              l.setStyle({
                weight: 1.6,
                color: '#ffffff',
                fillOpacity: 0.92
              });
            },
            mouseout: function (e) {
              const l = e.target;
              const p = (l.feature && l.feature.properties) || {};
              if (self.currentGWFilter !== 'all') {
                if (p.category === self.currentGWFilter) {
                  l.setStyle({
                    fillColor: p.color || self.getCategoryColor(p.category),
                    fillOpacity: 0.78,
                    weight: 1.0,
                    color: '#ffffff',
                    opacity: 0.9
                  });
                } else {
                  l.setStyle({
                    fillColor: '#e2e8f0',
                    fillOpacity: 0.35,
                    weight: 0.4,
                    color: '#cbd5e1',
                    opacity: 0.5
                  });
                }
              } else {
                self.districtsLayer.resetStyle(l);
              }
              if (l && l.closeTooltip) {
                l.closeTooltip();
              }
            },
            click: function (e) {
              L.DomEvent.stopPropagation(e);
              if (e.target && e.target.closeTooltip) {
                e.target.closeTooltip();
              }
              self.inspectDistrict(props);
            }
          });

          // Tooltip for quick hover
          const stageStr = props.stage_of_extraction_pct !== null && props.stage_of_extraction_pct !== undefined
            ? `${props.stage_of_extraction_pct}%`
            : 'Hilly / Unassessed (<70%)';

          const hostBadge = props.is_datacenter_host
            ? `<div style="font-size:10px; font-weight:700; color:#ea2804; text-transform:uppercase; margin-top:2px;">Data Centre Host (${props.dc_count} campuses)</div>`
            : '';

          layer.bindTooltip(`
            <div style="font-family:'Inter', sans-serif;">
              <strong style="font-size:13px; font-family:'Bricolage Grotesque', sans-serif;">${props.district}</strong>
              <div style="font-size:11px; color:#666;">${props.state}</div>
              <div style="margin-top:4px; font-size:11px;">Extraction: <strong>${stageStr}</strong></div>
              <div style="font-size:11px; color:${props.color || '#2b9a66'}; font-weight:600;">${props.category_label || 'Safe'}</div>
              ${hostBadge}
            </div>
          `, { sticky: true, opacity: 0.98, className: 'leaflet-custom-tooltip' });
        }
      }).addTo(this.map);

      if (this.districtsLayer && this.districtsLayer.getLayers().length > 0) {
        try {
          this.map.fitBounds(this.districtsLayer.getBounds(), { padding: [30, 30] });
        } catch (e) {}
      }
    },

    // Populate State Filter Options
    populateStateFilter: function () {
      const container = document.getElementById('map-state-options');
      if (!container) return;

      const states = new Set();
      this.facilitiesData.forEach(dc => {
        if (dc.state) states.add(dc.state);
      });

      const sortedStates = Array.from(states).sort();
      container.innerHTML = '<button class="filter-pill-btn active" data-filter-state="all">All States (14)</button>';

      sortedStates.forEach(st => {
        const btn = document.createElement('button');
        btn.className = 'filter-pill-btn';
        btn.setAttribute('data-filter-state', st);
        const count = this.facilitiesData.filter(d => d.state === st).length;
        btn.textContent = `${st} (${count})`;
        container.appendChild(btn);
      });

      const self = this;
      container.querySelectorAll('[data-filter-state]').forEach(btn => {
        btn.addEventListener('click', (e) => {
          e.stopPropagation();
          container.querySelectorAll('[data-filter-state]').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          const st = btn.getAttribute('data-filter-state');
          self.currentStateFilter = st;
          const labelState = document.getElementById('label-state-filter');
          if (labelState) {
            labelState.textContent = st === 'all' ? 'State: All (14)' : `State: ${st}`;
          }
          self.renderMarkers();
        });
      });
    },

    // Calculate marker radius based on capacity (fixed pixel size — no zoom dependency)
    // L.circleMarker natively keeps pixel radius constant across zooms, so no recalculation needed.
    // 10 MW → ~4.7 px | 100 MW → ~7.3 px | 500 MW → ~11.6 px | 1000 MW → ~14.8 px | 2000+ MW → 16 px (capped)
    getMarkerRadius: function (mw) {
      const safeMw = (!mw || mw <= 0) ? 5 : mw;
      const r = Math.sqrt(safeMw) * 0.35 + 3.6;
      return Math.min(Math.max(r, 4), 16);
    },

    // Render Data Centre Markers
    renderMarkers: function () {
      if (!this.markersLayer) return;
      this.markersLayer.clearLayers();

      const self = this;
      let visibleCount = 0;

      // Filter facilities
      const filtered = this.facilitiesData.filter(dc => {
        // 1. Search Query
        if (self.searchQuery) {
          const q = self.searchQuery.toLowerCase();
          const matchName = (dc.facility_name || '').toLowerCase().includes(q);
          const matchOp = (dc.operator || '').toLowerCase().includes(q);
          const matchDist = (dc.district || '').toLowerCase().includes(q);
          const matchState = (dc.state || '').toLowerCase().includes(q);
          if (!matchName && !matchOp && !matchDist && !matchState) return false;
        }

        // 2. State Filter
        if (self.currentStateFilter !== 'all' && dc.state !== self.currentStateFilter) {
          return false;
        }

        // 3. Precision Tier Filter
        if (self.currentTierFilter === 'verified' && dc.is_centroid_fallback) {
          return false;
        }
        if (self.currentTierFilter === 'fallback' && !dc.is_centroid_fallback) {
          return false;
        }

        // 4. Groundwater Category Filter
        if (self.currentGWFilter !== 'all') {
          const distProps = self.getDistrictProperties(dc.state, dc.district);
          const dcCat = dc.gw_category || (distProps ? distProps.category : null);
          if (!dcCat || dcCat !== self.currentGWFilter) {
            return false;
          }
        }

        return true;
      });

      filtered.forEach(dc => {
        if (dc.lat === null || dc.lng === null || dc.lat === undefined || dc.lng === undefined) {
          return;
        }

        visibleCount++;

        // Determine capacity metric
        const mw = self.currentMetric === 'live' ? (dc.operational_mw || 0) : (dc.planned_ultimate_mw || dc.operational_mw || 0);
        const radius = self.getMarkerRadius(mw);

        // Marker Styling depending on verified vs centroid fallback
        const isFallback = dc.is_centroid_fallback;

        let marker;
        if (isFallback) {
          // Hollow / Dashed Marker with center dot (Centroid fallback)
          marker = L.circleMarker([dc.lat, dc.lng], {
            pane: 'dcMarkersPane',
            radius: radius,
            color: '#dc2626',
            weight: 1.5,
            dashArray: '2, 3',
            fillColor: '#ffffff',
            fillOpacity: 0.25
          });

          // Center dot to indicate centroid anchor
          const centerDot = L.circleMarker([dc.lat, dc.lng], {
            pane: 'dcMarkersPane',
            radius: 2.5,
            color: '#dc2626',
            weight: 1,
            fillColor: '#dc2626',
            fillOpacity: 1.0,
            interactive: false
          });
          self.markersLayer.addLayer(centerDot);
        } else {
          // Solid Marker (Verified exact/plot coordinate) with crisp white separation border
          marker = L.circleMarker([dc.lat, dc.lng], {
            pane: 'dcMarkersPane',
            radius: radius,
            color: '#ffffff',
            weight: 1.5,
            fillColor: '#ea2804',
            fillOpacity: 0.82
          });
        }

        // Popup Content
        const popupContent = self.createPopupContent(dc);
        marker.bindPopup(popupContent, {
          closeButton: true,
          offset: [0, -radius]
        });

        // Click on marker also triggers inspector
        marker.on('click', function (e) {
          L.DomEvent.stopPropagation(e);
          if (self.districtsLayer) {
            self.districtsLayer.eachLayer(l => {
              if (l.closeTooltip) l.closeTooltip();
            });
          }
          self.inspectFacility(dc);
        });

        self.markersLayer.addLayer(marker);
      });

      // Update counter UI
      const countEl = document.getElementById('visible-facilities-count');
      if (countEl) {
        countEl.textContent = `${visibleCount} / ${this.facilitiesData.length}`;
      }
      const headerCountEl = document.getElementById('header-map-count');
      if (headerCountEl) {
        headerCountEl.textContent = visibleCount;
      }
    },

    // Create Rich Leaflet Popup
    createPopupContent: function (dc) {
      const liveMW = dc.operational_mw ? `${dc.operational_mw} MW` : '0 MW';
      const plannedMW = dc.planned_ultimate_mw ? `${dc.planned_ultimate_mw} MW` : 'Undisclosed';

      // District groundwater info
      const distProps = this.getDistrictProperties(dc.state, dc.district);
      let gwBadge = '';
      if (distProps) {
        gwBadge = `
          <div style="margin-top:8px; padding-top:6px; border-top:1px dashed var(--hairline); display:flex; justify-content:space-between; align-items:center;">
            <span style="font-size:11px; color:var(--charcoal);">Groundwater:</span>
            <span style="font-size:11px; font-weight:700; color:${distProps.color};">${distProps.category_label || 'Safe'} (${distProps.stage_of_extraction_pct || '<70'}%)</span>
          </div>
        `;
      }

      // Plain words precision explanation
      let confidenceNotice = '';
      if (dc.is_centroid_fallback) {
        confidenceNotice = `
          <div class="popup-confidence-notice fallback">
            <strong>Approximate Location</strong><br>
            Exact site not publicly located; mapped to district centroid (${dc.district || dc.state}).
          </div>
        `;
      } else {
        confidenceNotice = `
          <div class="popup-confidence-notice verified">
            <strong>Verified Location</strong><br>
            Precision: ${dc.precision_tier || 'Exact site'}.
          </div>
        `;
      }

      return `
        <div>
          <div class="popup-facility-name">${dc.facility_name}</div>
          <div class="popup-facility-operator">${dc.operator || 'Undisclosed Operator'}</div>
          <div style="font-size:11px; color:#555; margin-bottom:8px;">
            ${dc.district ? `${dc.district}, ` : ''}${dc.state}
          </div>
          <div class="popup-metrics">
            <div class="popup-metric-item">
              <span class="popup-metric-label">LIVE IT</span>
              <span class="popup-metric-val">${liveMW}</span>
            </div>
            <div class="popup-metric-item" style="border-left:1px solid #ddd; padding-left:10px;">
              <span class="popup-metric-label">PLANNED IT</span>
              <span class="popup-metric-val" style="color:var(--primary);">${plannedMW}</span>
            </div>
          </div>
          ${confidenceNotice}
          ${dc.coordinate_note ? `<div style="font-size:10px; color:#777; margin-top:5px; font-style:italic;">Note: ${dc.coordinate_note}</div>` : ''}
          ${gwBadge}
        </div>
      `;
    },

    // Inspect District in side drawer
    inspectDistrict: function (props) {
      const panel = document.getElementById('map-inspector');
      const title = document.getElementById('inspector-title');
      const subtitle = document.getElementById('inspector-subtitle');
      const content = document.getElementById('inspector-content');

      if (!panel || !title || !content) return;

      title.textContent = props.district;
      subtitle.textContent = `${props.state} · CGWB 2025 Resource Assessment`;

      const stagePct = props.stage_of_extraction_pct !== null && props.stage_of_extraction_pct !== undefined
        ? `${props.stage_of_extraction_pct}%`
        : 'Hilly / Unassessed (<70%)';

      const catBadgeClass = (props.category || 'safe').replace('_', '-');

      // Facilities in this district
      const facilities = this.facilitiesData.filter(dc => {
        return (dc.district && dc.district.toLowerCase() === (props.district || '').toLowerCase()) ||
               (dc.state && dc.state.toLowerCase() === (props.state || '').toLowerCase() && !dc.district && props.is_datacenter_host);
      });

      let facilitiesHtml = '';
      if (facilities.length > 0) {
        facilitiesHtml = `
          <div style="font-family:'Bricolage Grotesque', sans-serif; font-size:14px; font-weight:700; margin-bottom:10px; margin-top:16px;">
            Tracked Data Centres in this District (${facilities.length})
          </div>
          <div class="inspector-facilities-list">
            ${facilities.map(dc => `
              <div class="inspector-facility-item" data-dc-id="${dc.id}">
                <div class="facility-item-name">${dc.facility_name}</div>
                <div class="facility-item-operator">${dc.operator || 'Undisclosed'}</div>
                <div class="facility-item-meta">
                  <span>Live: <strong>${dc.operational_mw || 0} MW</strong></span>
                  <span style="color:var(--primary);">Planned: <strong>${dc.planned_ultimate_mw || 0} MW</strong></span>
                </div>
                <div style="font-size:10px; margin-top:4px; color:${dc.is_centroid_fallback ? 'var(--primary)' : 'var(--gw-safe)'};">
                  ${dc.confidence_badge}
                </div>
              </div>
            `).join('')}
          </div>
        `;
      } else {
        facilitiesHtml = `
          <div style="font-size:12px; color:var(--ash); font-style:italic; margin-top:16px;">
            No hyperscale data centres currently tracked in this district.
          </div>
        `;
      }

      content.innerHTML = `
        <div class="inspector-badge-row">
          <span class="inspector-badge ${catBadgeClass}">${props.category_label || 'Safe'}</span>
          ${props.is_datacenter_host ? `<span class="inspector-badge verified">HOST DISTRICT</span>` : ''}
        </div>

        <div class="inspector-stat-grid">
          <div class="inspector-stat-box highlight">
            <div class="inspector-stat-label">STAGE OF EXTRACTION</div>
            <div class="inspector-stat-value">${stagePct}</div>
          </div>
          <div class="inspector-stat-box">
            <div class="inspector-stat-label">DATA CENTRES</div>
            <div class="inspector-stat-value">${facilities.length}</div>
          </div>
          <div class="inspector-stat-box">
            <div class="inspector-stat-label">LIVE IT CAPACITY</div>
            <div class="inspector-stat-value">${props.dc_live_mw || 0} <span style="font-size:12px;">MW</span></div>
          </div>
          <div class="inspector-stat-box">
            <div class="inspector-stat-label">PLANNED PIPELINE</div>
            <div class="inspector-stat-value" style="color:var(--primary);">${props.dc_planned_mw || 0} <span style="font-size:12px;">MW</span></div>
          </div>
        </div>

        ${props.category === 'over_exploited' ? `
          <div class="inspector-note-box">
            <strong>Critical Sustainability Warning:</strong> This aquifer is already depleted beyond 100% of annual replenishment prior to data centre expansion.
          </div>
        ` : ''}

        ${facilitiesHtml}
      `;

      panel.classList.add('open');

      // Bind facility clicks inside inspector
      content.querySelectorAll('.inspector-facility-item').forEach(item => {
        item.addEventListener('click', (e) => {
          const dcId = item.getAttribute('data-dc-id');
          const targetDc = facilities.find(f => f.id === dcId);
          if (targetDc) {
            MapView.inspectFacility(targetDc);
          }
        });
      });
    },

    // Inspect Facility in side drawer
    inspectFacility: function (dc) {
      const panel = document.getElementById('map-inspector');
      const title = document.getElementById('inspector-title');
      const subtitle = document.getElementById('inspector-subtitle');
      const content = document.getElementById('inspector-content');

      if (!panel || !title || !content) return;

      title.textContent = dc.facility_name;
      subtitle.textContent = `${dc.operator || 'Undisclosed'} · ${dc.district ? `${dc.district}, ` : ''}${dc.state}`;

      const distProps = this.getDistrictProperties(dc.state, dc.district);
      const isFallback = dc.is_centroid_fallback;

      content.innerHTML = `
        <div class="inspector-badge-row">
          <span class="inspector-badge ${isFallback ? 'fallback' : 'verified'}">${dc.confidence_badge}</span>
          ${distProps ? `<span class="inspector-badge ${(distProps.category || 'safe').replace('_', '-')}">${distProps.category_label}</span>` : ''}
        </div>

        <div class="inspector-stat-grid">
          <div class="inspector-stat-box">
            <div class="inspector-stat-label">LIVE IT LOAD</div>
            <div class="inspector-stat-value">${dc.operational_mw ? `${dc.operational_mw} MW` : '0 MW'}</div>
          </div>
          <div class="inspector-stat-box highlight">
            <div class="inspector-stat-label">PLANNED IT LOAD</div>
            <div class="inspector-stat-value">${dc.planned_ultimate_mw ? `${dc.planned_ultimate_mw} MW` : 'Undisclosed'}</div>
          </div>
        </div>

        <div style="background:var(--surface-bone); padding:14px; border-radius:var(--radius-md); font-size:12px; margin-bottom:16px;">
          <div style="margin-bottom:6px;"><strong>Location Precision:</strong> ${dc.confidence_description}</div>
          <div style="margin-bottom:6px;"><strong>Cooling Technology:</strong> ${dc.cooling || 'Liquid / evaporative (standard hyperscale)'}</div>
          <div><strong>District Groundwater Stress:</strong> ${distProps ? `${distProps.stage_of_extraction_pct}% (${distProps.category_label})` : 'Unassessed'}</div>
        </div>

        ${dc.coordinate_note ? `
          <div class="inspector-note-box">
            <strong>Data Note:</strong> ${dc.coordinate_note}
          </div>
        ` : ''}

        <div style="margin-top:20px;">
          <button class="filter-pill-btn active" style="width:100%; padding:10px; text-align:center;" id="btn-zoom-facility">
            Focus on Map
          </button>
        </div>
      `;

      panel.classList.add('open');

      // Zoom button
      const zoomBtn = document.getElementById('btn-zoom-facility');
      if (zoomBtn && dc.lat && dc.lng) {
        zoomBtn.addEventListener('click', () => {
          MapView.map.setView([dc.lat, dc.lng], 10, { animate: true });
        });
      }
    },

    // Helper to get district properties from GeoJSON by state & district
    getDistrictProperties: function (state, district) {
      if (!this.geojsonData || !this.geojsonData.features) return null;
      let sClean = (state || '').toLowerCase().trim();
      let dClean = (district || '').toLowerCase().trim();

      // Spatial & administrative aliases for parent districts in 2011 shapefile
      if (dClean === 'chengalpattu') { dClean = 'kanchipuram'; sClean = 'tamil nadu'; }
      if (dClean === 'anakapalli') { dClean = 'visakhapatnam'; sClean = 'andhra pradesh'; }
      if (sClean === 'telangana' && !dClean) { dClean = 'ranga reddy'; }
      if (sClean === 'andhra pradesh' && !dClean) { dClean = 'visakhapatnam'; }

      const feat = this.geojsonData.features.find(f => {
        const p = f.properties || {};
        const pDist = (p.district || '').toLowerCase().trim();
        const pState = (p.state || '').toLowerCase().trim();
        return (pDist === dClean && pState === sClean) ||
               (pDist === dClean && !sClean) ||
               (p.original_district && p.original_district.toLowerCase().trim() === dClean);
      });

      return feat ? feat.properties : null;
    },

    // Sync choropleth styling with active groundwater filter
    // When a GW filter is active, dim/gray out districts that don't match the selected category
    // so the user clearly sees which districts belong to the filtered band.
    updateChoroplethFilter: function () {
      if (!this.districtsLayer) return;
      const self = this;
      const activeFilter = this.currentGWFilter;

      this.districtsLayer.eachLayer(function (layer) {
        const props = (layer.feature && layer.feature.properties) || {};
        const cat = props.category || 'unassessed';

        if (activeFilter === 'all') {
          // Restore original colors
          self.districtsLayer.resetStyle(layer);
        } else {
          if (cat === activeFilter) {
            // Matching district: full vibrant color
            const color = props.color || self.getCategoryColor(cat);
            layer.setStyle({
              fillColor: color,
              fillOpacity: 0.78,
              weight: 1.0,
              color: '#ffffff',
              opacity: 0.9
            });
          } else {
            // Non-matching district: dim to very faint gray
            layer.setStyle({
              fillColor: '#e2e8f0',
              fillOpacity: 0.35,
              weight: 0.4,
              color: '#cbd5e1',
              opacity: 0.5
            });
          }
        }
      });
    },

    // Setup Event Listeners for Filters
    setupEventListeners: function () {
      const self = this;

      // Close inspector
      const closeBtn = document.getElementById('inspector-close');
      if (closeBtn) {
        closeBtn.addEventListener('click', () => {
          const panel = document.getElementById('map-inspector');
          if (panel) panel.classList.remove('open');
        });
      }

      // Close inspector on map click outside
      if (this.map) {
        this.map.on('click', () => {
          const panel = document.getElementById('map-inspector');
          if (panel) panel.classList.remove('open');
        });
      }

      // Search input
      const searchInput = document.getElementById('map-search-input');
      if (searchInput) {
        searchInput.addEventListener('input', (e) => {
          self.searchQuery = e.target.value.trim();
          self.renderMarkers();
        });
      }

      // Click-to-toggle popover menus for all filter groups (improves touchscreen/trackpad responsiveness)
      document.querySelectorAll('.filter-group').forEach(group => {
        const header = group.querySelector('.filter-group-header');
        if (header) {
          header.addEventListener('click', (e) => {
            e.stopPropagation();
            const isOpen = group.classList.contains('open');
            document.querySelectorAll('.filter-group').forEach(g => g.classList.remove('open'));
            if (!isOpen) group.classList.add('open');
          });
        }
      });

      document.addEventListener('click', () => {
        document.querySelectorAll('.filter-group').forEach(g => g.classList.remove('open'));
      });

      // Precision Tier Pills
      const tierBtns = document.querySelectorAll('[data-filter-tier]');
      const labelTier = document.getElementById('label-tier-filter');
      tierBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
          e.stopPropagation();
          tierBtns.forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          const tier = btn.getAttribute('data-filter-tier');
          self.currentTierFilter = tier;
          if (labelTier) {
            if (tier === 'all') labelTier.textContent = 'Sites: All (118)';
            else if (tier === 'verified') labelTier.textContent = 'Sites: Verified (90)';
            else if (tier === 'fallback') labelTier.textContent = 'Sites: Centroid (28)';
          }
          self.renderMarkers();
        });
      });

      // Capacity Sizing Metric (Planned vs Live)
      const sizePlannedBtn = document.getElementById('btn-size-planned');
      const sizeLiveBtn = document.getElementById('btn-size-live');
      const labelSize = document.getElementById('label-size-filter');
      if (sizePlannedBtn && sizeLiveBtn) {
        sizePlannedBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          sizePlannedBtn.classList.add('active');
          sizeLiveBtn.classList.remove('active');
          self.currentMetric = 'planned';
          if (labelSize) labelSize.textContent = 'Size: Planned MW';
          self.renderMarkers();
        });
        sizeLiveBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          sizeLiveBtn.classList.add('active');
          sizePlannedBtn.classList.remove('active');
          self.currentMetric = 'live';
          if (labelSize) labelSize.textContent = 'Size: Live MW';
          self.renderMarkers();
        });
      }

      // Groundwater Category Filter Pills (No nested HTML select)
      const gwBtns = document.querySelectorAll('[data-filter-gw]');
      const labelGw = document.getElementById('label-gw-filter');
      gwBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
          e.stopPropagation();
          gwBtns.forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          const gw = btn.getAttribute('data-filter-gw');
          self.currentGWFilter = gw;
          if (labelGw) {
            const mapLabels = {
              'all': 'Groundwater: All',
              'over_exploited': 'GW: Over-exploited',
              'critical': 'GW: Critical',
              'semi_critical': 'GW: Semi-critical',
              'safe': 'GW: Safe'
            };
            labelGw.textContent = mapLabels[gw] || 'Groundwater: All';
          }
          self.renderMarkers();
          self.updateChoroplethFilter();
        });
      });

      // Reset All Filters Button
      const resetBtn = document.getElementById('btn-reset-filters');
      if (resetBtn) {
        resetBtn.addEventListener('click', () => {
          self.searchQuery = '';
          self.currentStateFilter = 'all';
          self.currentTierFilter = 'all';
          self.currentGWFilter = 'all';
          self.currentMetric = 'planned';

          // Reset UI form elements
          if (searchInput) searchInput.value = '';

          // Reset State options
          const stateBtns = document.querySelectorAll('[data-filter-state]');
          stateBtns.forEach(b => {
            b.classList.toggle('active', b.getAttribute('data-filter-state') === 'all');
          });
          const labelState = document.getElementById('label-state-filter');
          if (labelState) labelState.textContent = 'State: All (14)';

          // Reset Tier options
          tierBtns.forEach(b => {
            b.classList.toggle('active', b.getAttribute('data-filter-tier') === 'all');
          });
          if (labelTier) labelTier.textContent = 'Sites: All (118)';

          // Reset Sizing metric
          if (sizePlannedBtn) sizePlannedBtn.classList.add('active');
          if (sizeLiveBtn) sizeLiveBtn.classList.remove('active');
          if (labelSize) labelSize.textContent = 'Size: Planned MW';

          // Reset Groundwater options
          gwBtns.forEach(b => {
            b.classList.toggle('active', b.getAttribute('data-filter-gw') === 'all');
          });
          if (labelGw) labelGw.textContent = 'Groundwater: All';

          // Close all open popovers
          document.querySelectorAll('.filter-group').forEach(g => g.classList.remove('open'));

          self.renderMarkers();
          self.updateChoroplethFilter();
        });
      }
    }
  };

  window.MapView = MapView;
})(window);

