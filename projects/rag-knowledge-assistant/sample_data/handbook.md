# Internal Automation Handbook (Synthetic)

## Workflow approvals

Production workflow actions must be explicitly approved before an automation can dispatch them. The approval record should include the workflow name, requesting system, timestamp, and responsible owner.

## Data quality

Incoming provider data should be normalized before deduplication. Phone numbers should use a consistent canonical format, emails should be normalized to lowercase, and invalid records should be flagged rather than silently discarded.

## Document processing

Unstructured documents should be converted into structured fields with validation before they are sent to downstream business systems.
