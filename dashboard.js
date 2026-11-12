/**
 * dashboard.js — Summary Analytics View for India AI Data Centre Dashboard
 * Renders KPI cards and 7 Chart.js visualizations directly from summary_stats.json,
 * complete with contextual "i" explanation buttons and popovers.
 */

(function (window) {
  'use strict';

  // Comprehensive Dictionary of Rigorous Academic Explanations
  const INFO_EXPLANATIONS = {
    'kpi-campuses': {
      title: 'Data Centre Campuses Tracked',
      tag: 'Inventory Metric',
      whatItMeasures: 'Total count of distinct hyperscale, colocation, and enterprise data centre campuses identified across India (114 major campuses + 4 construction-phase sub-rows).',
      methodology: 'Aggregated through systematic triangulation across Ministry of Environment (MoEFCC) clearances, State Industrial Development Corporation (MIDC, SIPCOT, TSIIC) land registries, EPC contracts, and corporate disclosures. The 4 nested sub-rows capture independent construction phases of mega-campuses (e.g., Yotta D1 & D2).',
      sustainabilitySignificance: 'Provides the empirical baseline inventory. Each campus typically encompasses multiple buildings and substations, multiplying site-specific cooling water withdrawal and localized electrical power demands.'
    },
    'kpi-states': {
      title: 'Host States Covered',
      tag: 'Geographic Scope',
      whatItMeasures: 'Count of Indian states (14) hosting operational or announced data centre infrastructure.',
      methodology: 'Compiled from verified campus locations and formal state government MoU registries across India.',
      sustainabilitySignificance: 'Reveals severe geographic concentration: despite 14 states being represented, over 70% of all facilities and capacity cluster in just 3 coastal states (Maharashtra, Tamil Nadu, Andhra Pradesh) and Telangana, creating intense localized infrastructure bottlenecks.'
    },
    'kpi-districts': {
      title: 'Hosting Districts Covered',
      tag: 'Hydrological Unit',
      whatItMeasures: 'The 31 administrative districts containing tracked data centre campuses (29 primary hosting districts + 2 adjacent CGWB reporting units).',
      methodology: 'Geospatially resolved to 2011/2022 Census boundaries and matched against Central Ground Water Board (CGWB) assessment units.',
      sustainabilitySignificance: 'The core administrative unit for sustainability analysis. Water stress, municipal supply quotas, and DISCOM power substations are managed and stressed at the district level.'
    },
    'kpi-live-it': {
      title: 'Live IT Load Capacity',
      tag: 'Operational Energy',
      whatItMeasures: 'Current energized electrical power dedicated strictly to IT compute servers, storage arrays, and network hardware (1,380.5 MW).',
      methodology: 'Verified from operational commissioning filings, utility power off-take agreements, and operator disclosures. Expressed in Megawatts (MW) on a pure IT load basis (excluding chiller/cooling auxiliary overhead).',
      sustainabilitySignificance: 'Represents immediate, continuous 24/7/365 baseload electrical power draw. Unlike commercial buildings, data centres operate at flat >85% capacity factors, requiring uninterrupted power and continuous thermal rejection.'
    },
    'kpi-planned-it': {
      title: 'Planned IT Load Pipeline',
      tag: 'Pipeline Surge',
      whatItMeasures: 'Announced ultimate IT compute capacity under active construction, site engineering, or formal state MoUs (9,362.9 MW).',
      methodology: 'Compiled from state investment summit MoUs, Environmental Impact Assessments (EIA), and corporate investor presentations.',
      sustainabilitySignificance: 'Demonstrates an impending ~6.8x surge over live capacity. When energized, this massive expansion will multiply host district water consumption by billions of litres annually if conventional evaporative cooling is deployed.'
    },
    'kpi-live-facility': {
      title: 'Live Facility / Grid Load',
      tag: 'Substation Ingress',
      whatItMeasures: 'Total operational substation-level grid power drawn for the subset of facilities reporting on a total facility load basis (37.0 MW).',
      methodology: 'Facility load includes IT server compute PLUS all auxiliary power overhead (chillers, cooling towers, UPS conversion losses, transformers, lighting).',
      sustainabilitySignificance: 'Methodological integrity rule: Facility load and pure IT load use different engineering boundaries and must never be summed together. They are kept as distinct totals throughout this dissertation.'
    },
    'kpi-planned-facility': {
      title: 'Planned Facility / Grid Pipeline',
      tag: 'Grid Pipeline',
      whatItMeasures: 'Total announced substation interconnect capacity across mega-parks reporting on a facility load basis (9,141.0 MW; e.g. Adani ConneX and Reliance giga-campuses).',
      methodology: 'Sourced from state electricity transmission corporation (TRANSCO) substation applications and high-voltage grid feeder sanctions.',
      sustainabilitySignificance: 'Signals colossal transmission demands. Absorbing multi-gigawatt loads in concentrated industrial corridors places unprecedented stress on regional DISCOM transformers and renewable energy wheeling.'
    },
    'kpi-verified-sites': {
      title: 'Sites with Verified Ground Truth',
      tag: 'Geospatial Rigor',
      whatItMeasures: 'The proportion (90 of 118 campuses, or 76.3%) whose physical ground location has been pinpointed to exact cadastral boundaries or industrial parks.',
      methodology: 'Each facility was individually cross-referenced against satellite imagery, operator codes, building permits, and land registries before acceptance.',
      sustainabilitySignificance: 'Prevents spatial hallucination. The 28 unlocated facilities are assigned district centroids and visually marked with hollow dashed rings to maintain complete honesty about empirical ground truth vs. approximations.'
    },
    'kpi-overexploited-districts': {
      title: 'Districts Over-Exploited for Groundwater',
      tag: 'Ecological Threshold',
      whatItMeasures: '8 out of 30 analyzed hosting districts already extract groundwater faster than annual natural recharge (>100% extraction stage).',
      methodology: 'Official regulatory classification from the Central Ground Water Board (CGWB) 2025 National Compilation on Dynamic Ground Water Resources of India.',
      sustainabilitySignificance: 'The core finding of this dissertation: hyperscale AI data centres are heavily clustering in basins that are ALREADY in severe hydrological overdraft before any new compute cooling demand is added.'
    },
    'kpi-most-severe-stress': {
      title: 'Most Severe Groundwater Stress',
      tag: 'Critical Vulnerability',
      whatItMeasures: 'Gurugram (Haryana) exhibits the highest extraction rate among all hosting districts at 194.6% of annual replenishment.',
      methodology: 'CGWB 2025 assessment: Annual Extractable Ground Water Resource of 22,591 ham vs. Current Annual Extraction of 43,968 ham.',
      sustainabilitySignificance: 'Exemplifies regulatory blind-spots. Operating water-intensive evaporative cooling towers in Gurugram directly accelerates aquifer depletion, directly competing with community drinking water reserves.'
    },
    'chart-dcs-by-state': {
      title: 'Data Centre Campuses by State',
      tag: 'Regional Distribution',
      whatItMeasures: 'Count of tracked campuses across the 14 host states in India.',
      methodology: 'Empirical aggregation of individual facility entries by state administrative boundary.',
      sustainabilitySignificance: 'Highlights the massive primacy of Maharashtra (31 campuses), followed by Tamil Nadu (16), Telangana (14), and Karnataka (11). Proximity to subsea cable landing stations (Navi Mumbai, Chennai) strongly drives siting, often overshadowing local water resource limitations.'
    },
    'chart-mw-by-state': {
      title: 'IT Load: Live vs. Planned Pipeline',
      tag: 'Surge Comparison',
      whatItMeasures: 'Operational IT compute load vs. unbuilt announced pipeline (MW) across host states.',
      methodology: 'Stacked comparison derived from verified commissioning dates against announced pipeline MoUs.',
      sustainabilitySignificance: 'Visually conveys that ~87% of all capacity is currently unbuilt pipeline. In Maharashtra alone, planned IT load reaches 5,392.9 MW versus 746.7 MW live, illustrating that the ecological impacts observed today are only the vanguard of a much larger surge.'
    },
    'chart-verification-confidence': {
      title: 'Research Verification Confidence',
      tag: 'Audit Quality',
      whatItMeasures: 'Distribution of evidence rigor: 2+ independent sources (25), Primary statutory filings (40), Partially verified (48), Unverified (1).',
      methodology: 'Classified using academic audit standards. Primary sources include MoEFCC clearance files, company 10-K/annual disclosures, and official state gazettes.',
      sustainabilitySignificance: 'Ensures absolute academic transparency by distinguishing contractual/regulatory commitments from early-stage speculative press releases.'
    },
    'chart-precision-breakdown': {
      title: 'Spatial Precision Breakdown',
      tag: 'Geospatial Audit',
      whatItMeasures: 'Granularity of coordinate locations: Plot/village (51), Centroid fallback (28), Locality/industrial park (25), Exact site (13), District only (1).',
      methodology: 'Reflects the exact positional precision obtained during coordinate research.',
      sustainabilitySignificance: 'Validates that over three-quarters of sites represent real-world physical coordinates, while holding the dashboard accountable regarding which dots represent district centroid fallbacks.'
    },
    'chart-gw-category-distribution': {
      title: 'Host District Groundwater Status',
      tag: 'Regulatory Classification',
      whatItMeasures: 'Categorization of the 30 hosting districts across the four CGWB 2025 regulatory bands: Safe (18), Semi-critical (3), Critical (1), Over-exploited (8).',
      methodology: 'Official CGWB regulatory standard based on extraction stage: Safe (<70%), Semi-critical (70–90%), Critical (90–100%), Over-exploited (>100%).',
      sustainabilitySignificance: 'Over a quarter of all data centre districts sit in the highest legal hazard category, where groundwater extraction for commercial use is strictly restricted or banned by the Central Ground Water Authority (CGWA).'
    },
    'chart-gw-stress-ranked': {
      title: 'Groundwater Stress Ranked Across Hosting Districts',
      tag: 'Central Dissertation Exhibit',
      whatItMeasures: 'Exact Stage of Extraction (%) for all 29 hosting districts, sorted from most depleted to safest.',
      methodology: 'Direct join with CGWB 2025 dynamic resource accounting (Stage = Total Annual Extraction / Annual Extractable Resource × 100).',
      sustainabilitySignificance: 'The core empirical exhibit of the dissertation. 8 districts exceed 100% (Gurugram 194.6%, Bengaluru Urban 177.3%, Bengaluru Rural 146.8%, Chennai 121.7%, Indore 118.0%, Gandhinagar 111.3%, Sonipat 108.7%, Gautam Buddha Nagar 105.2%), demonstrating clear spatial overlap between AI compute clusters and critical water deficits.'
    },
    'chart-jjm-tap-coverage': {
      title: 'Jal Jeevan Mission Tap Water Coverage (%)',
      tag: 'Domestic Water Vulnerability',
      whatItMeasures: 'Percentage of rural households with functional tap water connections (FHTC) across hosting districts.',
      methodology: 'Official Jal Jeevan Mission national census dashboard dataset, Department of Drinking Water and Sanitation, Ministry of Jal Shakti.',
      sustainabilitySignificance: 'Exposes acute human water security conflicts. In districts like North 24 Parganas (66.8%), Guntur (68.1%), and Hooghly (68.1%), nearly one-third of rural households lack tap water, raising profound ethical questions if municipal reservoirs prioritize hyperscale data centre cooling.'
    },
    'chart-facilities-by-gw-zone': {
      title: 'Data Centre Facilities by Groundwater Zone',
      tag: 'Spatial Risk Distribution',
      whatItMeasures: 'Distribution of 118 tracked data centre campuses across CGWB 2025 groundwater stress categories. 33 facilities (28%) are in over-exploited zones, 9 (7.6%) in semi-critical, and 76 (64.4%) in safe zones.',
      methodology: 'Each facility is matched to its hosting district\'s CGWB 2025 groundwater assessment. Districts carved after the 2011 Census are mapped to their parent district for CGWB alignment.',
      sustainabilitySignificance: 'Over a quarter of all data centre campuses are in districts where groundwater extraction already exceeds sustainable recharge. These facilities will compete with agriculture and drinking water for an already depleting aquifer.'
    },
    'chart-facilities-by-location': {
      title: 'Data Centre Siting: Metro vs Non-Metro',
      tag: 'Urbanization Pattern',
      whatItMeasures: 'Classification of 118 data centre campuses by urban tier: 68 (57.6%) in Tier-1 metro cores (Mumbai, Bengaluru, Hyderabad, Chennai, Kolkata, Delhi, Pune), 26 (22%) in satellite industrial suburbs within metro influence zones, and 24 (20.3%) in emerging Tier-2+ locations.',
      methodology: 'Districts classified using Census 2011 urban agglomeration boundaries and state industrial development zone registrations. Satellite zones include Noida (Gautam Buddha Nagar), Navi Mumbai (Raigad), Chengalpattu, and Bengaluru Rural.',
      sustainabilitySignificance: 'The extreme metro concentration (nearly 80% in Tier-1 metros or their suburbs) intensifies localized power grid stress and groundwater competition. The small but growing Tier-2 footprint suggests early-stage diversification that could ease future sustainability pressures if directed toward water-surplus basins.'
    },
    'map-gw-stress': {
      title: 'CGWB Groundwater Extraction Gradient',
      tag: 'Nationwide Layer',
      whatItMeasures: 'District-by-district extraction as a percentage of sustainable recharge across all 643 districts of India.',
      methodology: 'CGWB 2025 Dynamic Groundwater Resource Assessment: Green (Safe, <70%), Amber (Semi-critical, 70-90%), Orange (Critical, 90-100%), Red (Over-exploited, >100%).',
      sustainabilitySignificance: 'Enables users to evaluate the broader hydrological context of India and see whether data centre developers are siting facilities in water-surplus or water-deficit aquifers.'
    },
    'map-marker-confidence': {
      title: 'Marker Confidence & Capacity Sizing',
      tag: 'Symbol Encoding',
      whatItMeasures: 'Visual encoding of facility confidence and electrical capacity scale.',
      methodology: 'Solid circle markers denote verified coordinates (exact site, plot, or village). Hollow dashed rings denote district centroid fallbacks. Marker radius scales with the square root of capacity (MW).',
      sustainabilitySignificance: 'Maintains absolute spatial honesty by ensuring unverified pipeline MoUs are immediately distinguishable from verified physical installations.'
    }
  };

  // Expose globally so map and app can access
  window.INFO_EXPLANATIONS = INFO_EXPLANATIONS;

  const Dashboard = {
    charts: {},

    // Mapping of KPI card label to info key
    KPI_INFO_MAP: {
      'Data centre campuses tracked': 'kpi-campuses',
      'States covered': 'kpi-states',
      'Districts covered': 'kpi-districts',
      'Live IT load capacity': 'kpi-live-it',
      'Planned IT load capacity': 'kpi-planned-it',
      'Live facility/grid load': 'kpi-live-facility',
      'Planned facility/grid load': 'kpi-planned-facility',
      'Sites with a verified real-world location': 'kpi-verified-sites',
      'Districts already over-exploited for groundwater': 'kpi-overexploited-districts',
      'Most severe groundwater stress': 'kpi-most-severe-stress'
    },

    // Initialize the Summary View with data from summary_stats.json
    init: function (summaryData) {
      if (!summaryData) {
        console.error('No summary data provided to Dashboard');
        return;
      }
      this.renderKPICards(summaryData.kpi_cards || []);
      this.renderCharts(summaryData.charts || {});
      this.initInfoPopovers();
    },

    // Render 10 KPI Cards with contextual "i" buttons
    renderKPICards: function (cards) {
      const container = document.getElementById('kpi-cards-grid');
      if (!container) return;

      container.innerHTML = '';

      cards.forEach((card, index) => {
        const cardEl = document.createElement('div');
        cardEl.className = 'kpi-card';

        // Styling variants for key thematic cards
        if (card.label.includes('Planned IT load')) {
          cardEl.classList.add('featured-orange');
        } else if (card.label.includes('over-exploited')) {
          cardEl.classList.add('featured-alert');
        } else if (card.label.includes('Most severe')) {
          cardEl.classList.add('featured-dark');
        }

        // Format value
        let formattedValue = card.value;
        if (typeof card.value === 'number') {
          formattedValue = card.value.toLocaleString('en-IN');
        }

        let unitHtml = card.unit ? `<span class="kpi-unit">${card.unit}</span>` : '';
        let totalHtml = card.total ? `<span class="kpi-unit" style="font-size:12px;"> / ${card.total}</span>` : '';
        let pctHtml = card.pct ? `<span class="kpi-unit" style="color:var(--gw-safe); font-weight:700; margin-left:4px;">(${card.pct}%)</span>` : '';

        // Note or detail text
        let noteText = card.note || card.detail || '';
        if (card.label.includes('over-exploited') && !noteText) {
          noteText = 'Districts exceeding sustainable extraction yield';
        }

        const infoId = this.KPI_INFO_MAP[card.label] || 'kpi-campuses';

        cardEl.innerHTML = `
          <div class="kpi-header-row">
            <div class="kpi-label">${card.label}</div>
            <button class="info-btn" data-info-id="${infoId}" aria-label="Explain ${card.label}" title="Explain this metric">i</button>
          </div>
          <div class="kpi-value-row">
            <div class="kpi-value">${formattedValue}</div>
            ${unitHtml}
            ${totalHtml}
            ${pctHtml}
          </div>
          ${noteText ? `<div class="kpi-note">${noteText}</div>` : ''}
        `;

        container.appendChild(cardEl);
      });
    },

    // Global Info Popover Manager
    initInfoPopovers: function () {
      if (window._infoPopoverInitialized) return;
      window._infoPopoverInitialized = true;

      function showInfoPopover(targetBtn, infoId) {
        const info = INFO_EXPLANATIONS[infoId];
        if (!info) return;

        let popover = document.getElementById('global-info-popover');
        if (!popover) {
          popover = document.createElement('div');
          popover.id = 'global-info-popover';
          popover.className = 'info-popover';
          document.body.appendChild(popover);
        }

        // Toggle off if clicking the active button
        if (popover.classList.contains('visible') && popover._activeBtn === targetBtn) {
          hideInfoPopover();
          return;
        }

        // Clear other active buttons
        document.querySelectorAll('.info-btn.active').forEach(b => b.classList.remove('active'));
        targetBtn.classList.add('active');
        popover._activeBtn = targetBtn;

        popover.innerHTML = `
          <div class="info-popover-header">
            <div>
              <div class="info-popover-title">${info.title}</div>
              <span class="info-popover-tag">${info.tag || 'Metric Explainer'}</span>
            </div>
            <button class="info-popover-close" aria-label="Close explainer">✕</button>
          </div>
          <div class="info-popover-body">
            <div>
              <div class="info-section-title">What it Measures</div>
              <div class="info-section-desc">${info.whatItMeasures}</div>
            </div>
            <div>
              <div class="info-section-title">Data Source & Methodology</div>
              <div class="info-section-desc">${info.methodology}</div>
            </div>
            <div class="info-significance-box">
              <div class="info-section-title" style="color:var(--primary); margin-bottom:2px;">Sustainability Significance</div>
              <div>${info.sustainabilitySignificance}</div>
            </div>
          </div>
        `;

        popover.querySelector('.info-popover-close').addEventListener('click', (e) => {
          e.stopPropagation();
          hideInfoPopover();
        });

        // Smart positioning relative to target button
        const rect = targetBtn.getBoundingClientRect();
        const popoverWidth = 380;
        
        // Horizontal: check screen boundaries
        let left = rect.left + window.scrollX;
        if (left + popoverWidth > window.innerWidth - 20) {
          left = window.innerWidth - popoverWidth - 20;
        }
        if (left < 16) left = 16;

        // Vertical: position below or above if overflowing bottom
        let top = rect.bottom + 8;
        const estimatedHeight = 340;
        if (top + estimatedHeight > window.innerHeight && rect.top > estimatedHeight + 10) {
          top = rect.top - estimatedHeight - 8;
        }

        popover.style.left = `${left}px`;
        popover.style.top = `${top}px`;

        popover.classList.add('visible');
      }

      function hideInfoPopover() {
        const popover = document.getElementById('global-info-popover');
        if (popover) {
          popover.classList.remove('visible');
          popover._activeBtn = null;
        }
        document.querySelectorAll('.info-btn.active').forEach(b => b.classList.remove('active'));
      }

      // Delegate click to any .info-btn across the entire page
      document.addEventListener('click', (e) => {
        const btn = e.target.closest('.info-btn');
        if (btn) {
          e.stopPropagation();
          const infoId = btn.getAttribute('data-info-id');
          showInfoPopover(btn, infoId);
          return;
        }

        // Close when clicking outside popover
        const popover = document.getElementById('global-info-popover');
        if (popover && popover.classList.contains('visible')) {
          if (!popover.contains(e.target)) {
            hideInfoPopover();
          }
        }
      });

      // Escape key closes popover
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
          hideInfoPopover();
        }
      });
    },

    // Global Chart.js defaults to match Replicate / Editorial styling
    applyChartDefaults: function () {
      Chart.defaults.font.family = "'Inter', -apple-system, sans-serif";
      Chart.defaults.font.size = 12;
      Chart.defaults.color = '#575757';
      Chart.defaults.plugins.tooltip.backgroundColor = '#202020';
      Chart.defaults.plugins.tooltip.titleFont = {
        family: "'Bricolage Grotesque', sans-serif",
        size: 13,
        weight: '700'
      };
      Chart.defaults.plugins.tooltip.bodyFont = {
        family: "'JetBrains Mono', monospace",
        size: 12
      };
      Chart.defaults.plugins.tooltip.padding = 10;
      Chart.defaults.plugins.tooltip.cornerRadius = 6;
      Chart.defaults.plugins.tooltip.boxPadding = 4;
    },

    // Render all 7 charts
    renderCharts: function (chartsData) {
      this.applyChartDefaults();

      this.renderDCByState(chartsData.data_centres_by_state || []);
      this.renderMWByState(chartsData.mw_by_state || []);
      this.renderVerificationConfidence(chartsData.verification_confidence || []);
      this.renderCoordinatePrecision(chartsData.coordinate_precision_breakdown || []);
      this.renderGWCategoryDistribution(chartsData.groundwater_category_distribution || []);
      this.renderGWStressRanked(chartsData.groundwater_stress_ranked_all_districts || []);
      this.renderJJMTapCoverage(chartsData.jjm_tap_coverage_ranked || []);
      this.renderFacilitiesByGWZone(chartsData.facilities_by_gw_zone || []);
      this.renderFacilitiesByLocation(chartsData.facilities_by_location_type || []);
    },

    // 1. Data Centres by State (Horizontal Bar)
    renderDCByState: function (data) {
      const ctx = document.getElementById('chart-dcs-by-state');
      if (!ctx) return;

      const labels = data.map(d => d.state);
      const values = data.map(d => d.count);

      this.charts.dcByState = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [{
            label: 'Campuses',
            data: values,
            backgroundColor: '#ea2804',
            borderRadius: 4,
            barThickness: 16
          }]
        },
        options: {
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false }
          },
          scales: {
            x: {
              grid: { color: 'rgba(32, 32, 32, 0.06)' },
              ticks: { precision: 0 }
            },
            y: {
              grid: { display: false },
              ticks: { font: { weight: 600 } }
            }
          }
        }
      });
    },

    // 2. MW Capacity by State (Grouped Bar: Live vs Planned)
    renderMWByState: function (data) {
      const ctx = document.getElementById('chart-mw-by-state');
      if (!ctx) return;

      const labels = data.map(d => d.state);
      const liveMW = data.map(d => d.live_it_mw);
      const plannedMW = data.map(d => d.planned_it_mw);

      this.charts.mwByState = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [
            {
              label: 'Live IT Load (MW)',
              data: liveMW,
              backgroundColor: '#202020',
              borderRadius: 3,
              barThickness: 12
            },
            {
              label: 'Planned IT Load (MW)',
              data: plannedMW,
              backgroundColor: '#ea2804',
              borderRadius: 3,
              barThickness: 12
            }
          ]
        },
        options: {
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'top',
              align: 'end',
              labels: {
                usePointStyle: true,
                pointStyle: 'circle',
                boxWidth: 8,
                font: { weight: 600 }
              }
            },
            tooltip: {
              callbacks: {
                label: function (context) {
                  return ` ${context.dataset.label}: ${context.raw.toLocaleString('en-IN')} MW`;
                }
              }
            }
          },
          scales: {
            x: {
              grid: { color: 'rgba(32, 32, 32, 0.06)' },
              ticks: {
                callback: function (val) {
                  return val >= 1000 ? `${val / 1000}k MW` : `${val} MW`;
                }
              }
            },
            y: {
              grid: { display: false },
              ticks: { font: { weight: 600 } }
            }
          }
        }
      });
    },

    // 3. Verification Confidence (Donut Chart)
    renderVerificationConfidence: function (data) {
      const ctx = document.getElementById('chart-verification-confidence');
      if (!ctx) return;

      const labels = data.map(d => d.status);
      const values = data.map(d => d.count);

      const colors = [
        '#2b9a66', // 2+ independent sources
        '#f59e0b', // Partially verified
        '#2563eb', // Primary source
        '#8d8d8d'  // Unverified
      ];

      this.charts.verificationConfidence = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: labels,
          datasets: [{
            data: values,
            backgroundColor: colors,
            borderColor: '#ffffff',
            borderWidth: 2,
            hoverOffset: 4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          cutout: '66%',
          plugins: {
            legend: {
              position: 'right',
              labels: {
                usePointStyle: true,
                pointStyle: 'circle',
                padding: 12,
                font: { size: 11, weight: 500 }
              }
            }
          }
        }
      });
    },

    // 4. Coordinate Precision Breakdown (Donut Chart)
    renderCoordinatePrecision: function (data) {
      const ctx = document.getElementById('chart-precision-breakdown');
      if (!ctx) return;

      const labels = data.map(d => d.tier);
      const values = data.map(d => d.count);

      const colors = [
        '#10b981', // Plot or village
        '#ea2804', // No coordinate (district centroid used)
        '#3b82f6', // Locality / industrial area
        '#059669', // Exact site
        '#8b5cf6'  // District only
      ];

      this.charts.coordinatePrecision = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: labels,
          datasets: [{
            data: values,
            backgroundColor: colors,
            borderColor: '#ffffff',
            borderWidth: 2,
            hoverOffset: 4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          cutout: '66%',
          plugins: {
            legend: {
              position: 'right',
              labels: {
                usePointStyle: true,
                pointStyle: 'circle',
                padding: 12,
                font: { size: 11, weight: 500 }
              }
            }
          }
        }
      });
    },

    // 5. Groundwater Category Distribution (Bar Chart)
    renderGWCategoryDistribution: function (data) {
      const ctx = document.getElementById('chart-gw-category-distribution');
      if (!ctx) return;

      const catMap = {
        'safe': { label: 'Safe (<70%)', color: '#2b9a66', order: 1 },
        'semi_critical': { label: 'Semi-critical (70–90%)', color: '#f59e0b', order: 2 },
        'critical': { label: 'Critical (90–100%)', color: '#f97316', order: 3 },
        'over_exploited': { label: 'Over-exploited (>100%)', color: '#dc2626', order: 4 }
      };

      const sortedData = [...data].sort((a, b) => {
        return (catMap[a.category]?.order || 99) - (catMap[b.category]?.order || 99);
      });

      const labels = sortedData.map(d => catMap[d.category]?.label || d.category);
      const values = sortedData.map(d => d.count);
      const bgColors = sortedData.map(d => catMap[d.category]?.color || '#888888');

      this.charts.gwCategoryDistribution = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [{
            label: 'Hosting Districts',
            data: values,
            backgroundColor: bgColors,
            borderRadius: 6,
            barThickness: 28
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: function (context) {
                  return ` ${context.raw} of 30 hosting districts`;
                }
              }
            }
          },
          scales: {
            x: {
              grid: { display: false },
              ticks: { font: { weight: 600, size: 11 } }
            },
            y: {
              grid: { color: 'rgba(32, 32, 32, 0.06)' },
              ticks: { precision: 0 }
            }
          }
        }
      });
    },

    // 6. Ranked Groundwater Stress Across All Districts (Prominent Horizontal Bar Chart)
    renderGWStressRanked: function (data) {
      const ctx = document.getElementById('chart-gw-stress-ranked');
      if (!ctx) return;

      const catColorMap = {
        'safe': '#2b9a66',
        'semi_critical': '#f59e0b',
        'critical': '#f97316',
        'over_exploited': '#dc2626'
      };

      const labels = data.map(d => `${d.district} (${d.state})`);
      const values = data.map(d => d.stage_pct);
      const bgColors = data.map(d => catColorMap[d.category] || '#2b9a66');

      this.charts.gwStressRanked = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [{
            label: 'Extraction as % of Sustainable Recharge',
            data: values,
            backgroundColor: bgColors,
            borderRadius: 3,
            barThickness: 11
          }]
        },
        plugins: [
          {
            id: 'overdraftThresholdLine',
            afterDraw: (chart) => {
              const xScale = chart.scales.x;
              const yScale = chart.scales.y;
              if (!xScale || !yScale) return;
              const xPos = xScale.getPixelForValue(100);
              const ctx = chart.ctx;
              ctx.save();
              ctx.setLineDash([4, 4]);
              ctx.strokeStyle = '#dc2626';
              ctx.lineWidth = 1.5;
              ctx.beginPath();
              ctx.moveTo(xPos, yScale.top);
              ctx.lineTo(xPos, yScale.bottom);
              ctx.stroke();

              ctx.fillStyle = '#dc2626';
              ctx.font = '700 10px monospace';
              ctx.fillText('100% CRITICAL OVERDRAFT', xPos + 5, yScale.top + 14);
              ctx.restore();
            }
          }
        ],
        options: {
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                afterLabel: function (context) {
                  const idx = context.dataIndex;
                  const item = data[idx];
                  return `Category: ${item.category.replace('_', ' ').toUpperCase()}`;
                },
                label: function (context) {
                  return ` Stage of Extraction: ${context.raw}%`;
                }
              }
            }
          },
          scales: {
            x: {
              grid: { color: 'rgba(32, 32, 32, 0.06)' },
              ticks: {
                callback: function (val) {
                  return `${val}%`;
                }
              }
            },
            y: {
              grid: { display: false },
              ticks: {
                font: { size: 11, family: "'Inter', sans-serif" }
              }
            }
          }
        }
      });
    },

    // 7. Jal Jeevan Mission Tap Coverage (Horizontal Bar Chart)
    renderJJMTapCoverage: function (data) {
      const ctx = document.getElementById('chart-jjm-tap-coverage');
      if (!ctx) return;

      const labels = data.map(d => `${d.district} (${d.state})`);
      const values = data.map(d => d.tap_coverage_pct);

      const bgColors = values.map(val => {
        if (val < 70) return '#ea2804';
        if (val < 85) return '#f59e0b';
        return '#2b9a66';
      });

      this.charts.jjmTapCoverage = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [{
            label: 'Rural Households with Tap Water (%)',
            data: values,
            backgroundColor: bgColors,
            borderRadius: 3,
            barThickness: 10
          }]
        },
        options: {
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: function (context) {
                  return ` JJM Household Tap Coverage: ${context.raw}%`;
                }
              }
            }
          },
          scales: {
            x: {
              min: 0,
              max: 100,
              grid: { color: 'rgba(32, 32, 32, 0.06)' },
              ticks: {
                callback: function (val) {
                  return `${val}%`;
                }
              }
            },
            y: {
              grid: { display: false },
              ticks: { font: { size: 10 } }
            }
          }
        }
      });
    },

    // 8. Facilities by Groundwater Zone (Donut Chart)
    renderFacilitiesByGWZone: function (data) {
      const ctx = document.getElementById('chart-facilities-by-gw-zone');
      if (!ctx) return;

      const catMap = {
        'safe': { label: 'Safe (<70%)', color: '#2b9a66', order: 1 },
        'semi_critical': { label: 'Semi-critical (70\u201390%)', color: '#f59e0b', order: 2 },
        'critical': { label: 'Critical (90\u2013100%)', color: '#f97316', order: 3 },
        'over_exploited': { label: 'Over-exploited (>100%)', color: '#dc2626', order: 4 }
      };

      const sortedData = [...data].sort((a, b) => {
        return (catMap[a.category]?.order || 99) - (catMap[b.category]?.order || 99);
      });

      const labels = sortedData.map(d => catMap[d.category]?.label || d.label);
      const values = sortedData.map(d => d.count);
      const bgColors = sortedData.map(d => catMap[d.category]?.color || '#888888');

      this.charts.facilitiesByGWZone = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: labels,
          datasets: [{
            data: values,
            backgroundColor: bgColors,
            borderColor: '#ffffff',
            borderWidth: 2,
            hoverOffset: 4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          cutout: '66%',
          plugins: {
            legend: {
              position: 'right',
              labels: {
                usePointStyle: true,
                pointStyle: 'circle',
                padding: 12,
                font: { size: 11, weight: 500 }
              }
            },
            tooltip: {
              callbacks: {
                label: function (context) {
                  const val = context.raw;
                  const pct = ((val / 118) * 100).toFixed(1);
                  return ` ${val} of 118 facilities (${pct}%)`;
                }
              }
            }
          }
        }
      });
    },

    // 9. Metro vs Non-Metro Siting (Horizontal Bar Chart)
    renderFacilitiesByLocation: function (data) {
      const ctx = document.getElementById('chart-facilities-by-location');
      if (!ctx) return;

      const colorMap = {
        'Metro / Tier-1 Core': '#202020',
        'Satellite / Industrial Suburb': '#ea2804',
        'Emerging / Tier-2+ Locations': '#3b82f6'
      };

      const labels = data.map(d => d.type);
      const values = data.map(d => d.count);
      const bgColors = data.map(d => colorMap[d.type] || '#888888');

      this.charts.facilitiesByLocation = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [{
            label: 'Facilities',
            data: values,
            backgroundColor: bgColors,
            borderRadius: 4,
            barThickness: 22
          }]
        },
        options: {
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: function (context) {
                  const idx = context.dataIndex;
                  const pct = data[idx].pct;
                  return ` ${context.raw} facilities (${pct}%)`;
                }
              }
            }
          },
          scales: {
            x: {
              grid: { color: 'rgba(32, 32, 32, 0.06)' },
              ticks: { precision: 0 }
            },
            y: {
              grid: { display: false },
              ticks: { font: { weight: 600 } }
            }
          }
        }
      });
    }
  };

  window.Dashboard = Dashboard;
})(window);

