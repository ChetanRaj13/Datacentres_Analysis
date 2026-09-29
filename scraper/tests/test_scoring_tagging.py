import os
import sys
import pytest

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from processing.schema import ProblemRecord
from processing.scorer import calculate_pain_score, score_all_records
from processing.tagger import tag_record_rules, tag_all_records

# 30 Hand-labelled sample posts covering realistic problems across all 4 themes
SAMPLE_POSTS = [
    # Sustainability (8 samples)
    {"text": "Why is there no cold chain infrastructure for tomato farmers in Kolar? Over 40% crop rots in post-harvest transit.", "expected": "Sustainability"},
    {"text": "Huge amount of food waste in Bangalore wedding halls every night. Over 500 kg thrown into landfills daily.", "expected": "Sustainability"},
    {"text": "Commercial kitchens have no easy way to donate food surplus safely. We need food waste reduction systems.", "expected": "Sustainability"},
    {"text": "Post-harvest loss in onion storage is killing Maharashtra farmers. We lose ₹20,000 per acre in spoilage.", "expected": "Sustainability"},
    {"text": "Apartment societies in Pune fail completely at dry and wet waste segregation. Mixed garbage fills landfills.", "expected": "Sustainability"},
    {"text": "Why are biodegradable food packaging alternatives 3x more expensive for small street food vendors?", "expected": "Sustainability"},
    {"text": "Small restaurants struggling with soaring commercial electricity and energy cost during peak summer.", "expected": "Sustainability"},
    {"text": "Lack of circular economy incentives for textile upcycling in Tirupur garment clusters.", "expected": "Sustainability"},

    # Environment (8 samples)
    {"text": "Delhi AQI crossed 480 today. Frustrated with stubble burning and vehicle emissions choking children.", "expected": "Environment"},
    {"text": "Groundwater scarcity in Bangalore east is a nightmare. Borewells dried up down to 1400 feet.", "expected": "Environment"},
    {"text": "Single use plastic packaging from quick commerce apps like Blinkit and Zepto is littering our lakes.", "expected": "Environment"},
    {"text": "Informal e-waste recycling in Seelampur exposes child workers to toxic acid fumes and lead poisoning.", "expected": "Environment"},
    {"text": "Severe water crisis in Chennai IT corridor. Tankers charging ₹4000 for dirty brackish water.", "expected": "Environment"},
    {"text": "Industrial effluent discharge into Bellandur lake causing toxic chemical froth and fire hazards.", "expected": "Environment"},
    {"text": "Urban heat island effect in Mumbai slums where tin roofs reach unbearable 48°C temperatures.", "expected": "Environment"},
    {"text": "Unregulated electronic waste disposal with old lithium batteries causing fires in municipal landfills.", "expected": "Environment"},

    # Social impact (7 samples)
    {"text": "Student mental health and suicide crisis in Kota coaching hubs due to 16-hour high pressure schedules.", "expected": "Social impact"},
    {"text": "Delivery riders and gig workers working 14 hours in 44°C heat with no health insurance or wage floor.", "expected": "Social impact"},
    {"text": "Female commuters facing severe safety issues and harassment waiting at unlit bus stops in Gurgaon.", "expected": "Social impact"},
    {"text": "Engineering college freshers facing acute burnout and depression with zero career guidance.", "expected": "Social impact"},
    {"text": "Middle class families struggling with out-of-pocket healthcare costs pushing them into severe debt.", "expected": "Social impact"},
    {"text": "Tenants in Bangalore facing arbitrary security deposit deductions and landlord harassment.", "expected": "Social impact"},
    {"text": "Public hospital waiting times exceed 8 hours for cancer chemotherapy appointments in tier 2 cities.", "expected": "Social impact"},

    # Business (7 samples)
    {"text": "MSME suppliers waiting over 120 days for invoice clearance from corporate buyers, destroying working capital.", "expected": "Business"},
    {"text": "Small retail shops struggling to compete with predatory 10-minute quick commerce dark stores.", "expected": "Business"},
    {"text": "Complex GST compliance and inverted duty structure choking small manufacturing units in Surat.", "expected": "Business"},
    {"text": "Informal vendors cannot get working capital credit from formal banks, forced to pay 5% monthly interest to loan sharks.", "expected": "Business"},
    {"text": "Logistics cost in India eats up 14% of GDP making local small exporters uncompetitive globally.", "expected": "Business"},
    {"text": "B2B payment delays and bad debt leading to bankruptcy for tier-3 component manufacturers.", "expected": "Business"},
    {"text": "Small kirana store profit margins collapsed from 15% to 4% due to aggregator price wars.", "expected": "Business"},
]

def test_tagging_accuracy_and_pain_scoring():
    correct = 0
    total = len(SAMPLE_POSTS)
    
    records = []
    for idx, sample in enumerate(SAMPLE_POSTS):
        rec = ProblemRecord(
            id=f"sample_{idx+1}",
            source="manual_test",
            url=f"https://example.com/test/{idx+1}",
            title=sample["text"][:60],
            text=sample["text"],
            author_hash="user_tester",
            score=15,
            num_comments=5,
            query=""
        )
        records.append(rec)

    # Score and tag
    scored_records = score_all_records(records)
    tagged_records = tag_all_records(scored_records, use_llm=False)

    print("\n" + "="*70)
    print(" [TARGET] 30 HAND-LABELLED POSTS TAGGING ACCURACY EVALUATION")
    print("="*70)
    for idx, (rec, sample) in enumerate(zip(tagged_records, SAMPLE_POSTS), 1):
        expected = sample["expected"]
        predicted = rec.theme
        is_match = (expected == predicted)
        if is_match:
            correct += 1
        
        status = "[PASS]" if is_match else "[FAIL]"
        print(f"[{idx:02d}] {status} | Pred: {predicted:<14} | Exp: {expected:<14} | Pain: {rec.pain_score:.1f}")
        assert rec.pain_score >= 1.0 and rec.pain_score <= 10.0

    accuracy = (correct / total) * 100
    print("-" * 70)
    print(f"Overall Tagging Accuracy: {correct}/{total} ({accuracy:.1f}%)")
    print("=" * 70 + "\n")

    # We expect high accuracy (>= 90%)
    assert accuracy >= 90.0, f"Accuracy too low: {accuracy}%"
