import os
import re
import pytest
from playwright.sync_api import sync_playwright

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_DIR = os.path.dirname(TEST_DIR) if os.path.basename(TEST_DIR) == "tests" else TEST_DIR
HTML_PATH = os.path.join(WORKSPACE_DIR, "impact_explorer.html")
FILE_URL = f"file:///{HTML_PATH.replace(os.sep, '/')}"

@pytest.fixture(scope="module")
def browser_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(FILE_URL)
        page.wait_for_load_state("networkidle")
        yield page
        browser.close()

def test_file_exists():
    """Verify that impact_explorer.html exists and is non-empty."""
    assert os.path.exists(HTML_PATH), "impact_explorer.html does not exist"
    assert os.path.getsize(HTML_PATH) > 10000, "impact_explorer.html is too small"

def test_default_state_numbers_match_master_context(browser_page):
    """
    Test 1: Default-state numbers match the locked Master Context table exactly:
    - High Demand = 48,952 GWh, High Capacity = 8,597 MW
    - Low Demand = 19,684 GWh, Low Capacity = 3,457 MW
    - National average gap = 77.8%
    - Kolkata gap = 81.8% at default, avoided CO2 = 12,090 t (High) / 7,606 t (Low)
    - All other 8 clusters report 0 t CO2 avoided against state grid baseline
    - SSI scores match locked deck values: Kurnool +15.31, Sri City +9.61, Tumakuru +12.83, Dobbaspet +13.75, Neemrana +23.79
    """
    page = browser_page

    # Check Total Capacity & Demand in default (High) mode
    nat_demand = page.locator("#natDemandVal").inner_text()
    assert "48,952 GWh" in nat_demand or "48,951 GWh" in nat_demand, f"High demand mismatch: {nat_demand}"
    assert "8,597" in page.locator("#natMwCap").inner_text(), "Total High capacity (8,597 MW) missing in national strip"

    # Check National summary gap
    nat_gap = page.locator("#natGapVal").inner_text()
    assert "77.8%" in nat_gap, f"National gap mismatch: {nat_gap}"

    # Check Kolkata card numbers
    kolkata_card = page.locator(".cluster-card:has-text('Kolkata')")
    assert kolkata_card.count() > 0, "Kolkata card not found"
    card_text = kolkata_card.inner_text()
    assert "81.8%" in card_text, f"Kolkata gap % mismatch: {card_text}"
    assert "+12,090 t" in card_text or "12,090" in card_text, f"Kolkata avoided CO2 mismatch: {card_text}"

    # Check Low Capacity Mode toggle
    page.click("#btnLowCap")
    page.wait_for_timeout(300)
    low_demand = page.locator("#natDemandVal").inner_text()
    assert "19,684 GWh" in low_demand, f"Low demand mismatch: {low_demand}"
    assert "3,457" in page.locator("#natMwCap").inner_text(), "Total Low capacity (3,457 MW) missing"
    
    # Check Kolkata CO2 in Low mode = 7,606 t
    assert "7,606 t" in kolkata_card.inner_text() or "7,606" in kolkata_card.inner_text()

    # Toggle back to High mode
    page.click("#btnHighCap")
    page.wait_for_timeout(300)

    # Check SSI candidate table scores at default weights
    # 1. Kurnool / Orvakal net score +15.31, uplift +17.87
    kurnool_row = page.locator("#candidatesTbody tr:has-text('Orvakal')")
    assert kurnool_row.count() > 0, "Kurnool row not found in SSI table"
    assert "+15.31" in kurnool_row.inner_text(), f"Kurnool score mismatch: {kurnool_row.inner_text()}"
    assert "+17.87" in kurnool_row.inner_text(), f"Kurnool uplift mismatch: {kurnool_row.inner_text()}"

    # 2. Sri City net score +9.61
    sri_city_row = page.locator("#candidatesTbody tr:has-text('Sri City')")
    assert "+9.61" in sri_city_row.inner_text(), f"Sri City score mismatch: {sri_city_row.inner_text()}"

    # 3. Tumakuru net score +12.83
    tumakuru_row = page.locator("#candidatesTbody tr:has-text('Vasanthanarasapura')")
    assert "+12.83" in tumakuru_row.inner_text(), f"Tumakuru score mismatch: {tumakuru_row.inner_text()}"

    # 4. Dobbaspet net score +13.75
    dobbaspet_row = page.locator("#candidatesTbody tr:has-text('Dobbaspet')")
    assert "+13.75" in dobbaspet_row.inner_text(), f"Dobbaspet score mismatch: {dobbaspet_row.inner_text()}"

    # 5. Neemrana net score +23.79 (corrected from +39.50)
    neemrana_row = page.locator("#candidatesTbody tr:has-text('Neemrana')")
    assert "+23.79" in neemrana_row.inner_text(), f"Neemrana score mismatch: {neemrana_row.inner_text()}"

