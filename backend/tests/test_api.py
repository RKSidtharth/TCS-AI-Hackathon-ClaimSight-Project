"""
CLAIMSIGHT AI - Automated Test Suite
Tests authentication, claim listing, evidence relationship graph, and Next-Best-Evidence formula.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.ai.next_best_evidence.recommendation_ranker import NextBestEvidenceRanker

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_auth_login_success():
    response = client.post(
        "/api/auth/login",
        json={"email": "investigator@claimsight.ai", "password": "Investigator2026!"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["role"] == "investigator"

def test_auth_login_invalid():
    response = client.post(
        "/api/auth/login",
        json={"email": "investigator@claimsight.ai", "password": "WrongPassword!"}
    )
    assert response.status_code == 401

def test_claims_list():
    login_res = client.post(
        "/api/auth/login",
        json={"email": "investigator@claimsight.ai", "password": "Investigator2026!"}
    )
    token = login_res.json()["access_token"]

    response = client.get(
        "/api/claims",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "claims" in data
    assert len(data["claims"]) >= 10

def test_next_best_evidence_formula():
    score = NextBestEvidenceRanker.calculate_rank_score(
        expected_info_gain=0.90,
        materiality=0.85,
        reliability=0.95,
        cost=0.10,
        epsilon=0.10
    )
    # Expected: (0.90 * 0.85 * 0.95) / (0.10 + 0.10) = 0.72675 / 0.20 = 3.63
    assert score == 3.63

def test_analytics_dashboard():
    login_res = client.post(
        "/api/auth/login",
        json={"email": "admin@claimsight.ai", "password": "ClaimsightAdmin2026!"}
    )
    token = login_res.json()["access_token"]

    response = client.get(
        "/api/analytics/dashboard",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "kpis" in data
    assert data["kpis"]["total_claims"] >= 10

def test_high_impact_guardrail_blocks_standard_investigator():
    # Login as standard investigator
    inv_login = client.post(
        "/api/auth/login",
        json={"email": "investigator@claimsight.ai", "password": "Investigator2026!"}
    )
    inv_token = inv_login.json()["access_token"]

    # Attempt to approve high-impact claim CLM-2026-011 (₹7,80,000)
    res = client.post(
        "/api/claims/CLM-2026-011/decisions",
        headers={"Authorization": f"Bearer {inv_token}"},
        json={
            "status": "approved",
            "notes": "Standard investigator trying to approve 7.8L loss without executive authority",
            "approved_settlement_amount": 757000
        }
    )
    # Must be intercepted by 5 Lakhs guardrail with HTTP 403
    assert res.status_code == 403
    assert "GUARDRAIL ENFORCED" in res.json()["detail"]

def test_high_impact_guardrail_allows_executive_admin():
    # Login as Chief Compliance Officer (Admin)
    admin_login = client.post(
        "/api/auth/login",
        json={"email": "admin@claimsight.ai", "password": "ClaimsightAdmin2026!"}
    )
    admin_token = admin_login.json()["access_token"]

    # Executive approves high-impact claim CLM-2026-011 (₹7,80,000)
    res = client.post(
        "/api/claims/CLM-2026-011/decisions",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "status": "approved",
            "notes": "Chief Compliance Officer executive authorization granted after forensic audit.",
            "approved_settlement_amount": 757000
        }
    )
    assert res.status_code == 200
    data = res.json()
    assert data["decision"]["is_high_impact"] is True
    assert data["decision"]["verified_by_top_insurance_officer"] is True

def test_list_all_reports_comprehensive_database():
    admin_login = client.post(
        "/api/auth/login",
        json={"email": "admin@claimsight.ai", "password": "ClaimsightAdmin2026!"}
    )
    token = admin_login.json()["access_token"]

    res = client.get("/api/reports", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.json()
    assert data["total_claims"] >= 16
    assert data["total_investigated"] > 0
    assert data["total_uninvestigated"] > 0
    assert data["total_high_impact_over_5l"] >= 3

def test_claimant_strictly_isolated_from_other_claims_and_siu():
    # Login as policyholder Rajesh Kumar
    res = client.post(
        "/api/auth/login",
        json={"email": "claimant@claimsight.ai", "password": "Claimant2026!"}
    )
    assert res.status_code == 200
    claimant_token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {claimant_token}"}

    # 1. Claims directory must only return claims belonging to claimant@claimsight.ai
    list_res = client.get("/api/claims", headers=headers)
    assert list_res.status_code == 200
    claims = list_res.json()["claims"]
    assert len(claims) >= 1
    for c in claims:
        assert c.get("claimant", {}).get("email") == "claimant@claimsight.ai"

    # 2. Accessing someone else's claim (CLM-2026-002) must return HTTP 403 Forbidden
    other_res = client.get("/api/claims/CLM-2026-002", headers=headers)
    assert other_res.status_code == 403

    # 3. Accessing SIU investigation relationship graph must return HTTP 403 Forbidden
    siu_res = client.get("/api/claims/CLM-2026-001/relationships", headers=headers)
    assert siu_res.status_code == 403

def test_relationship_graph_returns_nodes_and_edges():
    # Login as investigator
    res = client.post(
        "/api/auth/login",
        json={"email": "investigator@claimsight.ai", "password": "Investigator2026!"}
    )
    token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    graph_res = client.get("/api/claims/CLM-2026-002/relationships", headers=headers)
    assert graph_res.status_code == 200
    graph_data = graph_res.json()
    assert "nodes" in graph_data
    assert "edges" in graph_data
    assert len(graph_data["nodes"]) >= 5
    assert len(graph_data["edges"]) >= 3

def test_claim_creation_restricted_to_policyholder_with_image_reflection():
    # 1. Chief Officer (Admin) attempting to create claim must be rejected (403)
    admin_login = client.post("/api/auth/login", json={"email": "admin@claimsight.ai", "password": "ClaimsightAdmin2026!"})
    admin_token = admin_login.json()["access_token"]
    payload = {
        "policy_number": "POL-TEST-9999",
        "claimant": {"name": "Test Claimant", "phone": "+91 99999 88888", "email": "test@example.com"},
        "vehicle": {"registration": "KA-01-XX-9999", "make": "Hyundai", "model": "Verna", "year": 2024},
        "incident_date": "2026-03-22",
        "incident_time": "11:00",
        "incident_location": "MG Road, Bengaluru",
        "accident_type": "Rear-End Collision",
        "reported_narrative": "Car rear bumper valence hit while slowing down.",
        "estimated_damage": 35000,
        "vehicle_image_url": "https://images.unsplash.com/photo-1549399542-7e3f8b79c341"
    }
    res_admin = client.post("/api/claims", json=payload, headers={"Authorization": f"Bearer {admin_token}"})
    assert res_admin.status_code == 403

    # 2. Senior Investigator attempting to create claim must be rejected (403)
    inv_login = client.post("/api/auth/login", json={"email": "investigator@claimsight.ai", "password": "Investigator2026!"})
    inv_token = inv_login.json()["access_token"]
    res_inv = client.post("/api/claims", json=payload, headers={"Authorization": f"Bearer {inv_token}"})
    assert res_inv.status_code == 403

    # 3. Policyholder (Claimant) successfully creates claim and image is stored
    claimant_login = client.post("/api/auth/login", json={"email": "claimant@claimsight.ai", "password": "Claimant2026!"})
    claimant_token = claimant_login.json()["access_token"]
    payload["claimant"]["email"] = "claimant@claimsight.ai"
    res_claimant = client.post("/api/claims", json=payload, headers={"Authorization": f"Bearer {claimant_token}"})
    assert res_claimant.status_code == 201
    created_claim = res_claimant.json()
    assert created_claim["vehicle_image_url"] == payload["vehicle_image_url"]

    # 4. Chief Officer fetches this claim and can see the uploaded vehicle image
    res_get = client.get(f"/api/claims/{created_claim['claim_id']}", headers={"Authorization": f"Bearer {admin_token}"})
    assert res_get.status_code == 200
    fetched_claim = res_get.json()
    assert fetched_claim["claim"]["vehicle_image_url"] == payload["vehicle_image_url"]

def test_siu_pdf_download_succeeds():
    # Verify PDF generation & download works reliably with HTTP 200 and application/pdf
    res = client.get("/api/reports/CLM-2026-002/download")
    assert res.status_code == 200
    assert "application/pdf" in res.headers.get("content-type", "")
    assert len(res.content) > 1000
    assert res.content.startswith(b"%PDF")

def test_yolo_detection_endpoint():
    login_res = client.post("/api/auth/login", json={"email": "admin@claimsight.ai", "password": "ClaimsightAdmin2026!"})
    token = login_res.json()["access_token"]
    res = client.get("/api/claims/CLM-2026-002/yolo-detection", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.json()
    assert data["claim_id"] == "CLM-2026-002"
    assert "yolo_detection" in data
    assert data["yolo_detection"]["status"] == "success"
    assert len(data["yolo_detection"]["detections"]) > 0

def test_fir_pdf_download_succeeds_for_investigator_and_direct():
    # Direct endpoint
    res_direct = client.get("/api/reports/CLM-2026-002/fir-download")
    assert res_direct.status_code == 200
    assert "application/pdf" in res_direct.headers.get("content-type", "")
    assert res_direct.content.startswith(b"%PDF")

    # Authenticated investigator endpoint
    inv_login = client.post("/api/auth/login", json={"email": "investigator@claimsight.ai", "password": "Investigator2026!"})
    token = inv_login.json()["access_token"]
    res_auth = client.get("/api/reports/CLM-2026-002/fir/download", headers={"Authorization": f"Bearer {token}"})
    assert res_auth.status_code == 200
    assert "application/pdf" in res_auth.headers.get("content-type", "")
    assert res_auth.content.startswith(b"%PDF")

def test_fir_pdf_download_forbidden_for_claimant():
    claimant_login = client.post("/api/auth/login", json={"email": "claimant@claimsight.ai", "password": "Claimant2026!"})
    token = claimant_login.json()["access_token"]
    res = client.get("/api/reports/CLM-2026-002/fir/download", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 403



