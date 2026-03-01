# Clean Null Sales Rows

## Description

Given a list of row dictionaries, return only rows with a valid numeric `sales` value.

Rules:

- drop rows where `sales` is `null`
- drop rows where `sales` is not numeric
- keep order of valid rows

## Input

- `rows`: list of dictionaries with keys `id`, `region`, `sales`

## Output

- List of cleaned rows
