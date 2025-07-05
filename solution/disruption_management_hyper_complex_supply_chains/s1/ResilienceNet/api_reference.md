# ResilienceNet API Reference

**Complete API Documentation for ResilienceNet Platform**

---

## Table of Contents

1. [API Overview](#api-overview)
2. [Authentication](#authentication)
3. [Risk Assessment API](#risk-assessment-api)
4. [Anomaly Detection API](#anomaly-detection-api)
5. [Impact Analysis API](#impact-analysis-api)
6. [Simulation API](#simulation-api)
7. [Analytics API](#analytics-api)
8. [Entity Management API](#entity-management-api)
9. [Notification API](#notification-api)
10. [Error Handling](#error-handling)
11. [Rate Limiting](#rate-limiting)
12. [SDK and Examples](#sdk-and-examples)

---

## API Overview

### Base URL
```
Production: https://api.resiliencenet.com/v1
Staging: https://staging-api.resiliencenet.com/v1
Development: http://localhost:5000/api/v1
```

### API Versioning
The ResilienceNet API uses URL-based versioning. The current version is `v1`. All endpoints are prefixed with `/api/v1/`.

### Content Type
All API requests and responses use JSON format:
```
Content-Type: application/json
Accept: application/json
```

### HTTP Methods
- **GET**: Retrieve data
- **POST**: Create new resources
- **PUT**: Update existing resources
- **PATCH**: Partial updates
- **DELETE**: Remove resources

### Response Format
All API responses follow a consistent format:

**Success Response:**
```json
{
  "success": true,
  "data": {
    // Response data
  },
  "metadata": {
    "timestamp": "2025-01-15T10:30:00Z",
    "request_id": "req_123456789",
    "version": "v1"
  }
}
```

**Error Response:**
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input parameters",
    "details": {
      "field": "entity_id",
      "reason": "Required field missing"
    }
  },
  "metadata": {
    "timestamp": "2025-01-15T10:30:00Z",
    "request_id": "req_123456789",
    "version": "v1"
  }
}
```

---

## Authentication

### JWT Token Authentication

ResilienceNet uses JWT (JSON Web Token) for API authentication. Tokens must be included in the Authorization header for all API requests.

#### Obtaining a Token

**Endpoint:** `POST /auth/login`

**Request:**
```json
{
  "username": "your_username",
  "password": "your_password",
  "mfa_code": "123456"  // Optional, if MFA is enabled
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_in": 3600,
    "token_type": "Bearer"
  }
}
```

#### Using the Token

Include the token in the Authorization header:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### Refreshing Tokens

**Endpoint:** `POST /auth/refresh`

**Request:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### API Keys (Service-to-Service)

For service-to-service communication, use API keys:

**Header:**
```
X-API-Key: your_api_key_here
```

---

## Risk Assessment API

### Get Risk Assessment

Retrieve the current risk assessment for a specific entity.

**Endpoint:** `GET /risk/assessment/{entity_id}`

**Parameters:**
- `entity_id` (path, required): Unique identifier for the entity
- `include_history` (query, optional): Include historical risk scores (default: false)
- `time_range` (query, optional): Time range for historical data (7d, 30d, 90d)

**Example Request:**
```bash
curl -X GET "https://api.resiliencenet.com/v1/risk/assessment/SUPPLIER_001?include_history=true&time_range=30d" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "entity_id": "SUPPLIER_001",
    "entity_type": "supplier",
    "risk_score": 65.2,
    "risk_level": "medium",
    "confidence": 0.92,
    "last_updated": "2025-01-15T10:30:00Z",
    "risk_factors": [
      {
        "factor": "supplier_reliability",
        "value": 0.75,
        "weight": 0.35,
        "contribution": 22.8
      },
      {
        "factor": "transportation_capacity",
        "value": 0.60,
        "weight": 0.25,
        "contribution": 15.0
      }
    ],
    "recommendations": [
      {
        "id": "rec_001",
        "type": "diversify_suppliers",
        "priority": "high",
        "description": "Consider adding backup suppliers for critical components",
        "estimated_impact": 15.2,
        "implementation_cost": 50000
      }
    ],
    "history": [
      {
        "date": "2025-01-14",
        "risk_score": 63.8
      },
      {
        "date": "2025-01-13",
        "risk_score": 64.1
      }
    ]
  }
}
```

### Create Risk Assessment

Trigger a new risk assessment for one or more entities.

**Endpoint:** `POST /risk/assessment`

**Request Body:**
```json
{
  "entities": [
    {
      "entity_id": "SUPPLIER_001",
      "entity_type": "supplier"
    }
  ],
  "parameters": {
    "include_historical": true,
    "forecast_horizon": 30,
    "scenario_factors": {
      "geopolitical_risk": 0.8,
      "weather_risk": 0.3
    }
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "assessment_id": "assess_123456",
    "status": "queued",
    "entities": ["SUPPLIER_001"],
    "estimated_completion": "2025-01-15T10:35:00Z",
    "progress_url": "/risk/assessment/assess_123456/status"
  }
}
```

### Get Assessment Status

Check the status of a running assessment.

**Endpoint:** `GET /risk/assessment/{assessment_id}/status`

**Response:**
```json
{
  "success": true,
  "data": {
    "assessment_id": "assess_123456",
    "status": "completed",
    "progress": 100,
    "started_at": "2025-01-15T10:30:00Z",
    "completed_at": "2025-01-15T10:34:30Z",
    "results_url": "/risk/assessment/assess_123456/results"
  }
}
```

### Bulk Risk Assessment

Perform risk assessment for multiple entities.

**Endpoint:** `POST /risk/assessment/bulk`

**Request Body:**
```json
{
  "entity_filter": {
    "entity_type": "supplier",
    "location": "India",
    "risk_threshold": 50
  },
  "parameters": {
    "include_historical": true,
    "forecast_horizon": 30
  }
}
```

---

## Anomaly Detection API

### Detect Anomalies

Submit data points for real-time anomaly detection.

**Endpoint:** `POST /anomaly/detect`

**Request Body:**
```json
{
  "data_points": [
    {
      "timestamp": "2025-01-15T10:30:00Z",
      "entity_id": "DC_001",
      "metrics": {
        "cost": 85.5,
        "supplier_performance": 0.92,
        "inventory_level": 0.65,
        "demand": 1250
      }
    }
  ],
  "detection_parameters": {
    "sensitivity": 0.95,
    "include_context": true
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "detection_id": "detect_789012",
    "anomalies": [
      {
        "data_point_index": 0,
        "anomaly_type": "cost",
        "severity": "medium",
        "anomaly_score": -0.65,
        "expected_value": 75.2,
        "actual_value": 85.5,
        "confidence": 0.88,
        "potential_causes": [
          "supplier_price_increase",
          "transportation_cost_spike"
        ]
      }
    ],
    "summary": {
      "total_points": 1,
      "anomalies_detected": 1,
      "highest_severity": "medium"
    }
  }
}
```

### Get Anomaly History

Retrieve historical anomalies for analysis.

**Endpoint:** `GET /anomaly/history`

**Parameters:**
- `entity_id` (query, optional): Filter by specific entity
- `entity_type` (query, optional): Filter by entity type
- `severity` (query, optional): Filter by severity level
- `start_date` (query, optional): Start date for time range
- `end_date` (query, optional): End date for time range
- `limit` (query, optional): Maximum number of results (default: 100)
- `offset` (query, optional): Pagination offset (default: 0)

**Example Request:**
```bash
curl -X GET "https://api.resiliencenet.com/v1/anomaly/history?entity_type=supplier&severity=high&limit=50" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "anomalies": [
      {
        "id": "anom_001",
        "timestamp": "2025-01-15T09:15:00Z",
        "entity_id": "SUPPLIER_002",
        "entity_type": "supplier",
        "anomaly_type": "performance",
        "severity": "high",
        "anomaly_score": -0.85,
        "description": "Supplier performance dropped significantly below expected levels",
        "status": "acknowledged",
        "resolved_at": null
      }
    ],
    "pagination": {
      "total": 156,
      "limit": 50,
      "offset": 0,
      "has_more": true
    }
  }
}
```

### Update Anomaly Status

Update the status of an anomaly (acknowledge, resolve, etc.).

**Endpoint:** `PATCH /anomaly/{anomaly_id}`

**Request Body:**
```json
{
  "status": "resolved",
  "resolution_notes": "Issue resolved by switching to backup supplier",
  "assigned_to": "user_123"
}
```

---

## Impact Analysis API

### Predict Impact

Analyze the potential impact of a disruption scenario.

**Endpoint:** `POST /impact/predict`

**Request Body:**
```json
{
  "disruption_scenario": {
    "affected_entities": [
      {
        "entity_id": "SUPPLIER_001",
        "disruption_type": "complete_failure",
        "severity": 1.0,
        "duration_days": 7
      }
    ],
    "start_date": "2025-01-20T00:00:00Z"
  },
  "analysis_parameters": {
    "time_horizon": 30,
    "include_alternatives": true,
    "cost_calculation": true
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "prediction_id": "pred_345678",
    "scenario_summary": {
      "total_affected_entities": 15,
      "estimated_cost_impact": 2500000,
      "service_level_impact": -12.5,
      "recovery_time_days": 14
    },
    "affected_entities": [
      {
        "entity_id": "DC_001",
        "entity_type": "distribution_center",
        "impact_severity": 0.75,
        "impact_type": "capacity_reduction",
        "estimated_cost": 150000,
        "recovery_days": 10
      }
    ],
    "mitigation_options": [
      {
        "strategy": "activate_backup_supplier",
        "cost": 75000,
        "effectiveness": 0.80,
        "implementation_time_hours": 24
      }
    ],
    "network_analysis": {
      "critical_paths_affected": 3,
      "alternative_routes": 2,
      "bottleneck_entities": ["DC_002", "TRANSPORT_005"]
    }
  }
}
```

### Get Network Graph

Retrieve the supply chain network graph for visualization.

**Endpoint:** `GET /impact/network/{entity_id}`

**Parameters:**
- `entity_id` (path, required): Central entity for network extraction
- `depth` (query, optional): Number of hops to include (default: 2, max: 5)
- `include_metrics` (query, optional): Include performance metrics (default: false)

**Response:**
```json
{
  "success": true,
  "data": {
    "network": {
      "nodes": [
        {
          "id": "SUPPLIER_001",
          "type": "supplier",
          "properties": {
            "name": "ABC Manufacturing",
            "location": "Mumbai, India",
            "capacity": 10000,
            "reliability_score": 0.85
          }
        }
      ],
      "edges": [
        {
          "source": "SUPPLIER_001",
          "target": "DC_001",
          "relationship": "supplies",
          "properties": {
            "capacity": 5000,
            "lead_time_days": 3,
            "cost_per_unit": 25.50
          }
        }
      ]
    },
    "statistics": {
      "total_nodes": 25,
      "total_edges": 48,
      "network_density": 0.15,
      "average_path_length": 2.8
    }
  }
}
```

---

## Simulation API

### Create Simulation Scenario

Create and configure a new simulation scenario.

**Endpoint:** `POST /simulation/scenario`

**Request Body:**
```json
{
  "name": "Red Sea Crisis Simulation",
  "description": "Simulate impact of Red Sea shipping disruption",
  "duration_days": 30,
  "initial_conditions": {
    "inventory_levels": "normal",
    "demand_pattern": "seasonal_high",
    "supplier_performance": "baseline"
  },
  "disruption_events": [
    {
      "event_type": "transportation_disruption",
      "affected_routes": ["ROUTE_ASIA_EUROPE"],
      "start_day": 5,
      "duration_days": 14,
      "severity": 0.8,
      "description": "Major shipping route disruption"
    }
  ],
  "intervention_strategies": [
    {
      "strategy_type": "route_diversification",
      "trigger_conditions": {
        "service_level_below": 0.85
      },
      "implementation_delay_hours": 48
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "scenario_id": "sim_901234",
    "name": "Red Sea Crisis Simulation",
    "status": "created",
    "estimated_runtime_minutes": 15,
    "created_at": "2025-01-15T10:30:00Z"
  }
}
```

### Start Simulation

Execute a configured simulation scenario.

**Endpoint:** `POST /simulation/{scenario_id}/start`

**Request Body:**
```json
{
  "execution_parameters": {
    "time_step_hours": 6,
    "random_seed": 12345,
    "parallel_execution": true
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "execution_id": "exec_567890",
    "scenario_id": "sim_901234",
    "status": "running",
    "started_at": "2025-01-15T10:35:00Z",
    "estimated_completion": "2025-01-15T10:50:00Z",
    "progress_url": "/simulation/exec_567890/progress"
  }
}
```

### Get Simulation Progress

Monitor the progress of a running simulation.

**Endpoint:** `GET /simulation/{execution_id}/progress`

**Response:**
```json
{
  "success": true,
  "data": {
    "execution_id": "exec_567890",
    "scenario_id": "sim_901234",
    "status": "running",
    "progress_percentage": 65,
    "current_simulation_day": 19,
    "total_simulation_days": 30,
    "elapsed_time_seconds": 450,
    "estimated_remaining_seconds": 240,
    "current_metrics": {
      "service_level": 0.78,
      "total_cost": 1250000,
      "active_disruptions": 1
    }
  }
}
```

### Get Simulation Results

Retrieve the results of a completed simulation.

**Endpoint:** `GET /simulation/{execution_id}/results`

**Response:**
```json
{
  "success": true,
  "data": {
    "execution_id": "exec_567890",
    "scenario_id": "sim_901234",
    "status": "completed",
    "execution_time_seconds": 720,
    "summary_metrics": {
      "average_service_level": 0.82,
      "total_cost": 2750000,
      "cost_increase_percentage": 15.2,
      "recovery_time_days": 18,
      "customer_impact_score": 0.25
    },
    "timeline": [
      {
        "day": 1,
        "service_level": 0.95,
        "total_cost": 85000,
        "active_events": []
      },
      {
        "day": 5,
        "service_level": 0.88,
        "total_cost": 92000,
        "active_events": ["transportation_disruption"]
      }
    ],
    "entity_performance": [
      {
        "entity_id": "SUPPLIER_001",
        "entity_type": "supplier",
        "average_utilization": 0.85,
        "disruption_impact": 0.15,
        "recovery_performance": 0.92
      }
    ],
    "recommendations": [
      {
        "recommendation": "Increase safety stock for critical components",
        "impact": "Reduce service level impact by 8%",
        "cost": 125000
      }
    ]
  }
}
```

### List Scenarios

Get a list of all simulation scenarios.

**Endpoint:** `GET /simulation/scenarios`

**Parameters:**
- `status` (query, optional): Filter by scenario status
- `created_by` (query, optional): Filter by creator
- `limit` (query, optional): Maximum number of results
- `offset` (query, optional): Pagination offset

**Response:**
```json
{
  "success": true,
  "data": {
    "scenarios": [
      {
        "scenario_id": "sim_901234",
        "name": "Red Sea Crisis Simulation",
        "description": "Simulate impact of Red Sea shipping disruption",
        "status": "completed",
        "created_at": "2025-01-15T10:30:00Z",
        "created_by": "user_123",
        "last_execution": "2025-01-15T11:00:00Z"
      }
    ],
    "pagination": {
      "total": 25,
      "limit": 20,
      "offset": 0,
      "has_more": true
    }
  }
}
```

---

## Analytics API

### Get Dashboard Metrics

Retrieve key metrics for dashboard display.

**Endpoint:** `GET /analytics/dashboard`

**Parameters:**
- `time_range` (query, optional): Time range for metrics (1h, 24h, 7d, 30d)
- `entity_filter` (query, optional): Filter by entity type or location

**Response:**
```json
{
  "success": true,
  "data": {
    "overall_risk_score": 45.2,
    "risk_trend": "stable",
    "active_alerts": 12,
    "critical_alerts": 2,
    "service_level": 0.94,
    "cost_variance": 0.08,
    "supplier_performance": 0.87,
    "inventory_health": 0.91,
    "recent_assessments": 156,
    "pending_recommendations": 8,
    "last_updated": "2025-01-15T10:30:00Z"
  }
}
```

### Get Trend Analysis

Analyze trends for specific metrics over time.

**Endpoint:** `GET /analytics/trends`

**Parameters:**
- `metric` (query, required): Metric to analyze (risk_score, service_level, cost, etc.)
- `entity_id` (query, optional): Specific entity to analyze
- `entity_type` (query, optional): Entity type filter
- `time_range` (query, required): Time range for analysis
- `granularity` (query, optional): Data granularity (hour, day, week)

**Response:**
```json
{
  "success": true,
  "data": {
    "metric": "risk_score",
    "time_range": "30d",
    "granularity": "day",
    "data_points": [
      {
        "timestamp": "2025-01-01T00:00:00Z",
        "value": 42.5,
        "entity_count": 150
      },
      {
        "timestamp": "2025-01-02T00:00:00Z",
        "value": 43.1,
        "entity_count": 152
      }
    ],
    "statistics": {
      "average": 44.8,
      "minimum": 38.2,
      "maximum": 52.1,
      "standard_deviation": 3.7,
      "trend_direction": "increasing",
      "trend_strength": 0.65
    }
  }
}
```

### Generate Report

Create a custom analytical report.

**Endpoint:** `POST /analytics/reports`

**Request Body:**
```json
{
  "report_type": "risk_assessment",
  "title": "Monthly Risk Assessment Report",
  "parameters": {
    "time_period": {
      "start_date": "2025-01-01",
      "end_date": "2025-01-31"
    },
    "entity_filter": {
      "entity_types": ["supplier", "distribution_center"],
      "locations": ["India", "Southeast Asia"]
    },
    "metrics": [
      "risk_score",
      "service_level",
      "cost_variance",
      "supplier_performance"
    ],
    "include_recommendations": true,
    "format": "pdf"
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "report_id": "rpt_123456",
    "status": "generating",
    "estimated_completion": "2025-01-15T10:35:00Z",
    "download_url": null,
    "progress_url": "/analytics/reports/rpt_123456/status"
  }
}
```

---

## Entity Management API

### List Entities

Get a list of supply chain entities.

**Endpoint:** `GET /entities`

**Parameters:**
- `entity_type` (query, optional): Filter by entity type
- `location` (query, optional): Filter by location
- `status` (query, optional): Filter by status (active, inactive)
- `search` (query, optional): Search by name or ID
- `limit` (query, optional): Maximum number of results
- `offset` (query, optional): Pagination offset

**Response:**
```json
{
  "success": true,
  "data": {
    "entities": [
      {
        "entity_id": "SUPPLIER_001",
        "entity_type": "supplier",
        "name": "ABC Manufacturing",
        "location": {
          "country": "India",
          "state": "Maharashtra",
          "city": "Mumbai"
        },
        "status": "active",
        "capacity": 10000,
        "reliability_score": 0.85,
        "last_updated": "2025-01-15T10:30:00Z"
      }
    ],
    "pagination": {
      "total": 250,
      "limit": 50,
      "offset": 0,
      "has_more": true
    }
  }
}
```

### Get Entity Details

Retrieve detailed information about a specific entity.

**Endpoint:** `GET /entities/{entity_id}`

**Response:**
```json
{
  "success": true,
  "data": {
    "entity_id": "SUPPLIER_001",
    "entity_type": "supplier",
    "name": "ABC Manufacturing",
    "description": "Leading electronics component manufacturer",
    "location": {
      "country": "India",
      "state": "Maharashtra",
      "city": "Mumbai",
      "coordinates": {
        "latitude": 19.0760,
        "longitude": 72.8777
      }
    },
    "contact_information": {
      "primary_contact": "John Doe",
      "email": "john.doe@abcmfg.com",
      "phone": "+91-22-1234-5678"
    },
    "operational_metrics": {
      "capacity": 10000,
      "current_utilization": 0.75,
      "reliability_score": 0.85,
      "average_lead_time_days": 7,
      "quality_score": 0.92
    },
    "financial_information": {
      "credit_rating": "A",
      "payment_terms": "Net 30",
      "currency": "INR"
    },
    "relationships": [
      {
        "related_entity_id": "DC_001",
        "relationship_type": "supplies",
        "capacity": 5000,
        "lead_time_days": 3
      }
    ],
    "risk_profile": {
      "current_risk_score": 45.2,
      "risk_factors": [
        {
          "factor": "financial_stability",
          "score": 0.85,
          "trend": "stable"
        }
      ]
    },
    "created_at": "2024-01-15T10:30:00Z",
    "last_updated": "2025-01-15T10:30:00Z"
  }
}
```

### Create Entity

Add a new entity to the system.

**Endpoint:** `POST /entities`

**Request Body:**
```json
{
  "entity_id": "SUPPLIER_002",
  "entity_type": "supplier",
  "name": "XYZ Components",
  "description": "Specialized automotive parts supplier",
  "location": {
    "country": "India",
    "state": "Tamil Nadu",
    "city": "Chennai"
  },
  "contact_information": {
    "primary_contact": "Jane Smith",
    "email": "jane.smith@xyzcomp.com",
    "phone": "+91-44-9876-5432"
  },
  "operational_metrics": {
    "capacity": 8000,
    "reliability_score": 0.90,
    "average_lead_time_days": 5
  }
}
```

### Update Entity

Update an existing entity's information.

**Endpoint:** `PUT /entities/{entity_id}`

**Request Body:**
```json
{
  "operational_metrics": {
    "capacity": 12000,
    "reliability_score": 0.88
  },
  "contact_information": {
    "phone": "+91-44-9876-5433"
  }
}
```

---

## Notification API

### Get Notifications

Retrieve notifications for the current user.

**Endpoint:** `GET /notifications`

**Parameters:**
- `status` (query, optional): Filter by status (unread, read, all)
- `type` (query, optional): Filter by notification type
- `priority` (query, optional): Filter by priority level
- `limit` (query, optional): Maximum number of results
- `offset` (query, optional): Pagination offset

**Response:**
```json
{
  "success": true,
  "data": {
    "notifications": [
      {
        "id": "notif_001",
        "type": "risk_alert",
        "priority": "high",
        "title": "High Risk Detected: SUPPLIER_001",
        "message": "Risk score increased to 78.5 for SUPPLIER_001",
        "status": "unread",
        "created_at": "2025-01-15T10:30:00Z",
        "data": {
          "entity_id": "SUPPLIER_001",
          "risk_score": 78.5,
          "previous_score": 65.2
        },
        "actions": [
          {
            "label": "View Details",
            "url": "/risk/assessment/SUPPLIER_001"
          },
          {
            "label": "Acknowledge",
            "action": "acknowledge"
          }
        ]
      }
    ],
    "summary": {
      "total": 25,
      "unread": 8,
      "high_priority": 3
    }
  }
}
```

### Mark Notification as Read

Update the status of a notification.

**Endpoint:** `PATCH /notifications/{notification_id}`

**Request Body:**
```json
{
  "status": "read"
}
```

### Create Notification

Send a custom notification (admin only).

**Endpoint:** `POST /notifications`

**Request Body:**
```json
{
  "recipients": ["user_123", "user_456"],
  "type": "system_announcement",
  "priority": "medium",
  "title": "Scheduled Maintenance",
  "message": "System maintenance scheduled for tonight 2-4 AM",
  "data": {
    "maintenance_window": "2025-01-16T02:00:00Z to 2025-01-16T04:00:00Z"
  }
}
```

---

## Error Handling

### Error Codes

ResilienceNet uses standard HTTP status codes along with custom error codes:

**HTTP Status Codes:**
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `409` - Conflict
- `422` - Unprocessable Entity
- `429` - Too Many Requests
- `500` - Internal Server Error
- `503` - Service Unavailable

**Custom Error Codes:**
- `VALIDATION_ERROR` - Input validation failed
- `AUTHENTICATION_FAILED` - Invalid credentials
- `AUTHORIZATION_DENIED` - Insufficient permissions
- `RESOURCE_NOT_FOUND` - Requested resource doesn't exist
- `RATE_LIMIT_EXCEEDED` - API rate limit exceeded
- `SIMULATION_FAILED` - Simulation execution failed
- `MODEL_UNAVAILABLE` - ML model temporarily unavailable
- `DATA_PROCESSING_ERROR` - Error processing input data

### Error Response Format

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input parameters",
    "details": {
      "field": "entity_id",
      "reason": "Required field missing",
      "provided_value": null
    },
    "suggestion": "Please provide a valid entity_id"
  },
  "metadata": {
    "timestamp": "2025-01-15T10:30:00Z",
    "request_id": "req_123456789",
    "version": "v1"
  }
}
```

### Handling Errors

**Best Practices:**
1. Always check the `success` field in responses
2. Use the `error.code` for programmatic error handling
3. Display `error.message` to users
4. Log `request_id` for debugging
5. Implement retry logic for transient errors (5xx status codes)

**Example Error Handling (JavaScript):**
```javascript
async function callAPI(endpoint, options) {
  try {
    const response = await fetch(endpoint, options);
    const data = await response.json();
    
    if (!data.success) {
      switch (data.error.code) {
        case 'RATE_LIMIT_EXCEEDED':
          // Wait and retry
          await new Promise(resolve => setTimeout(resolve, 60000));
          return callAPI(endpoint, options);
        
        case 'AUTHENTICATION_FAILED':
          // Refresh token and retry
          await refreshAuthToken();
          return callAPI(endpoint, options);
        
        default:
          throw new Error(data.error.message);
      }
    }
    
    return data.data;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
}
```

---

## Rate Limiting

### Rate Limits

ResilienceNet implements rate limiting to ensure fair usage and system stability:

**Default Limits:**
- **Standard Users**: 1,000 requests per hour
- **Premium Users**: 5,000 requests per hour
- **Enterprise Users**: 10,000 requests per hour
- **Service Accounts**: 50,000 requests per hour

**Endpoint-Specific Limits:**
- **Simulation API**: 10 concurrent simulations per user
- **Bulk Operations**: 5 requests per minute
- **Report Generation**: 20 reports per hour

### Rate Limit Headers

All API responses include rate limit information in headers:

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1642248000
X-RateLimit-Window: 3600
```

### Handling Rate Limits

When rate limits are exceeded, the API returns a `429 Too Many Requests` status:

```json
{
  "success": false,
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Try again in 60 seconds.",
    "details": {
      "limit": 1000,
      "window_seconds": 3600,
      "reset_time": "2025-01-15T11:00:00Z"
    }
  }
}
```

**Best Practices:**
1. Monitor rate limit headers
2. Implement exponential backoff for retries
3. Cache responses when possible
4. Use bulk operations for multiple requests
5. Consider upgrading for higher limits

---

## SDK and Examples

### Official SDKs

ResilienceNet provides official SDKs for popular programming languages:

**Python SDK:**
```bash
pip install resiliencenet-sdk
```

```python
from resiliencenet import ResilienceNetClient

client = ResilienceNetClient(
    api_key="your_api_key",
    base_url="https://api.resiliencenet.com/v1"
)

# Get risk assessment
assessment = client.risk.get_assessment("SUPPLIER_001")
print(f"Risk Score: {assessment.risk_score}")

# Detect anomalies
anomalies = client.anomaly.detect([
    {
        "timestamp": "2025-01-15T10:30:00Z",
        "entity_id": "DC_001",
        "metrics": {"cost": 85.5, "performance": 0.92}
    }
])
```

**JavaScript SDK:**
```bash
npm install @resiliencenet/sdk
```

```javascript
import { ResilienceNetClient } from '@resiliencenet/sdk';

const client = new ResilienceNetClient({
  apiKey: 'your_api_key',
  baseUrl: 'https://api.resiliencenet.com/v1'
});

// Get risk assessment
const assessment = await client.risk.getAssessment('SUPPLIER_001');
console.log(`Risk Score: ${assessment.riskScore}`);

// Create simulation
const simulation = await client.simulation.create({
  name: 'Test Scenario',
  durationDays: 30,
  disruptionEvents: [...]
});
```

### Code Examples

**Risk Assessment Workflow:**
```python
import asyncio
from resiliencenet import ResilienceNetClient

async def assess_supplier_risk(supplier_id):
    client = ResilienceNetClient(api_key="your_api_key")
    
    # Start assessment
    assessment = await client.risk.create_assessment({
        "entities": [{"entity_id": supplier_id, "entity_type": "supplier"}],
        "parameters": {"include_historical": True, "forecast_horizon": 30}
    })
    
    # Wait for completion
    while assessment.status != "completed":
        await asyncio.sleep(5)
        assessment = await client.risk.get_assessment_status(assessment.assessment_id)
    
    # Get results
    results = await client.risk.get_assessment_results(assessment.assessment_id)
    
    return results

# Usage
results = asyncio.run(assess_supplier_risk("SUPPLIER_001"))
print(f"Risk Score: {results.risk_score}")
```

**Anomaly Monitoring:**
```javascript
const client = new ResilienceNetClient({ apiKey: 'your_api_key' });

// Real-time anomaly monitoring
async function monitorAnomalies() {
  const stream = client.anomaly.subscribe({
    entityTypes: ['supplier', 'distribution_center'],
    severityThreshold: 'medium'
  });
  
  stream.on('anomaly', (anomaly) => {
    console.log(`Anomaly detected: ${anomaly.entityId}`);
    console.log(`Severity: ${anomaly.severity}`);
    console.log(`Type: ${anomaly.anomalyType}`);
    
    // Send alert
    sendAlert(anomaly);
  });
  
  stream.on('error', (error) => {
    console.error('Stream error:', error);
  });
}

monitorAnomalies();
```

**Simulation Automation:**
```python
def run_stress_test_simulation():
    client = ResilienceNetClient(api_key="your_api_key")
    
    # Define stress test scenario
    scenario = {
        "name": "Multi-Supplier Failure Stress Test",
        "duration_days": 14,
        "disruption_events": [
            {
                "event_type": "supplier_failure",
                "affected_entities": ["SUPPLIER_001", "SUPPLIER_002"],
                "start_day": 1,
                "duration_days": 7,
                "severity": 0.9
            },
            {
                "event_type": "transportation_disruption",
                "affected_routes": ["ROUTE_001"],
                "start_day": 3,
                "duration_days": 5,
                "severity": 0.7
            }
        ]
    }
    
    # Create and run simulation
    simulation = client.simulation.create(scenario)
    execution = client.simulation.start(simulation.scenario_id)
    
    # Monitor progress
    while execution.status == "running":
        time.sleep(30)
        execution = client.simulation.get_progress(execution.execution_id)
        print(f"Progress: {execution.progress_percentage}%")
    
    # Get results
    results = client.simulation.get_results(execution.execution_id)
    
    return {
        "service_level_impact": results.summary_metrics.average_service_level,
        "cost_impact": results.summary_metrics.total_cost,
        "recovery_time": results.summary_metrics.recovery_time_days,
        "recommendations": results.recommendations
    }
```

### Webhook Integration

**Setting up Webhooks:**
```python
# Configure webhook endpoint
webhook_config = {
    "url": "https://your-app.com/webhooks/resiliencenet",
    "events": ["risk_alert", "anomaly_detected", "simulation_completed"],
    "secret": "your_webhook_secret"
}

client.webhooks.create(webhook_config)
```

**Webhook Handler Example (Flask):**
```python
from flask import Flask, request, jsonify
import hmac
import hashlib

app = Flask(__name__)

@app.route('/webhooks/resiliencenet', methods=['POST'])
def handle_webhook():
    # Verify webhook signature
    signature = request.headers.get('X-ResilienceNet-Signature')
    payload = request.get_data()
    
    expected_signature = hmac.new(
        b'your_webhook_secret',
        payload,
        hashlib.sha256
    ).hexdigest()
    
    if not hmac.compare_digest(signature, f"sha256={expected_signature}"):
        return jsonify({"error": "Invalid signature"}), 401
    
    # Process webhook event
    event = request.json
    
    if event['type'] == 'risk_alert':
        handle_risk_alert(event['data'])
    elif event['type'] == 'anomaly_detected':
        handle_anomaly(event['data'])
    elif event['type'] == 'simulation_completed':
        handle_simulation_result(event['data'])
    
    return jsonify({"status": "success"})

def handle_risk_alert(data):
    # Send notification to team
    send_slack_message(f"High risk detected: {data['entity_id']}")

def handle_anomaly(data):
    # Log anomaly and trigger investigation
    log_anomaly(data)
    create_investigation_ticket(data)

def handle_simulation_result(data):
    # Process simulation results
    generate_report(data)
    notify_stakeholders(data)
```

---

## Conclusion

This API reference provides comprehensive documentation for integrating with the ResilienceNet platform. The API is designed to be RESTful, consistent, and easy to use while providing powerful capabilities for supply chain risk management and resilience planning.

For additional support, examples, or questions about the API, please contact our developer support team or visit the developer portal at https://developers.resiliencenet.com.

---

**API Version**: v1  
**Documentation Version**: 1.0  
**Last Updated**: January 15, 2025  
**Next Review**: April 15, 2025

