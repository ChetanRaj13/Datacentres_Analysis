/**
 * app.js — Main Application Orchestrator for India AI Data Centre Sustainability Dashboard
 * Handles global data fetching, tab switching, and component initialization
 */

(function () {
  'use strict';

  const App = {
    summaryData: null,
    geojsonData: null,
    facilitiesData: null,

    init: async function () {
      this.setupNavigation();
      await this.loadData();
    },

    // Navigation and View Switching
    setupNavigation: function () {
      const tabMap = document.getElementById('tab-map');
      const tabSummary = document.getElementById('tab-summary');
      const viewMap = document.getElementById('map-view');
      const viewSummary = document.getElementById('summary-view');

      function switchView(target) {
        if (target === 'summary-view' || target === 'summary') {
          tabMap.classList.remove('active');
          tabSummary.classList.add('active');
          viewMap.classList.remove('active');
          viewSummary.classList.add('active');
          window.location.hash = 'summary';
          window.scrollTo({ top: 0, behavior: 'smooth' });
        } else {
          tabSummary.classList.remove('active');
          tabMap.classList.add('active');
          viewSummary.classList.remove('active');
          viewMap.classList.add('active');
          window.location.hash = 'map';

          // Tell Leaflet to re-measure its container size
          if (window.MapView && window.MapView.map) {
            setTimeout(() => {
              window.MapView.map.invalidateSize();
            }, 100);
          }
        }
      }

      tabMap.addEventListener('click', (e) => {
        e.preventDefault();
        switchView('map-view');
      });

      tabSummary.addEventListener('click', (e) => {
        e.preventDefault();
        switchView('summary-view');
      });

      // Handle browser back/forward or initial hash
      window.addEventListener('hashchange', () => {
        const hash = window.location.hash.replace('#', '');
        if (hash === 'summary') {
          switchView('summary-view');
        } else {
          switchView('map-view');
        }
      });

      if (window.location.hash === '#summary') {
        switchView('summary-view');
      }
    },

    // Load Data Files via fetch() with direct file:// fallback
    loadData: async function () {
      try {
        console.log('Loading dataset files...');

        const [summaryRes, geojsonRes, facilitiesRes] = await Promise.all([
          fetch('summary_stats.json'),
          fetch('india_districts.geojson'),
          fetch('data_centres_processed.json')
        ]);

        if (!summaryRes.ok) throw new Error(`Failed to load summary_stats.json: ${summaryRes.status}`);
        if (!geojsonRes.ok) throw new Error(`Failed to load india_districts.geojson: ${geojsonRes.status}`);
        if (!facilitiesRes.ok) throw new Error(`Failed to load data_centres_processed.json: ${facilitiesRes.status}`);

        this.summaryData = await summaryRes.json();
        this.geojsonData = await geojsonRes.json();
        this.facilitiesData = await facilitiesRes.json();

        console.log('Dataset loaded via fetch():', {
          kpiCount: this.summaryData.kpi_cards?.length,
          districtsCount: this.geojsonData.features?.length,
          facilitiesCount: this.facilitiesData.length
        });
      } catch (err) {
        console.warn('fetch() failed or blocked (e.g. file:// protocol):', err.message);
        if (window.DATA_BUNDLE) {
          console.log('Successfully loaded datasets from local data_bundle.js fallback.');
          this.summaryData = window.DATA_BUNDLE.summaryData;
          this.geojsonData = window.DATA_BUNDLE.geojsonData;
          this.facilitiesData = window.DATA_BUNDLE.facilitiesData;
        } else {
          console.error('No data available:', err);
          return;
        }
      }

      // Initialize Map View
      if (window.MapView && this.geojsonData && this.facilitiesData) {
        window.MapView.init(this.geojsonData, this.facilitiesData);
      }

      // Initialize Dashboard View
      if (window.Dashboard && this.summaryData) {
        window.Dashboard.init(this.summaryData);
      }
    }
  };

  // Run on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => App.init());
  } else {
    App.init();
  }

  window.App = App;
})();