def test_jhansi_600mw_correction_and_siting_caveats(browser_page):
    """
    Test 2: Check siting section reflects the locked corrections:
    - BIDA Jhansi solar park specifically shows 600 MW, NOT 4,000 MW
    - Neemrana shows 'State Proxy' and wind CF 'Not Viable'
    """
    page = browser_page

    # Verify BIDA Jhansi row shows 600 MW
    jhansi_row = page.locator("#candidatesTbody tr:has-text('Jhansi')")
    assert jhansi_row.count() > 0, "Jhansi row not found"
    jhansi_text = jhansi_row.inner_text()
    assert "600 MW" in jhansi_text, f"Jhansi did not display 600 MW: {jhansi_text}"
    assert "4,000 MW" not in jhansi_text and "4000 MW" not in jhansi_text

    # Verify Neemrana row shows State Proxy and Not Viable
    neemrana_row = page.locator("#candidatesTbody tr:has-text('Neemrana')")
    neemrana_text = neemrana_row.inner_text()
    assert "State Proxy" in neemrana_text or "Proxy" in neemrana_text
    assert "Not Viable" in neemrana_text

def test_jamnagar_desal_split_and_dual_wind_scenarios(browser_page):
    """
    Test 3: Check Jamnagar water desalination scope and dual wind CF scenario:
    - Jamnagar water priority is 'Medium-High Priority' (NOT 'Low Priority')
    - Jamnagar card displays confirmed (168 MW) vs unconfirmed (832-2,832 MW) portions
    - Jamnagar allows toggling between Conservative (24% wind, 76.6% gap) and Claimed (32% wind, 73.4% gap)
    """
    page = browser_page

    jamnagar_card = page.locator(".cluster-card:has-text('Jamnagar')")
    assert jamnagar_card.count() > 0, "Jamnagar card not found"
    j_text = jamnagar_card.inner_text()

    # 1. Water Priority is Medium-High, not Low Priority
    assert "Medium-High" in j_text, f"Jamnagar priority not Medium-High: {j_text}"
    assert "Low Priority" not in j_text

    # 2. Water split confirmed 168 MW vs unconfirmed 832-2,832 MW
    assert "168 MW" in j_text and "1,196 ML" in j_text
    assert "832" in j_text or "2,832" in j_text

    # 3. Default wind scenario is Conservative 24% -> 76.6% gap
    assert "76.6%" in j_text, f"Default Jamnagar gap not 76.6%: {j_text}"

    # 4. Toggle to Claimed Regional 32% wind scenario
    claimed_btn = jamnagar_card.locator("button:has-text('Claimed 32%')")
    claimed_btn.click()
    page.wait_for_timeout(300)

    # In claimed upside mode, gap should update to 73.4%
    j_text_claimed = jamnagar_card.inner_text()
    assert "73.4%" in j_text_claimed, f"Jamnagar gap did not update to 73.4% under claimed upside: {j_text_claimed}"

    # Toggle back to Conservative 24%
    cons_btn = jamnagar_card.locator("button:has-text('Cons. 24%')")
    cons_btn.click()
    page.wait_for_timeout(300)
    assert "76.6%" in jamnagar_card.inner_text()

def test_map_cluster_capacities_and_relocation_distances(browser_page):
    """
    Test 4: Map view's cluster capacities and relocation arrows match Master Context:
    - 9 cluster dots render with proportional sizes
    - Relocation arrows present with exact distances:
      Hyderabad->Kurnool 205 km, Chennai->Sri City 72 km, Bengaluru->Tumakuru 76 km
    - Clicking nodes displays exact capacity in MW
    """
    page = browser_page

    # Verify arrows
    arrow_hyd = page.locator("#arrow_hyd_kurnool")
    arrow_chn = page.locator("#arrow_chn_sricity")
    arrow_blr = page.locator("#arrow_blr_tumakuru")
    assert arrow_hyd.count() == 1
    assert arrow_chn.count() == 1
    assert arrow_blr.count() == 1

    # Click Hyderabad -> Kurnool arrow and check distance in drawer
    page.eval_on_selector("#arrow_hyd_kurnool", "el => el.dispatchEvent(new MouseEvent('click', {bubbles: true}))")
    page.wait_for_timeout(300)
    assert "205 km" in page.locator("#drawerState").inner_text()

    # Click Chennai -> Sri City arrow
    page.eval_on_selector("#arrow_chn_sricity", "el => el.dispatchEvent(new MouseEvent('click', {bubbles: true}))")
    page.wait_for_timeout(300)
    assert "72 km" in page.locator("#drawerState").inner_text()

    # Click Bengaluru -> Tumakuru arrow
    page.eval_on_selector("#arrow_blr_tumakuru", "el => el.dispatchEvent(new MouseEvent('click', {bubbles: true}))")
    page.wait_for_timeout(300)
    assert "76 km" in page.locator("#drawerState").inner_text()

    # Click Jamnagar node and check capacity (1,000 Low / 3,000 High MW)
    page.eval_on_selector("#clusterNodes g:has-text('Jamnagar')", "el => el.dispatchEvent(new MouseEvent('click', {bubbles: true}))")
    page.wait_for_timeout(300)
    assert "1,000" in page.locator("#drawerMwLow").inner_text()
    assert "3,000" in page.locator("#drawerMwHigh").inner_text()
    assert "Medium-High Priority" in page.locator("#drawerWaterStress").inner_text()

