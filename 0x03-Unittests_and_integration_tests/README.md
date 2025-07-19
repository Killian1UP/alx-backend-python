# ALX Backend Python - Unittests and Integration Tests

This project implements various unit and integration tests for Python code. The tests are based on specific objectives outlined by ALX's backend curriculum, focusing on testing techniques, parameterization, patching, mocking, and memoization.

## Project Structure

```
.
├── client.py
├── test_client.py
├── test_utils.py
├── utils.py
└── fixtures.py
```

## Task Breakdown

### 0. Parameterize a Unit Test

- **File**: `test_utils.py`
- **Tested Function**: `utils.access_nested_map`
- **Technique**: `@parameterized.expand`
- **Goal**: Assert correct access of values in nested dictionaries.

### 1. Parameterized Exception Test

- **File**: `test_utils.py`
- **Tested Function**: `utils.access_nested_map`
- **Goal**: Assert `KeyError` is raised with correct message for missing keys.

### 2. Mock HTTP Calls

- **File**: `test_utils.py`
- **Tested Function**: `utils.get_json`
- **Goal**: Patch `requests.get` and mock `.json()` return values.

### 3. Memoization Test

- **File**: `test_utils.py`
- **Tested Function**: `utils.memoize`
- **Goal**: Mock method call and verify memoization only calls it once.

### 4. Parameterize and Patch (as Decorators)

- **File**: `test_client.py`
- **Tested Function**: `GithubOrgClient.org`
- **Goal**: Patch `get_json`, verify output and call count.

### 5. Mocking a Property

- **File**: `test_client.py`
- **Tested Function**: `GithubOrgClient._public_repos_url`
- **Goal**: Use `PropertyMock` to patch `.org` and verify URL returned.

### 6. More Patching

- **File**: `test_client.py`
- **Tested Function**: `GithubOrgClient.public_repos`
- **Goal**: Patch both `get_json` and `_public_repos_url`.

### 7. Parameterize License Check

- **File**: `test_client.py`
- **Tested Function**: `GithubOrgClient.has_license`
- **Goal**: Check if repos match a specified license key.

### 8. Integration Tests with Fixtures

- **File**: `test_client.py`
- **Fixtures**: `fixtures.py`
- **Test Class**: `TestIntegrationGithubOrgClient`
- **Goal**: Mock external requests using patch and side_effect.

### 9. Final Integration Verification

- **File**: `test_client.py`
- **Tests**:
  - `test_public_repos`
  - `test_public_repos_with_license`
- **Goal**: Ensure correct filtering and data retrieval based on fixtures.

## Tools and Libraries Used

- `unittest`
- `parameterized`
- `unittest.mock`
- `requests`
- `pycodestyle` (PEP8 validation)

## Running the Tests

```bash
python3 -m unittest test_utils.py
python3 -m unittest test_client.py
```

## Author

Ikaelelo Motlhako