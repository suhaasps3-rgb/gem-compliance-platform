-- 🟢 LIVE: Regulatory Versioning Engine
CREATE TABLE regulatory_rules (
    id UUID PRIMARY KEY,
    rule_identifier VARCHAR(100) NOT NULL,
    effective_from DATE NOT NULL,
    source_reference VARCHAR(255),
    superseded_by UUID REFERENCES regulatory_rules(id),
    logic_schema JSONB
);

-- 🟢 LIVE: Core Bidding Entities
CREATE TABLE tenders (
    id UUID PRIMARY KEY,
    reference_number VARCHAR(50) UNIQUE NOT NULL,
    closing_date TIMESTAMP WITH TIME ZONE NOT NULL,
    rules_schema JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE bidders (
    id UUID PRIMARY KEY,
    primary_pan VARCHAR(10) UNIQUE,
    fuzzy_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE documents (
    id UUID PRIMARY KEY,
    bidder_id UUID REFERENCES bidders(id),
    tender_id UUID REFERENCES tenders(id),
    doc_type VARCHAR(50),
    s3_uri VARCHAR(255) NOT NULL,
    extraction_status VARCHAR(20),
    extracted_claims JSONB
);

-- 🟢 LIVE: Evidence Graph (NetworkX Persistence)
CREATE TABLE evidence_graphs (
    id UUID PRIMARY KEY,
    bidder_id UUID REFERENCES bidders(id),
    tender_id UUID REFERENCES tenders(id),
    graph_state JSONB NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 🟢 LIVE: Compliance & Contradictions
CREATE TABLE compliance_checks (
    id UUID PRIMARY KEY,
    bidder_id UUID REFERENCES bidders(id),
    requirement_rule_id UUID REFERENCES regulatory_rules(id),
    status VARCHAR(20), -- 'Verified Compliant', 'Non-Compliant', 'Needs Review', 'Unverified', 'Not Applicable'
    confidence_score NUMERIC(3,2),
    risk_score INTEGER
);

CREATE TABLE verification_events (
    id UUID PRIMARY KEY,
    compliance_check_id UUID REFERENCES compliance_checks(id),
    source VARCHAR(50),
    event_timestamp TIMESTAMP,
    raw_response JSONB
);

CREATE TABLE contradictions (
    id UUID PRIMARY KEY,
    bidder_id UUID REFERENCES bidders(id),
    tender_id UUID REFERENCES tenders(id),
    claim_node JSONB,
    evidence_node JSONB,
    ai_synthesis TEXT,
    status VARCHAR(20)
);

-- 🟢 LIVE: Officer Actions & Audit
CREATE TABLE officer_decisions (
    id UUID PRIMARY KEY,
    bidder_id UUID REFERENCES bidders(id),
    contradiction_id UUID REFERENCES contradictions(id),
    action_type VARCHAR(50),
    rule_citation_id UUID REFERENCES regulatory_rules(id),
    escalation_flag_id UUID REFERENCES regulatory_rules(id),
    justification TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE audit_events (
    id UUID PRIMARY KEY,
    event_type VARCHAR(50),
    payload JSONB,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    previous_hash VARCHAR(64),
    current_hash VARCHAR(64)
);