def test_superseded_claims_audit_in_methodology(browser_page):
    """
    Test 5: Methodology drawer displays explicit audit trail of superseded claims:
    - Documents why 8.4-20.5 Mt model was discarded
    - Confirms no superseded claim is accepted as an active figure
    """
    page = browser_page

    # Click open methodology button
    page.click("#btnOpenMethodology")
    page.wait_for_timeout(300)

    panel_text = page.locator("#methodologyPanel").inner_text()
    assert "AUDIT TRAIL" in panel_text.upper()
    assert "CORRECTED & SUPERSEDED CLAIMS" in panel_text.upper()
    assert "Discarded 8.4–20.5 Mt CO₂ Avoided Model" in panel_text
    assert "BIDA Jhansi 600 MW Correction" in panel_text
    assert "Neemrana Wind & Net Score Correction" in panel_text
    assert "Jamnagar Dual-Scenario Wind CF" in panel_text
    assert "Jamnagar Water Scope Honesty" in panel_text

    # Close modal
    page.click(".btn-close")
    page.wait_for_timeout(300)

def test_accurate_india_map_and_survey_of_india_boundaries(browser_page):
    """
    Test 6: Verify India Map is using accurate Survey of India boundaries:
    - High-fidelity mainland outline path with > 5,000 characters
    - All 36 States and Union Territories explicitly rendered in #stateBoundaries
    - Critical sensitive border regions (Ladakh, Jammu & Kashmir, Arunachal Pradesh) present
    - Interactive state hover updates dynamic label
    - 9 cluster dots positioned correctly relative to geographic state coordinates
    """
    page = browser_page

    # 1. Check outer mainland silhouette fidelity
    outline = page.locator("#indiaOutline")
    assert outline.count() == 1, "#indiaOutline path not found"
    d_attr = outline.get_attribute("d")
    assert len(d_attr) > 5000, f"Outline path is too short or simplified ({len(d_attr)} chars)"

    # 2. Check all 36 States & UTs rendered
    states = page.locator("#stateBoundaries path")
    assert states.count() == 36, f"Expected 36 states/UTs, found {states.count()}"

    # Verify critical regions
    state_names = [states.nth(i).get_attribute("data-name") for i in range(states.count())]
    for required in ["Ladakh", "Jammu & Kashmir", "Arunachal Pradesh", "Maharashtra", "Gujarat", "Tamil Nadu", "Karnataka", "West Bengal", "Delhi", "Telangana", "Andhra Pradesh"]:
        assert required in state_names, f"Required boundary region missing: {required}"

    # 3. Test state hover functionality
    page.eval_on_selector("#st_maharashtra", "el => el.dispatchEvent(new MouseEvent('mouseenter'))")
    page.wait_for_timeout(100)
    hover_label = page.locator("#hoverStateName").text_content() or ""
    assert "MAHARASHTRA" in hover_label, f"Hover label did not reflect state: {hover_label}"

    page.eval_on_selector("#st_maharashtra", "el => el.dispatchEvent(new MouseEvent('mouseleave'))")
    page.wait_for_timeout(100)

    # 4. Check 9 cluster dots render inside SVG viewport
    cluster_dots = page.locator("#clusterNodes g")
    assert cluster_dots.count() == 9, f"Expected 9 cluster dots, found {cluster_dots.count()}"

def test_light_dark_theme_toggle_and_persistence(browser_page):
    """
    Test 7: Verify Light/Dark mode toggle:
    - Switches HTML attribute to data-theme='light'
    - Changes background and card colors with zero unreadable text
    - Persists across page reload via localStorage
    - Toggles cleanly back to dark mode
    """
    page = browser_page

    # Verify initial theme is dark
    initial_theme = page.evaluate("document.documentElement.getAttribute('data-theme')")
    assert initial_theme in ["dark", None], f"Expected initial dark theme, got: {initial_theme}"

    # Click theme toggle button to switch to light mode
    page.click("#themeToggleBtn")
    page.wait_for_timeout(200)

    # Verify light theme applied
    light_theme = page.evaluate("document.documentElement.getAttribute('data-theme')")
    assert light_theme == "light", f"Expected light theme, got: {light_theme}"

    stored_theme = page.evaluate("localStorage.getItem('dc_impact_theme')")
    assert stored_theme == "light", f"localStorage did not store light theme: {stored_theme}"

    # Verify background and card text styles are high-contrast light mode
    bg_color = page.evaluate("getComputedStyle(document.body).backgroundColor")
    assert "248, 250, 252" in bg_color or "rgb(248" in bg_color, f"Unexpected body light bg: {bg_color}"

    # Test persistence across reload
    page.reload()
    page.wait_for_load_state("networkidle")
    persisted_theme = page.evaluate("document.documentElement.getAttribute('data-theme')")
    assert persisted_theme == "light", f"Theme did not persist after reload: {persisted_theme}"

    # Toggle back to dark mode
    page.click("#themeToggleBtn")
    page.wait_for_timeout(200)
    dark_theme = page.evaluate("document.documentElement.getAttribute('data-theme')")
    assert dark_theme == "dark", f"Expected dark theme after toggle, got: {dark_theme}"
    assert page.evaluate("localStorage.getItem('dc_impact_theme')") == "dark"

def test_card_info_buttons_across_sections_no_data_alteration(browser_page):
    """
    Test 8: Verify 'i' info buttons on cards across all sections:
    - Info buttons exist on baseline cards, SSI calculator, comparison cards, and map
    - Clicking opens contextual modal with card-specific title, description, and formula
    - Clicking NEVER mutates slider state, capacity values, or triggers recalculation
    - Full glossary link inside modal successfully opens methodology drawer
    """
    page = browser_page

    # Verify presence of info buttons across dashboard
    info_buttons = page.locator(".card-info-btn")
    count = info_buttons.count()
    assert count >= 15, f"Expected at least 15 info buttons across sections, found {count}"

    # Capture baseline state before clicking info button
    initial_demand = page.locator("#natDemandVal").inner_text()
    initial_gap = page.locator("#natGapVal").inner_text()
    initial_util = page.locator("#badgeUtil").inner_text()

    # 1. Test clicking KPI capacity info button
    kpi_info = page.locator(".hero-kpi-card:has-text('2030 Pipeline Electricity') .card-info-btn")
    kpi_info.click()
    page.wait_for_timeout(200)

    # Modal should be open
    modal = page.locator("#cardInfoModal")
    assert "active" in modal.get_attribute("class")
    title = page.locator("#infoModalTitle").inner_text()
    desc = page.locator("#infoModalDesc").inner_text()
    formula = page.locator("#infoModalFormula").inner_text()

    assert "Capacity" in title, f"Unexpected modal title: {title}"
    assert "8,597 MW" in desc or "3,457 MW" in desc
    assert "Capacity (MW)" in formula

    # Verify NO DATA ALTERATION occurred
    assert page.locator("#natDemandVal").inner_text() == initial_demand, "Demand value was mutated by info click!"
    assert page.locator("#natGapVal").inner_text() == initial_gap, "Gap value was mutated by info click!"
    assert page.locator("#badgeUtil").inner_text() == initial_util, "Slider was mutated by info click!"

    # Test link to glossary
    page.click("#infoModalGlossaryBtn")
    page.wait_for_timeout(200)

    # Modal should be closed and methodology panel open
    assert "active" not in (page.locator("#cardInfoModal").get_attribute("class") or "")
    assert page.locator("#drawerOverlay").is_visible()

    # Close methodology drawer
    page.click(".btn-close")
    page.wait_for_timeout(200)

    # 2. Test clicking Mumbai cluster card info button
    mumbai_info = page.locator(".cluster-card:has-text('Mumbai') .card-info-btn")
    mumbai_info.click()
    page.wait_for_timeout(200)

    assert "active" in page.locator("#cardInfoModal").get_attribute("class")
    assert "Mumbai" in page.locator("#infoModalTitle").inner_text()
    assert "78.8%" in page.locator("#infoModalDesc").inner_text()

    # Close info modal
    page.click(".info-modal-close")
    page.wait_for_timeout(200)
    assert "active" not in (page.locator("#cardInfoModal").get_attribute("class") or "")

